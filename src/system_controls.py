import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyttsx3

def get_system_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMasterVolumeLevelScalar()

def set_system_volume(volume_level):  # 0.0 - 1.0 (0% - 100%)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_level, None)

def say_text(text):
    engine = pyttsx3.init()
    # Dapatkan daftar suara yang tersedia
    voices = engine.getProperty('voices')
    
    # Pilih suara wanita (biasanya suara wanita berada di indeks 1)
    engine.setProperty('voice', voices[1].id)
    original_volume = get_system_volume()  # Simpan volume awal
    set_system_volume(0.9)  # Atur volume ke 80%
    
    engine.say(text)
    engine.runAndWait()
    
    set_system_volume(original_volume)  # Kembalikan volume ke awal
    
def shutdown():
    os.system("shutdown /s /t 0")

def restart():
    os.system("shutdown /r /t 0")

def hibernate():
    os.system("shutdown /h")

def lock_computer():
    os.system("rundll32.exe user32.dll,LockWorkStation")

