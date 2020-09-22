from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ruautogui import keyboard as kb 
from ruautogui import mouse as ms 
import sys, random, time

chrome_options = ChromeOptions()
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = Chrome(options=chrome_options)

driver.get('https://github.com')
kb.press('f11') # Полноэкранный режим браузера
try:
    input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'form-control')]"))
    )
except Exception as exc:
    print('Невозможно найти поле ввода...')
    driver.quit()
    sys.exit()

# input_field - объект Selenium, в данном случае web элемент, представляющий
# собой поле ввода для поиска на github.com
input_field = driver.find_element_by_xpath("//input[contains(@class, 'form-control')]")

ms.grab() # имитируем хватание мыши рукой.
time.sleep(1)

# field_location - это кортеж из координат web элемента в окне браузера.
# Координаты представляют собой верхнюю левую точку элемента.
field_location = (input_field.location['x'], input_field.location['y'])
# field_size - это кортеж из длины и высоты элемента в окне браузера.
field_size = (input_field.size['width'], input_field.size['height'])

# target_loc используется как кортеж случайных координат внутри web элемента.
target_loc = (
    field_location[0] + random.randint(field_size[0] // 4, field_size[0] // 2),
    field_location[1] + random.randint(field_size[1] // 4, field_size[1] // 2)
)

ms.move(end_pos=target_loc, order=4) # Перемещение курсора мыши в зону поля ввода.
time.sleep(1)
ms.click() # Клик левой кнопкой мыши по полю ввода.
time.sleep(1)
kb.type('ruautogui', mode='standard', typo=True) # Ввод с клавиатуры текста 'ruautogui'
time.sleep(1)
kb.press('enter') # Нажатие кнопки enter на клавиатуре.
time.sleep(5)
driver.quit()