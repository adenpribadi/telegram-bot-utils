import telebot
import time
import psutil

import os
import platform
import getpass
import threading
import requests

from flask import Flask, jsonify
from src.records import record_audio_only, record_video_with_audio
from src.capture import handle_capture
from src.system_controls import shutdown, restart, hibernate, say_text, lock_computer
from src.screen_capture import start_screen_capture, stop_screen_capture
from src.deepseek import ask_question
from src.utils import read_tokens_from_file

config_tokens = read_tokens_from_file("config.txt")
IP_SERVER = config_tokens.get("IP_SERVER")

if not IP_SERVER:
    raise ValueError("IP_SERVER tidak ditemukan dalam file config.txt")

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(commands=['shutdown'])
        def handle_shutdown(message):
            # Mengucapkan pesan pemberitahuan
            say_text("Your laptop will shut down in 5 seconds...")  # Memberi tahu dalam bahasa Inggris
            
            # Kirim pesan ke chat Telegram tentang countdown
            self.bot.reply_to(message, "Your laptop will shut down in 5 seconds...")
            
            # Countdown 5 detik
            for i in range(5, 0, -1):
                say_text(f"{i} ")
                # self.bot.send_message(message.chat.id, f"{i} seconds remaining...")
                time.sleep(1)  # Tunggu 1 detik di setiap iterasi
            
            # Setelah countdown selesai, matikan laptop
            shutdown()
            self.bot.reply_to(message, "Laptop is shutting down now!")

        @self.bot.message_handler(commands=['restart'])
        def handle_restart(message):
            say_text("Your laptop will restart in 5 seconds...")
            self.bot.reply_to(message, "Your laptop will restart in 5 seconds...")

            for i in range(5, 0, -1):
                say_text(f"{i} ")
                time.sleep(1)  # Tunggu 1 detik di setiap iterasi

            restart()
            self.bot.reply_to(message, "Laptop is restart now!")

        @self.bot.message_handler(commands=['hibernate'])
        def handle_hibernate(message):
            hibernate()
            self.bot.reply_to(message, "Laptop akan masuk mode hibernate!")

        @self.bot.message_handler(commands=['lock'])
        def handle_lock(message):
            lock_computer()  # Panggil fungsi untuk mengunci komputer
            self.bot.reply_to(message, "Your computer has been locked!")

        @self.bot.message_handler(commands=['say'])
        def handle_say(message):
            text_to_say = message.text.replace('/say ', '', 1)
            if text_to_say.strip():
                say_text(text_to_say)
                self.bot.reply_to(message, f"Mengucapkan: {text_to_say}")
            else:
                self.bot.reply_to(message, "Silakan masukkan teks setelah /say")

        @self.bot.message_handler(commands=['ask'])
        def handle_ask(message):
            ask_text = message.text.replace('/ask ', '', 1)
            if ask_text.strip():
                answer_ai = ask_question(ask_text)
                self.bot.reply_to(message, f"Mengucapkan: {answer_ai}")
            else:
                self.bot.reply_to(message, "Silakan masukkan teks setelah /ask")

        @self.bot.message_handler(commands=['capture'])
        def handle_capture_command(message):
            command_parts = message.text.split()  # Pisahkan perintah berdasarkan spasi
            if len(command_parts) < 2:
                self.bot.reply_to(message, "Gunakan format: /capture desktop atau /capture webcam")
                return

            command = command_parts[1].lower()  # Ambil argumen kedua dan ubah ke huruf kecil
            screenshot_file = handle_capture(command)  # Panggil fungsi handle_capture dengan parameter

            if screenshot_file is None:
                self.bot.reply_to(message, "Gagal mengambil gambar. Pastikan perintah benar.")
                return

            self.bot.send_photo(message.chat.id, screenshot_file)
            self.bot.reply_to(message, f"Gambar dari {command} telah diambil dan dikirim!")

        @self.bot.message_handler(commands=['records'])
        def handle_records_command(message):
            command_parts = message.text.split()  # Pisahkan perintah berdasarkan spasi
            if len(command_parts) < 2:
                self.bot.reply_to(message, "Gunakan format: /records webcam <durasi> atau /capture microphone <durasi>")
                return

            command = command_parts[1].lower()  # Ambil argumen kedua dan ubah ke huruf kecil
            
            # Periksa jika ada argumen durasi
            if len(command_parts) >= 3:
                try:
                    duration = int(command_parts[2])  # Ambil durasi dari teks
                except ValueError:
                    duration = 5  # Jika tidak valid, set durasi ke 5 detik
            else:
                duration = 5  # Set durasi default ke 5 detik jika tidak ada argumen durasi

            if command == "webcam":
                records_file = record_video_with_audio(duration)  # Panggil fungsi record_video dengan parameter

                if records_file is None:
                    self.bot.reply_to(message, "Gagal mengambil gambar. Pastikan perintah benar.")
                    return

                # Kirim video ke Telegram
                with open(records_file, 'rb') as video_file:
                    self.bot.send_video(message.chat.id, video_file)

                self.bot.reply_to(message, f"Video dari {command} telah diambil dan dikirim!")

            elif command == "microphone":
                record_file = record_audio_only(duration)  # Menggunakan fungsi yang benar untuk merekam audio
                if record_file is None:
                    self.bot.reply_to(message, "Gagal merekam audio. Pastikan perintah benar.")
                    return

                # Kirim Audio ke Telegram
                with open(record_file, 'rb') as audio_file:
                    self.bot.send_audio(message.chat.id, audio_file)

                self.bot.reply_to(message, f"Audio dari {command} telah diambil dan dikirim!")
            else:
                response = "Perintah tidak valid"
                self.bot.reply_to(message, response, parse_mode="Markdown")


        @self.bot.message_handler(commands=['battery'])
        def handle_battery(message):
            battery = psutil.sensors_battery()
            percent = battery.percent
            charging = "🔌 Charging" if battery.power_plugged else "🔋 Not Charging"
            time_left = f"{battery.secsleft // 60} minutes left" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "N/A"

            response = f"🔋 Battery: {percent}%\n⚡ Status: {charging}\n⏳ Time Left: {time_left}"
            self.bot.reply_to(message, response)

        @self.bot.message_handler(commands=['cpu'])
        def handle_cpu(message):
            cpu_usage = psutil.cpu_percent(interval=1)
            self.bot.reply_to(message, f"🖥 CPU Usage: {cpu_usage}%")

        @self.bot.message_handler(commands=['ram'])
        def handle_ram(message):
            ram = psutil.virtual_memory()
            self.bot.reply_to(message, f"💾 RAM Usage: {ram.percent}%")

        @self.bot.message_handler(commands=['ip'])
        def handle_ip(message):
            ip_address = requests.get('https://api64.ipify.org?format=json').json()["ip"]
            self.bot.reply_to(message, f"🌍 Public IP Address: `{ip_address}`")

        @self.bot.message_handler(commands=['whoami'])
        def handle_whoami(message):
            username = getpass.getuser()
            hostname = platform.node()
            os_name = platform.system()
            os_version = platform.version()

            reply = f"👤 **User Info:**\n🖥 Username: {username}\n🏠 Hostname: {hostname}\n💻 OS: {os_name} {os_version}"
            self.bot.reply_to(message, reply)

        @self.bot.message_handler(commands=['sharescreen'])
        def share_screen(message):
            try:
                command = message.text.split(" ", 1)  # Pisahkan perintah dari argumen (start/stop)
    
                if len(command) < 2:
                    self.bot.reply_to(message, "Gunakan: `/sharescreen start` atau `/sharescreen stop`", parse_mode="Markdown")
                    return

                action = command[1].strip().lower()
                
                if action == "start":
                    # Mulai proses berbagi layar
                    self.bot.reply_to(message, f"Berbagi layar telah dimulai http://{IP_SERVER}:5001", parse_mode="Markdown")
                    print(f"Berbagi layar telah dimulai!")
                    
                    start_screen_capture(ws_url=f"ws://{IP_SERVER}:5000")  # Ganti dengan URL server WebSocket Anda
                elif action == "stop":
                    stop_screen_capture()
                    self.bot.reply_to(message, "Berbagi layar telah berhenti", parse_mode="Markdown")
                else:
                    response = "Perintah tidak valid. Gunakan: `/sharescreen start` atau `/sharescreen stop`"
                    self.bot.reply_to(message, response, parse_mode="Markdown")

            except Exception as e:
                print(f"Error saat memulai berbagi layar: {e}")
                self.bot.send_message(message.chat.id, "Gagal memulai berbagi layar. Coba lagi nanti.")

    def start(self):
        self.bot.infinity_polling()
