
__version__ = '0.1'

import os, logging

logger = logging.getLogger('ruautogui')

logger.setLevel(logging.DEBUG)

logConsoleHandler = logging.StreamHandler()
formatterConsole = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logConsoleHandler.setFormatter(formatterConsole)
logger.addHandler(logConsoleHandler)

logFileHandler = logging.FileHandler(f'ruautogui.log')
formatterFile = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logFileHandler.setFormatter(formatterFile)
logger.addHandler(logFileHandler)    