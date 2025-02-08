import pyautogui
import io
import cv2
from PIL import Image

def capture_screen():
    screenshot = pyautogui.screenshot()  # Mengambil screenshot
    img_byte_array = io.BytesIO()  # Tempat untuk menyimpan gambar dalam format byte
    screenshot.save(img_byte_array, format='PNG')  # Simpan screenshot ke byte array
    img_byte_array.seek(0)  # Pindahkan pointer ke awal byte array
    return img_byte_array  # Mengembalikan byte array screenshot

def capture_webcam():
    cap = cv2.VideoCapture(0)  # Buka webcam (0 untuk default webcam)
    if not cap.isOpened():
        print("Error: Webcam tidak dapat diakses.")
        return None
    
    ret, frame = cap.read()  # Ambil satu frame dari webcam
    cap.release()  # Tutup koneksi ke webcam
    
    if not ret:
        print("Error: Gagal mengambil gambar dari webcam.")
        return None
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Konversi dari BGR (OpenCV) ke RGB (PIL)
    pil_image = Image.fromarray(img)  # Konversi ke format PIL
    
    img_byte_array = io.BytesIO()
    pil_image.save(img_byte_array, format='PNG')  # Simpan sebagai PNG ke byte array
    img_byte_array.seek(0)
    
    return img_byte_array  # Mengembalikan byte array gambar webcam

def handle_capture(command):
    if command == "desktop":
        return capture_screen()
    elif command == "webcam":
        return capture_webcam()
    else:
        print("Error: Perintah tidak dikenali.")
        return None
