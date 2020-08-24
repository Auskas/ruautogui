# RuAutoGUI

RuAutoGUI программный пакет для языка программирования Python с имитацией человеческого поведения
для программного управления мышью и клавиатурой.

## Возможности модуля

- Последовательное нажатие клавиш клавиатуры для ввода текста в формы web страниц и т.п.
- Поддержка кириллических символов при вводе текста.
- Поддержка горячих клавиш, например Alt+Tab или Alt+Shift.
- Настраиваемая случайная задержка между вводом символов.
- Опция исправляемых ошибок при вводе текста с настраиваемой частотой ошибок.
- Перемещение курсора мыши в заданную точку по так называемой кривой Безье.
- Случайный или настраиваемый порядок кривой Безье.
- Случайное движение курсора мыши для имитации "хватания" рукой мыши.
- Клик и двойной клик.

## Системные требования
- OS Windows 10 (не проверялось на ранних версиях)
- Python 3.6 и выше

## Установка

В данный момент поддерживается установка из репозитария github:
```
https://github.com/Auskas/ruautogui.git
```

## Примеры использования модуля клавиатуры
```python
from ruautogui import keyboard as kb

text = "Пример использования модуля клавиатуры!"
kb.type(text, mode="fast")
```
![keyboard_example_1](https://github.com/Auskas/ruautogui/blob/master/demo/kb_example1.gif)
___
```python
from ruautogui import keyboard as kb
   
text = "Пример использования с исправляемыми опечатками!"
kb.type(text, mode="ultrafast", typo=True)
```
![keyboard_example_2](https://github.com/Auskas/ruautogui/blob/master/demo/kb_example2.gif)

## Пример использования модуля мыши
```python
from ruautogui import mouse as ms 
import time

ms.grab() # Имитация захвата рукой мыши
time.sleep(1) # Таймаут перед следующим действием
ms.move((300,300)) # Движение мыши по кривой Безье до точки 300,300
```
![mouse_example](https://github.com/Auskas/ruautogui/blob/master/demo/mouse_example.gif)

## Пример совместного использования с пакетом Selenium
В случае, если вы хотите имитировать поведение реального человека на web странице,
простое использование пакета Selenium не является достаточным.
При использовании ресурсом технологии webvisor, если вы переживаете, что
ваш робот или парсер может быть выявлен, используёте ruautogui совместно с Selenium.

```python
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

input_field = driver.find_element_by_xpath("//input[contains(@class, 'form-control')]")
ms.grab()
time.sleep(1)
field_location = (input_field.location['x'], input_field.location['y'])
field_size = (input_field.size['width'], input_field.size['height'])

target_loc = (
    field_location[0] + random.randint(field_size[0] // 4, field_size[0] // 2),
    field_location[1] + random.randint(field_size[1] // 4, field_size[1] // 2)
)
ms.move(target_loc)
time.sleep(1)
ms.click()
time.sleep(1)
kb.type('ruautogui', mode='ultrafast')
time.sleep(1)
kb.press('enter')
time.sleep(5)
driver.quit()
```
![selenium_example](https://github.com/Auskas/ruautogui/blob/master/demo/selenium_example.gif)

