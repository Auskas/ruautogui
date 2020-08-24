# -*- coding: utf-8 -*-
#
# keyboard.py - a module from ruautogui package that simulates human-like 
#               typing.
# Features:
#   - simulates typing by using the so-called virtual keys;
#   - cyrillic (russian) alphabet is supported;
#   - tuned typing speed;
#   - hotkeys are supported.

import sys

if sys.platform == 'win32':
    import os
    import logging
    import ctypes
    from ctypes import wintypes
    import time, random
    if __name__ == '__main__':
        import win32tools
    else:
        from ruautogui import win32tools
else:
    raise Exception('Currently supports only Windows OS!')

logger = logging.getLogger('ruautogui.keyboard')
logger.setLevel(logging.DEBUG)

logConsoleHandler = logging.StreamHandler()
formatterConsole = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logConsoleHandler.setFormatter(formatterConsole)
logger.addHandler(logConsoleHandler)

logFileHandler = logging.FileHandler(f'ruautogui.log')
formatterFile = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logFileHandler.setFormatter(formatterFile)
logger.addHandler(logFileHandler)    

KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002

wintypes.ULONG_PTR = wintypes.WPARAM

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

# The following two constants indicate a hotkey that changes the keyboard layout
# in the system. Replace them in accordance with the 'mapping' dictionary keys 
# below if your hotkey differs.
CHANGE_KEYBOARD_LAYOUT_KEY1 = 'leftalt'
CHANGE_KEYBOARD_LAYOUT_KEY2 = 'shift'


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

user32 = ctypes.WinDLL('user32', use_last_error=True)

# The following dictionary is used to set the average typing speed.
# The keys of the dictionary are the names of the modes.
# 'min' and 'max' determine the minimum and maximum delay before the next
# symbol in the string will be typed.
# 'typorate' is used to set the number of typos per symbols typed:
#       for instance, typorate of 20 means that for every 20 symbols in average
#       there will be a typo (typos are not allowed by default,
#                             all the typos will be corrected automatically).
modes = {
    'ultraslow' : {'min': 0.9, 'max': 3, 'typorate': 10},
    'slow' : {'min': 0.4, 'max': 0.9, 'typorate': 20},
    'standard': {'min': 0.15, 'max': 0.4, 'typorate': 20},
    'fast': {'min': 0.08, 'max': 0.15, 'typorate': 20},
    'ultrafast': {'min': 0.01, 'max': 0.05, 'typorate': 30},
    'instant': {'min': 0, 'max': 0, 'typorate': False}
}

# The following dictionary is used to map a symbol or a button of a typical
# keyboard to its virtual-key code.
mapping = {
    "leftmousebutton": 0x01, #VK_LBUTTON
    "rightmousebutton": 0x02, #VK_RBUTTON
    "controlbreak": 0x03, #VK_CANCEL
    "middlemousebutton": 0x04, #VK_MBUTTON
    "x1mousebutton": 0x05, #VK_XBUTTON1
    "x2mousebutton": 0x06, #VK_XBUTTON1
    "backspace": 0x08, #VK_BACK
    "tab": 0x09, #VK_TAB
    "clear": 0x0C, #VK_CLEAR
    "enter": 0x0D, #VK_RETURN
    "shift": 0x10, #VK_SHIFT
    "ctrl": 0x11, #VK_CONTROL
    "alt": 0x12, #VK_MENU
    "pause": 0x13, #VK_PAUSE
    "capslock": 0x14, #VK_CAPITAL
    "esc": 0x1B, #VK_ESCAPE
    "escape": 0x1B, #VK_ESCAPE
    "spacebar": 0x20, #VK_SPACE
    "space": 0x20, #VK_SPACE
    " ": 0x20, #VK_SPACE
    "pageup": 0x21, #VK_PRIOR
    "pagedown": 0x22, #VK_NEXT
    "end": 0x23, #VK_END
    "home": 0x24, #VK_HOME
    "left": 0x25, #VK_LEFT
    "up": 0x26, #VK_UP
    "right": 0x27, #VK_RIGHT
    "down": 0x28, #VK_DOWN
    "select": 0x29, #VK_SELECT
    "print": 0x2A, #VK_PRINT
    "execute": 0x2B, #VK_EXECUTE
    "printscreen": 0x2C, #VK_SNAPSHOT
    "insert": 0x2D, #VK_INSERT
    "delete": 0x2E, #VK_DELETE
    "help": 0x2F, #VK_HELP
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
    "a": 0x41,
    "b": 0x42,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "f": 0x46,
    "g": 0x47,
    "h": 0x48,
    "i": 0x49,
    "j": 0x4A,
    "k": 0x4B,
    "l": 0x4C,
    "m": 0x4D,
    "n": 0x4E,
    "o": 0x4F,
    "p": 0x50,
    "q": 0x51,
    "r": 0x52,
    "s": 0x53,
    "t": 0x54,
    "u": 0x55,
    "v": 0x56,
    "w": 0x57,
    "x": 0x58,
    "y": 0x59,
    "z": 0x5A,
    "leftwindow": 0x5B, #VK_LWIN
    "rightwindow": 0x5C, #VK_RWIN
    "applications": 0x5D, #VK_APPS
    "sleep": 0x5F, #VK_SLEEP
    "numpad0": 0x60, #VK_NUMPAD0
    "numpad1": 0x61, #VK_NUMPAD1
    "numpad2": 0x62, #VK_NUMPAD2
    "numpad3": 0x63, #VK_NUMPAD3
    "numpad4": 0x64, #VK_NUMPAD4
    "numpad5": 0x65, #VK_NUMPAD5
    "numpad6": 0x66, #VK_NUMPAD6
    "numpad7": 0x67, #VK_NUMPAD7
    "numpad8": 0x68, #VK_NUMPAD8
    "numpad9": 0x69, #VK_NUMPAD9
    "*": 0x6A, #VK_MULTIPLY
    "+": 0x6B, #VK_ADD
    "-": 0x6D, #VK_SUBTRACT
    ".": 0x6E, #VK_DECIMAL
    "/": 0x6F, #VK_DIVIDE
    "f1": 0x70, #VK_F1
    "f2": 0x71, #VK_F2
    "f3": 0x72, #VK_F3
    "f4": 0x73, #VK_F4
    "f5": 0x74, #VK_F5
    "f6": 0x75, #VK_F6
    "f7": 0x76, #VK_F7
    "f8": 0x77, #VK_F8
    "f9": 0x78, #VK_F9
    "f10": 0x79, #VK_F10
    "f11": 0x7A, #VK_F11
    "f12": 0x7B, #VK_F12
    "numlock": 0x90, #VK_NUMLOCK
    "scrolllock": 0x91, #VK_SCROLL
    "leftshift": 0xA0, #VK_LSHIFT
    "rightshift": 0xA1, #VK_RSHIFT
    "leftctrl": 0xA2, #VK_LCONTROL
    "rightctrl": 0xA3, #VK_RCONTROL
    "leftalt": 0xA4, #VK_LMENU
    "rightalt": 0xA5, #VK_RMENU
    "browserback": 0xA6, #VK_BROWSER_BACK
    "browserforward": 0xA7, #VK_BROWSER_FORWARD
    "browserrefresh": 0xA8, #VK_BROWSER_REFRESH
    "browserstop": 0xA9, #VK_BROWSER_STOP
    "browsersearch": 0xAA, #VK_BROWSER_SEARCH
    "browserfavorites": 0xAB, #VK_BROWSER_FAVORITES
    "browserhome": 0xAC, #VK_BROWSER_HOME
    "volumemute": 0xAD, #VK_VOLUME_MUTE
    "volumedown": 0xAE, #VK_VOLUME_DOWN
    "volumeup": 0xAF, #VK_VOLUME_UP
    "nexttrack": 0xB0, #VK_MEDIA_NEXT_TRACK
    "previoustrack": 0xB1, #VK_MEDIA_PREV_TRACK
    "mediastop": 0xB2, #VK_MEDIA_STOP
    "mediaplay": 0xB3, #VK_MEDIA_PLAY_PAUSE
    "mail": 0xB4, #VK_LAUNCH_MAIL
    "selectmedia": 0xB5, #VK_LAUNCH_MEDIA_SELECT
    "app1": 0xB6, #VK_LAUNCH_APP1
    "app2": 0xB7, #VK_LAUNCH_APP2
    ";": 0xBA, #VK_OEM_1
    "=": 0xBB, #VK_OEM_PLUS
    ",": 0xBC, #VK_OEM_COMMA
    "-": 0xBD, #VK_OEM_MINUS
    ".": 0xBE, #VK_OEM_PERIOD
    "/": 0xBF, #VK_OEM_2
    "`": 0xC0, #VK_OEM_3
    "[": 0xDB, #VK_OEM_4
    "\\": 0xDC, #VK_OEM_5
    "]": 0xDD, #VK_OEM_6
    "'": 0xDE, #VK_OEM_7

    '"': 0xDE, #VK_OEM_7
    "~": 0xC0, #VK_OEM_3
    "!": 0x31,
    "@": 0x32,
    "#": 0x33,
    "$": 0x34,
    "%": 0x35,
    "^": 0x36,
    "&": 0x37,
    "*": 0x38,
    "(": 0x39,
    ")": 0x30,
    "_": 0xBD, #VK_OEM_MINUS
    "+": 0xBB, #VK_OEM_PLUS
    "{": 0xDB, #VK_OEM_4
    "}": 0xDD, #VK_OEM_6
    "|": 0xDC, #VK_OEM_5
    ":": 0xBA, #VK_OEM_1
    "<": 0xBC, #VK_OEM_COMMA
    ">": 0xBE, #VK_OEM_PERIOD
    "?": 0xBF, #VK_OEM_2
}

# The following dictionary is used to determine which characters require
# the shift key to be typed. It overlapses with the main mapping dictionary.
shift_mapping = {
    '"': 0xDE, #VK_OEM_7
    "~": 0xC0, #VK_OEM_3
    "!": 0x31,
    "@": 0x32,
    "#": 0x33,
    "$": 0x34,
    "%": 0x35,
    "^": 0x36,
    "&": 0x37,
    "*": 0x38,
    "(": 0x39,
    ")": 0x30,
    "_": 0xBD, #VK_OEM_MINUS
    "+": 0xBB, #VK_OEM_PLUS
    "{": 0xDB, #VK_OEM_4
    "}": 0xDD, #VK_OEM_6
    "|": 0xDC, #VK_OEM_5
    ":": 0xBA, #VK_OEM_1
    "<": 0xBC, #VK_OEM_COMMA
    ">": 0xBE, #VK_OEM_PERIOD
    "?": 0xBF, #VK_OEM_2
}

# The following dictionary enable the cyrillic support.
# It maps a cyrillic character to its english character or symbol 
# in the ordinary keyboard.
# (there is no such thing as cyrillic virtual-key codes)
ru_mapping = {
    'а': 'f', 
    'б': ',',
    'в': 'd', 
    'г': 'u',
    'д': 'l', 
    'е': 't',
    'ё': '`', 
    'ж': ';', 
    'з': 'p', 
    'и': 'b', 
    'й': 'q', 
    'к': 'r', 
    'л': 'k',
    'м': 'v', 
    'н': 'y',
    'о': 'j', 
    'п': 'g', 
    'р': 'h',
    'с': 'c',
    'т': 'n', 
    'у': 'e',
    'ф': 'a', 
    'х': '[',
    'ц': 'w', 
    'ч': 'x', 
    'ш': 'i', 
    'щ': 'o',
    'ь': 'm', 
    'ъ': ']', 
    'ы': 's', 
    'э': "'", 
    'ю': '.', 
    'я': 'z',
    ' ': ' '
}

def get_keyboard_layout(thread_id=0):
    """ Returns the keyboard layout of the foreground window as a string:
        'russian', 'english' or 'unknown'"""
    current_window = ctypes.windll.user32.GetForegroundWindow()
    if thread_id == 0: 
        thread_id = ctypes.windll.user32.GetWindowThreadProcessId(current_window, 0) 
    # keyboard_language_id made up of 0xAAABBBB, where 
    # AAA = HKL (handle object), BBBB = language ID
    keyboard_language_id = ctypes.windll.user32.GetKeyboardLayout(thread_id)
    # Language ID -> low 10 bits, Sub-language ID -> high 6 bits
    language_id = keyboard_language_id & (2**16 - 1)
    # Convert language ID from decimal to hexadecimal
    language_id_hex = hex(language_id)
    if '409' in language_id_hex:
        return 'english'
    elif '419' in language_id_hex:
        return 'russian'
    else:
        return 'unknown'

def change_keyboard_layout(thread_id=0, language='russian'):
    """ This function gets:
            thread_id - an integer (default = 0) - the thread to switch the 
                        target language on;
            language - a string (default = 'russian') - the target language 
                        to switch on.
        
        This function returns None.

        Changes the keyboard layout language by simulating the press of the 
        default hotkey. The number of attemps equals to five: 
        if the target language is found, stops its attemps."""

    trials = 5
    while get_keyboard_layout() != language:
        hotkey(CHANGE_KEYBOARD_LAYOUT_KEY1, CHANGE_KEYBOARD_LAYOUT_KEY2)
        logger.debug(f'Switched to {get_keyboard_layout(thread_id)} keyboard layout')
        trials -= 1
        time.sleep(0.1)
        if trials == 0:
            raise Exception('Cannot get the target keyboard layout.')

def hotkey(*args, **kwargs):
    """ This function gets:
    *args - strings of keys that form a hotkey;
    **kwargs - actually are not used here.

This function return None.

Simulates the press of a hotkey by pressing the passed keys one by one
and releasing them in the reverse order.
Any number of keys can be passed as the arguments."""

    interval = float(kwargs.get("interval", 0.0))
    for key in args:
        if len(key) > 1:
            key = key.lower()
        ctypes.windll.user32.keybd_event(mapping[key], 0, KEYEVENTF_KEYDOWN, 0)
        time.sleep(interval)
    for key in reversed(args):
        if len(key) > 1:
            key = key.lower()
        ctypes.windll.user32.keybd_event(mapping[key], 0, KEYEVENTF_KEYUP, 0)
        time.sleep(interval)

def type(message, mode='standard', typo=False):
    """This function gets:
    message - a string of symbols to type in;
    mode - a string of the name of the typing mode;
    typo - a bollean - True if typos are allowed, False if are not.
                       (all the typos will be corrected).

This function returns None."""

    if isinstance(message, str) == False:
        raise Exception('The message is not a string')
    if mode not in modes.keys():
        mode = 'standard'
    if isinstance(typo, bool) == False:
        typo=False

    if typo:
        typorate = modes[mode]['typorate']

    for i in range(len(message)):

        if message[i] in shift_mapping.keys():
            symbol = message[i]
            shift = True
            if get_keyboard_layout() != 'english':
                change_keyboard_layout(language='english')

        elif message[i].lower() in ru_mapping.keys():
            symbol = ru_mapping[message[i].lower()]
            if message[i] in ru_mapping.keys():
                shift = False
            else:
                shift = True
            if get_keyboard_layout() != 'russian':
                change_keyboard_layout()

        elif message[i].lower() in mapping.keys():
            symbol = message[i].lower()
            if message[i] in mapping.keys():
                shift = False
            else:
                shift = True
            if get_keyboard_layout() != 'english':
                change_keyboard_layout(language='english')

        else:
            logger.error(f'Symbol "{symbol}" not found in virtual keys! Skipping...')
            continue
        if typo and random.randint(0, typorate) > typorate - 1:
            logger.debug('Let\'s make a typo!')
            random_symbol = ru_mapping[random.choice(list(ru_mapping.keys()))]

            press(random_symbol, mode)
            time.sleep(random.uniform(modes[mode]['min'] * 3, modes[mode]['max'] * 3))

            press('backspace', mode)

        press(symbol, mode, shift=shift)         

def press(symbol, mode='standard', shift=False):
    """This function gets:
    symbol - a string of a symbol to be pressed;
    mode - a string of the name of typing mode;
    shift - a boolean - if True the shift key will be pressed along with 
                        the symbol.

This function returns None."""

    if shift:
        x = INPUT(type=INPUT_KEYBOARD, 
                  ki=KEYBDINPUT(wVk=mapping['shift'])
            )
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

    x = INPUT(type=INPUT_KEYBOARD, 
              ki=KEYBDINPUT(wVk=mapping[symbol])
              )
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    
    x = INPUT(type=INPUT_KEYBOARD, 
              ki=KEYBDINPUT(wVk=mapping[symbol], dwFlags=KEYEVENTF_KEYUP)
              )
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    time.sleep(random.uniform(modes[mode]['min'], modes[mode]['max']))

    if shift:
        x = INPUT(type=INPUT_KEYBOARD, 
                  ki=KEYBDINPUT(wVk=mapping['shift'], dwFlags=KEYEVENTF_KEYUP)
                  )
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

    time.sleep(random.uniform(modes[mode]['min'], modes[mode]['max']))

if __name__ == '__main__':
    message = 'ПРЕИМУЩЕСТВЕННО равноценные БОЙКОТЫ грандиозных событий. Ещё желаемые запретные категории стандартных упрощённых целей. Въезд и льготы на парашюты.'
    message2 = 'ёйцукенгшщзхъфывапролджэячсмитьбю.ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ.`1234567890-=qwertyuiop[]asdfghjkl;zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?\\|/'
    message3 = 'QWERTY'
    #hotkey('leftalt', 'shift')
    time.sleep(4)
    type(message, mode='ultrafast', typo=True)