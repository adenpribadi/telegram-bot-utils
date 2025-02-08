import pystray
from pystray import MenuItem as item, Icon
from PIL import Image
from src.bot import TelegramBot
from src.utils import read_tokens_from_file
import os
import sys

# Membaca semua token dari file config.txt
config_tokens = read_tokens_from_file("config.txt")
# Ambil TELEGRAM_BOT_TOKEN dari dictionary yang didapat
TELEGRAM_BOT_TOKEN = config_tokens.get("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan dalam file config.txt")

# Membuat instance bot
bot = TelegramBot(TELEGRAM_BOT_TOKEN)

# Membuat ikon tray
# image = Image.new('RGB', (64, 64), (255, 0, 0))  # Ikon merah sederhana
# image = Image.open("static/images/icon-white.png")  # Ganti dengan path ikon yang diinginkan
def resource_path(relative_path):
    """ Mengambil path absolut, menangani mode frozen (PyInstaller) """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Path sementara PyInstaller
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Load ikon dengan path yang benar
image_path = resource_path("static/images/icon-white.png")

if not os.path.exists(image_path):
    raise FileNotFoundError(f"Ikon tidak ditemukan: {image_path}")

image = Image.open(image_path)

# menu = (
#     item('Shutdown', lambda icon, item: shutdown()),
#     item('Restart', lambda icon, item: restart()),
#     item('Hibernate', lambda icon, item: hibernate()),
#     item('Exit', lambda icon, item: icon.stop())
# )

menu = (item('Exit', lambda icon, item: icon.stop()),)

icon = Icon("TrayControl", image, "Vzveda", menu=menu)

# Jalankan bot Telegram di thread lain
import threading
telegram_thread = threading.Thread(target=bot.start, daemon=True)
telegram_thread.start()

icon.run()
