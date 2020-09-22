# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('ruautogui.bezier')
logger.setLevel(logging.DEBUG)

logConsoleHandler = logging.StreamHandler()
formatterConsole = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logConsoleHandler.setFormatter(formatterConsole)
logger.addHandler(logConsoleHandler)

logFileHandler = logging.FileHandler(f'ruautogui.log')
formatterFile = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logFileHandler.setFormatter(formatterFile)
logger.addHandler(logFileHandler) 

import math
import random
import time
import ctypes

def get_mouse_cursor_position():
    cursor = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return (cursor.x, cursor.y)
    
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

def get_curve_points(
        begin_pos=None, 
        end_pos=(100,100),
        order=2,
        control_points=[],
        transition_time=None
    ):
    """ This function gets the following arguments:
    begin_pos - a tuple of x and y coordinates of the starting point 
                (default = None - the starting point will be the current cursor
                position);
    end_pos - a tuple of x and y coordinates of the ending point 
                (default = (100,100));
    order - an integer that indicates the order of the Bezier curve 
                (default=2)
                (if order is 1 the resulting curve is a straight line,
                if order is 2 the resulting curve is quadratic etc.);
    control_points - a list of tuples of x and y coordinates of the control points
                (default is an empty list - the control points will be calculated
                randomily).
    transition_time - an integer - transition time in milliseconds
                (default is None - the transition time will be calculated randomily)
Returns:
    points - a tuple of tuples of x and y coordinates of the Bezier curve;
    control_points - a tuple of tuples of x and y coordinates of the control
        points, including the starting  and the ending points;
    transition_time - an integer in milliseconds of the transition time.
    """

    if begin_pos == None:
        begin_pos = get_mouse_cursor_position()

    # Make sure that the order equal to at least one.
    if order < 2:
        order = 1

    # The transition time that is used for calculating the points of the curve.
    if transition_time == None:
        transition_time = get_random_travel_time(begin_pos, end_pos)

    logger.debug(f'The transition time is {transition_time}')

    # The optimal number of points is calculated keeping in mind that the points of the curve
    # could be used for automatic mouse movement. Therefore, the sleep time between
    # the movements should be greater than 13 milliseconds.
    optimal_number_of_points = int(transition_time / 13)
    if optimal_number_of_points == 0:
        optimal_number_of_points = 1
    logger.debug(f'Optimal number of points: {optimal_number_of_points}')

    # The controls point are not passed as an argument to the function.
    # Therefore, they will be chosen randomily. The number of control points
    # are one less than the order of the curve.
    if len(control_points) == 0:
        logger.debug('The control points will be determined randomly')
        control_points.append(begin_pos)
        for i in range(1, order):
            random_control_point = get_random_control_point(begin_pos, end_pos)
            control_points.append(random_control_point)
        control_points.append(end_pos)

    # The control points have been passed to the function. We need to add the starting point and 
    # ending point to the list of control points.
    else:
        control_points.insert(0, begin_pos)
        control_points.append(end_pos)

    logger.debug(f'Control points: {control_points}')
    logger.debug(f'ORDER: {order}')

    # Calculated points of the Bezier curve are added to the following list.
    points = []

    STEP = int(transition_time / optimal_number_of_points)
    if STEP == 0:
        STEP = 1
    logger.debug(f'The optimal step for calculating the points is {STEP} milliseconds.')
    time_stamps = [t / (transition_time) for t in range(0, transition_time + 1, STEP)]

    for time_stamp in time_stamps:
        point_x = 0
        point_y = 0 
        for i in range(0, order + 1):
            coeff = number_of_combinations(order, i) * (1 - time_stamp) ** (order - i) * time_stamp ** i
            point_x += coeff * control_points[i][0] 
            point_y += coeff * control_points[i][1]
        points.append((int(point_x), int(point_y))) 

    return tuple(points), tuple(control_points), transition_time

def get_random_control_point(
        begin_pos=(300,10), 
        end_pos=(280,100),
    ):
    """ This function gets the coordinates of two points both as a tuple,
calculates a random control point for a Bezier curve.
Returns the coordinates of the random control point as a tuple of coordinates."""
    
    # Random offsets are calculated. The offsets show how far the control
    # point is from the straight line that connects the two initial points.
    # If the offsets equal to zero, the control point is on the line.
    offset_x = round(random.uniform(0.25, 0.55), 2)
    offset_y = round(random.uniform(0.25, 0.55), 2)

    # The following block calculates the coordinates of the middle of the straight line.
    middle_x = abs((end_pos[0] - begin_pos[0]) // 2)
    if middle_x < 30:
        middle_x = random.randint(30, 45)
    middle_y = abs((end_pos[1] - begin_pos[1]) // 2)
    if middle_y < 30:
        middle_y = random.randint(30, 45)

    # Variable direction shows the relative position of the control point.
    # If direction is 1, the control point will be to the right of the straight line.
    # If direction is -1, the control point will be to the left.
    direction = random.choice((-1,1))

    # The x coordinate of the control point
    control_point_x = int(min(begin_pos[0], end_pos[0]) + middle_x + direction * middle_x * offset_x)
    
    # The y coordinate of the control point depends on the inclination of the straight line.
    if (begin_pos[0] >= end_pos[0] and begin_pos[1] >= end_pos[1]) \
            or (end_pos[0] >= begin_pos[0] and end_pos[1] >= begin_pos[1]
        ):
        control_point_y = int(min(begin_pos[1], end_pos[1]) + middle_y - direction * middle_y * offset_y)    
    elif (begin_pos[0] > end_pos[0] and begin_pos[1] < end_pos[1]) \
            or (end_pos[0] > begin_pos[0] and end_pos[1] < begin_pos[1]
        ):           
        control_point_y = int(min(begin_pos[1], end_pos[1]) + middle_y + direction * middle_y * offset_y)
    
    return (control_point_x, control_point_y)

def get_random_travel_time(begin_pos, end_pos):
    """ This function gets the coordinates of two points both as a tuple.
Returns a random duration of transition between the two points.
The transition time slightly correlates with the distance."""
    MINIMUM_TRANSITION_TIME_MILLISECONDS = 150
    MAXIMUM_TRANSITION_TIME_MILLISECONDS = 850
    # The distance is calculated using the Pythagorean theorem.
    distance = int(math.sqrt((end_pos[0] - begin_pos[0]) ** 2 + (end_pos[1] - begin_pos[1]) ** 2))
    
    logger.debug(f'The distance between the two points is {distance}')
    resulting_random_transition_time = distance // (random.randint(3,4))
    if resulting_random_transition_time < MINIMUM_TRANSITION_TIME_MILLISECONDS:
        resulting_random_transition_time = MINIMUM_TRANSITION_TIME_MILLISECONDS + random.randint(10,100)
    
    if resulting_random_transition_time > MAXIMUM_TRANSITION_TIME_MILLISECONDS:
        resulting_random_transition_time = MAXIMUM_TRANSITION_TIME_MILLISECONDS - random.randint(10,100)
    
    logger.debug(f'Random transition time has been chosen: {resulting_random_transition_time} milliseconds.')
    return resulting_random_transition_time

def number_of_combinations(n, i):
    """ This function gets the binominal coefficients n and i.
        Returns the number of ways the i objects can be chosen from among n objects."""
    return int((math.factorial(n)) / (math.factorial(i) * math.factorial(n - i)))