
import ctypes
from ctypes import wintypes
import time
import pyautogui

from ctypes import POINTER

KLF_ACTIVATE = 0x00000001
KLF_SETFORPROCESS = 0x00000100

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

def get_mouse_cursor_position():
    cursor = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return (cursor.x, cursor.y)

def get_screen_size():
    return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

def get_left_button_state():
    return ctypes.windll.user32.GetKeyState(0x01)

def get_keyboard_layout(thread_id):
    #print(ctypes.windll.user32.GetKeyboardLayoutList(5, 0x0000))
    # Made up of 0xAAABBBB, AAA = HKL (handle object) & BBBB = language ID
    klid = ctypes.windll.user32.GetKeyboardLayout(thread_id)
    # Language ID -> low 10 bits, Sub-language ID -> high 6 bits
    # Extract language ID from KLID
    lid = klid & (2**16 - 1)
    # Convert language ID from decimal to hexadecimal
    lid_hex = hex(lid)
    #print(klid, lid, lid_hex)
    if '409' in lid_hex:
        return 'English'
    elif '419' in lid_hex:
        return 'Russian'
    else:
        return 'Unknown'

def rus_keyboard_layout(tid):
    locale_id_bytes = b"00000419"
    klid = ctypes.create_string_buffer(locale_id_bytes)
    user32_dll = ctypes.WinDLL("user32")
    kernel32_dll = ctypes.WinDLL("kernel32")
    LoadKeyboardLayout = user32_dll.LoadKeyboardLayoutA
    LoadKeyboardLayout.argtypes = [wintypes.LPCSTR, wintypes.UINT]
    LoadKeyboardLayout.restype = wintypes.HKL
    GetLastError = kernel32_dll.GetLastError
    GetLastError.restype = wintypes.DWORD
    klh = LoadKeyboardLayout(klid, 0x00000002)
    print("{} returned: {}".format(LoadKeyboardLayout.__name__, hex(klh)))
    print("{} returned: {}".format(GetLastError.__name__, GetLastError()))

def change_keyboard_layout(thread_id):
    while get_keyboard_layout(thread_id) != 'Russian':
        pyautogui.hotkey('alt', 'shift')
        print(f'Switched to {get_keyboard_layout(thread_id)} keyboard layout')
        time.sleep(2)

if __name__ =='__main__':
    #get_keyboard_layout(0)
    change_keyboard_layout(0)