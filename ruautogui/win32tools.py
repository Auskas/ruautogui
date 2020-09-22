
import ctypes
from ctypes import wintypes
import time
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