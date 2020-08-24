# -*- coding: utf-8 -*-
#
# mouse.py - a module from ruautogui package that simulates human-like mouse
#            movements.
# Features:
#   - simulates a random mouse movement when a user grabs the mouse controller;
#   - moves the mouse controller through the passed coordinates (Bezier curve);
#   - clicks any mouse buttons at the current location 
#     (double-clicks are allowed).

import sys

import logging
logger = logging.getLogger('ruautogui.mouse')
logger.setLevel(logging.DEBUG)

logConsoleHandler = logging.StreamHandler()
formatterConsole = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logConsoleHandler.setFormatter(formatterConsole)
logger.addHandler(logConsoleHandler)

logFileHandler = logging.FileHandler(f'ruautogui.log')
formatterFile = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logFileHandler.setFormatter(formatterFile)
logger.addHandler(logFileHandler)   

if sys.platform == 'win32':
    import os
    import ctypes
    from ctypes import wintypes
    if __name__ == '__main__':
        import win32tools, bezier
    else:
        from ruautogui import win32tools, bezier
else:
    raise Exception('Currently supports only Windows OS!')
    sys.exit()

MINIMUM_SLEEP_TIME = 0.013

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040

wintypes.ULONG_PTR = wintypes.WPARAM

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

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

def grab():
    """ This function is used to create a tuple of coordinates to simulate
a random mouse movement when a user grabs the mouse controller.
Calls the function 'move' and passes the obtained random coordinates and the 
transition time to it.
"""
    transition_time = random.randint(95, 145)
    random_angle_rad = random.uniform(0, 2 * math.pi)
    distance = random.randint(15,50)
    begin_pos = win32tools.get_mouse_cursor_position()
    distanse_x = distance * math.cos(random_angle_rad)
    distance_y = distance * math.sin(random_angle_rad)
    end_pos = (int(begin_pos[0] + distanse_x), int(begin_pos[1] + distance_y))
    order = random.randint(1,5)
    points, _, _ = bezier.get_curve_points(
        begin_pos=begin_pos, 
        end_pos=end_pos, 
        order=order, 
        control_points=[], 
        transition_time=transition_time
    )
    move_through_coordinates(points, transition_time)

def move(end_pos, order=2, transition_time=None):
    """ This function is used to generate the points on the Bezier curve,
as well as a random transition time and to call the 'move_through_coordinates'
function to move the mouse cursor through the points.

This function gets the following arguments:
    end_pos - a tuple of x and y coordinates of the target point.
    order - an integer (default = 3) the order of the Bezier Curve
            (if the order less or equal to 1 the resulting curve is
            a straight line).
    transition_time an integer (default = None) - milliseconds of the
            transition time of the movement. If None, the transition
            time will be chosen randomily.

This function returns None."""

    if len(end_pos) == 0:
        return None
    begin_pos = win32tools.get_mouse_cursor_position()
    points, _, transition_time_random = bezier.get_curve_points(
        begin_pos=begin_pos, 
        end_pos=end_pos, 
        order=order, 
        control_points=[], 
        transition_time=transition_time
    )
    if transition_time == None:
        transition_time = transition_time_random
    move_through_coordinates(points, transition_time)

def move_through_coordinates(coordinates, transition_time, polynom=False):
    """ This function moves the mouse controller through the passed coordinates.

This function gets the following arguments:
    coordinates - a tuple of tuples that represent the points on the Bezier
                  curve.
    transition_time - an integer - the amount of time to make the whole movement.
    polynom - boolean (default = False) - currently is not used.

This function returns None."""

    logger.debug('#### MOVING MOUSE ####')
    step_time = round(transition_time / len(coordinates) / 1000, 6)
    if step_time < MINIMUM_SLEEP_TIME:
        step_time = MINIMUM_SLEEP_TIME
    number_of_steps = len(coordinates)
    logger.debug(f'Number of steps: {number_of_steps}')
    logger.debug(f'Step time: {step_time} seconds.')

    st_time = time.perf_counter()

    for i in range(1, number_of_steps):
        if polynom:
            ctypes.windll.user32.SetCursorPos(coordinates[i][0], 
                                              int(polynom(coordinates[i][0]))
                                              )
        else:
            ctypes.windll.user32.SetCursorPos(coordinates[i][0], coordinates[i][1])
        if i < number_of_steps - 1:
            time.sleep(step_time)
    end_time = time.perf_counter()
    logger.debug(f'Measured transition time = {end_time - st_time}')
    logger.debug(f'#######################')

def click(button='left', double_click=False):
    """ This function is used to click at the current mouse position.

This function gets the following arguments:
    button - a string (default = 'right') - the name of a mouse button
             ('left', 'right', and 'middle').
    double_click - boolean (default = False) - if True the double-click
             will be performed.

This function returns None."""

    if button == 'right':
        dwFlags1 = MOUSEEVENTF_RIGHTDOWN
        dwFlags2 = MOUSEEVENTF_RIGHTUP
    elif button == 'left':
        dwFlags1 = MOUSEEVENTF_LEFTDOWN
        dwFlags2 = MOUSEEVENTF_LEFTUP
    elif button == 'middle':
        dwFlags1 = MOUSEEVENTF_MIDDLEDOWN
        dwFlags2 = MOUSEEVENTF_MIDDLEUP  
    else:
        logger.warning(f'Cannot find mouse button {button}')
        return None

    x = INPUT(type=INPUT_MOUSE, 
              mi=MOUSEINPUT(mouseData=0, dwFlags=dwFlags1)
            )
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    time.sleep(0.13)
    x = INPUT(type=INPUT_MOUSE, 
              mi=MOUSEINPUT(mouseData=0, dwFlags=dwFlags2)
            )
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

    if double_click:
        x = INPUT(type=INPUT_MOUSE, 
              mi=MOUSEINPUT(mouseData=0, dwFlags=dwFlags1)
            )
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
        time.sleep(0.13)
        x = INPUT(type=INPUT_MOUSE, 
                 mi=MOUSEINPUT(mouseData=0, dwFlags=dwFlags2)
                )
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

if __name__ == '__main__':
    # The following piece of code can be used to test the capabilities of 
    # the module.
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long),
                    ("y", ctypes.c_long)]
    cursor = POINT()
    time.sleep(5)
    click(button='right')