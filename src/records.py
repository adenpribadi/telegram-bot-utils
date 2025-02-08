import cv2
import sounddevice as sd
import numpy as np
import wave
import os
import subprocess
import threading
import pyaudio
import time

# === SETUP CONFIG ===
VIDEO_FILENAME = "video_temp.avi"
AUDIO_FILENAME = "audio_temp.wav"
OUTPUT_FILENAME = "webcam.mp4"
FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe")  # Sesuaikan lokasi FFmpeg

# Konfigurasi untuk pengujian
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Mono untuk pengujian mikrofon
RATE = 44100  # Sampling rate
CHUNK = 1024  # Ukuran buffer

# Fungsi untuk menampilkan daftar perangkat audio
def list_audio_devices():
    audio = pyaudio.PyAudio()
    print("Daftar perangkat audio yang tersedia:")
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']} - Input Channels: {device_info['maxInputChannels']}")
    audio.terminate()

# Fungsi untuk menguji mikrofon pada perangkat tertentu
def test_microphone(device_index, duration=1):
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            input_device_index=device_index,
                            frames_per_buffer=CHUNK)

        frames = []
        print(f"Testing device {device_index}...")

        for _ in range(int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Konversi ke array NumPy untuk cek apakah ada suara
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        if np.max(np.abs(audio_data)) > 500:  # Cek apakah ada suara (bukan noise kosong)
            print(f"✅ Microphone pada device {device_index} berfungsi dengan baik!\n")
            return True  # Mikrofon berfungsi
        else:
            print(f"❌ Microphone pada device {device_index} tidak menangkap suara.\n")
            return False  # Mikrofon tidak menangkap suara
    
    except Exception as e:
        print(f"❌ Gagal membuka device {device_index}: {e}\n")
        return False  # Mikrofon gagal dibuka

# Fungsi untuk mencari perangkat audio yang valid dan berfungsi
def get_valid_audio_device():
    audio = pyaudio.PyAudio()
    valid_devices = []

    # Cek semua perangkat yang memiliki input channel
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0:
            valid_devices.append(i)

    audio.terminate()

    if not valid_devices:
        print("❌ Tidak ada perangkat audio yang tersedia untuk merekam!")
        return None

    print(f"✅ Ditemukan {len(valid_devices)} perangkat audio dengan input channels.")
    print("Menguji perangkat-perangkat audio yang ditemukan...\n")

    # Tes semua perangkat yang ditemukan secara otomatis
    for device_index in valid_devices:
        if test_microphone(device_index):  # Jika perangkat berfungsi, pilih
            print(f"🎤 Perangkat {device_index} dipilih sebagai mikrofon default.")
            return device_index

    print("❌ Tidak ada perangkat yang berfungsi. Menggunakan perangkat default sistem.")
    return None  # Jika tidak ada perangkat yang valid, kembalikan None

# Fungsi untuk merekam video dan audio tanpa menampilkan frame dan tanpa perlu menekan tombol 'q'
def record_video_with_audio(duration):
    audio_device = get_valid_audio_device()
    if not audio_device:
        return None

    audio_frames = []

    def record_audio():
        samplerate = 44100
        channels = 2
        print("🎤 Merekam audio...")

        with sd.InputStream(device=audio_device, samplerate=samplerate, channels=channels, dtype=np.int16) as stream:
            audio_data = stream.read(int(samplerate * duration))[0]
            audio_frames.append(audio_data)

        # Simpan audio ke file WAV
        with wave.open(AUDIO_FILENAME, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(np.array(audio_frames).tobytes())

    # === REKAM VIDEO ===
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(VIDEO_FILENAME, fourcc, 20.0, (640, 480))

    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()

    print("📹 Merekam video...")

    # Lakukan perekaman tanpa menampilkan frame dan tanpa tombol untuk berhenti
    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    # Hapus jendela tampilan (tidak diperlukan)
    cv2.destroyAllWindows()

    audio_thread.join()

    # === GABUNG VIDEO & AUDIO DENGAN FFMPEG ===
    print("🔄 Menggabungkan video dan audio...")
    ffmpeg_cmd = [
        FFMPEG_PATH, "-y",
        "-i", VIDEO_FILENAME,
        "-i", AUDIO_FILENAME,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-strict", "experimental",
        "-shortest",  # Opsi untuk menyesuaikan panjang file audio/video
        OUTPUT_FILENAME
    ]

    subprocess.run(ffmpeg_cmd)

    # === HAPUS FILE SEMENTARA ===
    os.remove(VIDEO_FILENAME)
    os.remove(AUDIO_FILENAME)

    print(f"✅ Rekaman selesai! Simpan sebagai {OUTPUT_FILENAME}")
    return OUTPUT_FILENAME

# Fungsi untuk merekam audio saja
def record_audio_only(duration):
    audio_device = get_valid_audio_device()
    if not audio_device:
        return None

    audio_frames = []
    samplerate = 44100
    channels = 2
    print("🎤 Merekam audio dimulai...")

    with sd.InputStream(device=audio_device, samplerate=samplerate, channels=channels, dtype=np.int16) as stream:
        audio_data = stream.read(int(samplerate * duration))[0]
        audio_frames.append(audio_data)

    # Simpan audio ke file WAV
    with wave.open(AUDIO_FILENAME, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(np.array(audio_frames).tobytes())

    print("🎤 Merekam audio selesai...")
    return AUDIO_FILENAME
