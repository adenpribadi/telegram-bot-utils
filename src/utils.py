import os
import sys

def read_tokens_from_file(filename):
    tokens = {}
    # Cek apakah sedang berjalan sebagai exe
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Path sementara untuk PyInstaller
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))  # Path asli jika berjalan sebagai skrip Python

    file_path = os.path.join(base_path, filename)

    try:
        with open(file_path, "r") as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=')
                    tokens[key] = value
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan.")
    return tokens
