#!/usr/bin/python3

import logging
logger = logging.getLogger('ruautogui.bezier_draftsman')

logger.setLevel(logging.DEBUG)

logConsoleHandler = logging.StreamHandler()
formatterConsole = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logConsoleHandler.setFormatter(formatterConsole)
logger.addHandler(logConsoleHandler)

logFileHandler = logging.FileHandler(f'ruautogui.log')
formatterFile = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logFileHandler.setFormatter(formatterFile)
logger.addHandler(logFileHandler)  

import sys
if sys.platform == 'win32':
    try:
        import cv2
        import numpy
        import ctypes
        if __name__ == '__main__':
            import bezier
        else:
            from ruautogui import bezier
    except Exception as exc:
        print(f'Cannot import required module: {exc}')
        sys.exit()
else:
    raise Exception('Currently supports only Windows OS!')

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

def get_screen_size():
    return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

def get_left_button_state():
    return ctypes.windll.user32.GetKeyState(0x01)

def get_mouse_cursor_position():
    cursor = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return (cursor.x, cursor.y)

def get_blank_image(width, height):
    return numpy.zeros(shape=[height, width, 3], dtype=numpy.uint8)

def draftsman():
    try:
        SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()
    except Exception as exc:
        SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
    blank_image = get_blank_image(SCREEN_WIDTH, SCREEN_HEIGHT)
    left_button_release_state = (0, 1)
    begin_and_end_points = []
    control_points = []
    mouse_key_down = False
    while True:
        current_button_state = get_left_button_state()

        if len(begin_and_end_points) < 2 and \
        current_button_state not in left_button_release_state and \
        mouse_key_down == False:
            begin_and_end_points.append(get_mouse_cursor_position())
            mouse_key_down = True
            #print(f'Clicked!: {get_mouse_cursor_position()}')

        elif len(begin_and_end_points) < 2 and \
        current_button_state in left_button_release_state and \
        mouse_key_down == True :
            mouse_key_down = False

        elif len(begin_and_end_points) == 2 and \
        current_button_state not in left_button_release_state and \
        mouse_key_down == False:
            control_points.append(get_mouse_cursor_position())
            mouse_key_down = True
            #print(f'Clicked!: {get_mouse_cursor_position()}')

        elif len(begin_and_end_points) == 2 and \
        current_button_state in left_button_release_state and \
        mouse_key_down == True :
            mouse_key_down = False

        if len(begin_and_end_points) == 0:
            message1 = 'Put the starting point by clicking elsewhere'
            message2 = 'Press ESC to quit'
        elif len(begin_and_end_points) == 1:
            blank_image = get_blank_image(SCREEN_WIDTH, SCREEN_HEIGHT)
            message1 = 'Put the ending point by clicking elsewhere'
            message2 = 'Press ESC to quit'
        else:
            blank_image = get_blank_image(SCREEN_WIDTH, SCREEN_HEIGHT)
            message1 = 'Put as many control points as you want'
            message2 = 'Press ESC to quit, SPACEBAR to proceed to the curve'
        for point in begin_and_end_points: 
            cv2.circle(blank_image, point, 5, [0, 255, 0], -1)
        for point in control_points:
            cv2.circle(blank_image, point, 5, [255, 0, 0], -1)

        cv2.putText(blank_image, 
                    message1,
                    (50,50),
                     cv2.FONT_HERSHEY_SIMPLEX,                     
                     1,
                     (255,255,255),
                     1
                     )
        cv2.putText(blank_image, 
                    message2,
                    (50,100),
                     cv2.FONT_HERSHEY_SIMPLEX,                     
                     1,
                     (255,255,255),
                     1
                     )

        cv2.namedWindow('Blank window', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Blank window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Blank window', blank_image)
        key = cv2.waitKey(1)
        if key == 27: 
            break  # esc to quit
            cv2.destroyAllWindows()
        elif key == 32:
            break

    ORDER_OF_CURVE = 1 + len(control_points)

    points, control_points, _ = bezier.get_curve_points(begin_and_end_points[0], 
                                                        begin_and_end_points[1],
                                                        ORDER_OF_CURVE,
                                                        control_points)

    blank_image = get_blank_image(SCREEN_WIDTH, SCREEN_HEIGHT)
    while True:
        cv2.circle(blank_image, begin_and_end_points[0], 5, [0, 255, 0], -1)
        cv2.circle(blank_image, begin_and_end_points[1], 5, [0, 255, 0], -1)
        for i in range(1, len(control_points) - 1):
            cv2.circle(blank_image, control_points[i], 5, [0, 0, 255], -1)
        for i in range(1, len(points) - 1):
            cv2.circle(blank_image, points[i], 3, [255, 0, 0], -1)
        
        message1 = 'Press ESC to quit or SPACEBAR to start over again'
        cv2.putText(blank_image, 
                    message1,
                    (50,50),
                     cv2.FONT_HERSHEY_SIMPLEX,                     
                     1,
                     (255,255,255),
                     1
                     )
        cv2.namedWindow('Blank window', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Blank window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Blank window', blank_image)
        key = cv2.waitKey(1)
        if key == 27: 
            break  # esc to quit
        elif key == 32:
            break
    if key == 27:
        cv2.destroyAllWindows()
    elif key == 32:
        draftsman()

if __name__ == '__main__':
    draftsman()
    