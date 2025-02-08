import cv2
import numpy as np
import websocket
import base64
import time
import threading
import pyautogui

# Flag untuk menghentikan thread
stop_event = threading.Event()

def capture_screen():
    """Fungsi untuk menangkap layar secara real-time"""
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)  
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  
    return screenshot

def send_frame(ws, frame):
    """Fungsi untuk mengirim frame gambar ke server menggunakan WebSocket"""
    try:
        frame = cv2.resize(frame, (1280, 720))
        _, img_bytes = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])  
        base64_str = base64.b64encode(img_bytes).decode('utf-8')  
        ws.send(base64_str)  
    except Exception as e:
        print(f"Error sending frame: {e}")

def capture_and_send(ws):
    """Fungsi untuk menangkap layar dan mengirimkan frame secara real-time"""
    while not stop_event.is_set():  # Periksa apakah ada permintaan untuk berhenti
        try:
            start_time = time.time()
            frame = capture_screen()
            send_frame(ws, frame)
            elapsed_time = time.time() - start_time
            sleep_time = max(0.1 - elapsed_time, 0)
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error in capture_and_send: {e}")
            break

def start_screen_capture(ws_url):
    """Fungsi untuk memulai pengambilan dan pengiriman video layar ke server"""
    global ws
    while not stop_event.is_set():
        try:
            ws = websocket.create_connection(ws_url)
            capture_thread = threading.Thread(target=capture_and_send, args=(ws,))
            capture_thread.daemon = True
            capture_thread.start()
            capture_thread.join()  
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            time.sleep(5)  

def stop_screen_capture():
    """Fungsi untuk menghentikan screen sharing"""
    global ws
    stop_event.set()  # Set event untuk menghentikan loop
    try:
        if ws:
            ws.close()  # Tutup koneksi WebSocket
            print("WebSocket connection closed.")
    except Exception as e:
        print(f"Error closing WebSocket: {e}")
