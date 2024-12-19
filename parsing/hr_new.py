from bs4 import BeautifulSoup
from undetected_chromedriver import By

import undetected_chromedriver as uc
import pandas as pd
import time
import re
import os


def save_excel2(fio: str, phone: str, city: str, resume: str, date_birth: str, email: str):
    # Путь к файлу
    file_path = 'NEW_HR_Excel.xlsx'

    # Новые данные для сохранения
    new_data = {
        'ФИО': fio,
        'Номер телефона': phone,
        'Почта': email,
        'Город': city,
        'Дата рождения': date_birth,
        'Резюме': resume,
    }

    # Проверяем существует ли файл
    if os.path.exists(file_path):
        # Читаем существующий файл
        existing_df = pd.read_excel(file_path)

        # Создаем DataFrame с новыми данными
        new_row_df = pd.DataFrame([new_data])

        # Объединяем существующие и новые данные
        result_df = pd.concat([existing_df, new_row_df], ignore_index=True)
    else:
        # Если файл не существует, создаем новый DataFrame
        result_df = pd.DataFrame([new_data])

    # Сохраняем обновленные данные
    result_df.to_excel(file_path, index=False)
    
def init_driver():
    options_chrome = uc.ChromeOptions()
    options_chrome.add_argument("--window-position=-32000,-32000")
    options_chrome.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = uc.Chrome(
        driver_executable_path='chrome_windows/chromedriver-win64/chromedriver-win64/chromedriver.exe',
        browser_executable_path='chrome_windows/chrome-win64/chrome-win64/chrome.exe',
        options=options_chrome,
        use_subprocess=True,
        version_main=133,
        headless=True,
    )
    return driver

def login_gorodrabot():
    coocs = []
    driver = init_driver()
    driver.get(url='https://gorodrabot.ru/site/login')
    # print(driver.page_source)
    time.sleep(20)
    for i in driver.get_cookies():
        coocs.append(i)
    driver.quit()
        
    print( coocs)

def detail_page_gorodrabot(url, driver: uc.Chrome):
    """
    Функция для получения телефонов с поддержкой бесконечного скроллинга
    """
    
    driver.get(url)
    time.sleep(3)
    phone = driver.find_element(By.CSS_SELECTOR, 'li[class="resume-view__list-item resume-view__contacts contacts-info"]')
    phone.click()
    time.sleep(3)
    
    general = BeautifulSoup(driver.page_source, 'html.parser')  
    
    
    # Инициализируйте переменные до цикла
    email = None
    phone_number = None
    fio = None
    date_of_birth = None
    city = None
    resume = None

    # поиск почты и номера телефона
    contact_elements = general.find_all('div', class_='contacts-info__content')
    # Проход по найденным элементам
    for element in contact_elements:
        # Найти элементы с email и телефоном
        email_element = element.find('span', string='Email: ')
        phone_element = element.find('span', string='Телефон: ')

        # Извлечь значения, если элементы найдены
        if email_element:
            email = email_element.find_next('a').text.strip()
        
        if phone_element:
            phone_number = phone_element.find_next('a').text.strip()

    # поиск фио, даты рождения, город проживания
    contact_elements = general.find_all('ul', class_='resume-view__list sidebar-light__block')
    
    for ul_element in contact_elements:
        # Найдем элементы с именем
        for li in ul_element.find_all('li', class_='resume-view__list-item'):
            if 'Имя:' in li.text:
                fio = li.find('span', class_='resume-view__text').text.strip()
                break
        
        # Найдем элементы с датой рождения
        for li in ul_element.find_all('li', class_='resume-view__list-item'):
            if 'Дата рождения:' in li.text:
                date_of_birth = li.find('strong').text.strip()
                break
        
        # Найдем элементы с городом проживания
        for li in ul_element.find_all('li', class_='resume-view__list-item'):
            if 'Город проживания:' in li.text:
                city = li.find('strong').text.strip()
                break
    
    try:
        def clean_text(text):
            # Удаление лишних пробелов, переносов строк и табуляций
            text = re.sub(r'\s+', ' ', text).strip()

            # Удаление специальных символов и лишних пробелов
            text = re.sub(r'\s*(?:Поделиться с друзьями:|ВКонтакте|Одноклассники|Мой Мир|Viber|WhatsApp|Skype|Telegram|Я\.Мессенджер)\s*', '', text)

            # Удаление повторяющихся пробелов
            text = ' '.join(text.split())

            return text

        # поиск полной резюме
        contact_elements = general.find('div', class_='resume-view__content')
        resume = clean_text(contact_elements.text)
        
    except:
        resume = None

    save_excel2(fio=fio, phone=phone_number, city=city, date_birth=date_of_birth, email=email, resume=resume )
    

def pagination_new(url, cookies_dropdown):
    """
    Обработка списка объявлений с пропуском уже обработанных
    """
    driver = init_driver()
    
    if cookies_dropdown == '1':
        cookies = [{'domain': '.gorodrabot.ru', 'expiry': 1734027093, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734025893'}, {'domain': '.gorodrabot.ru', 'expiry': 1768585890, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734025880.1.1.1734025890.50.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765561890, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734025889'}, {'domain': '.gorodrabot.ru', 'expiry': 1736617889, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350838%2C%22AfN9qt7p_4OgYNu99GJHqdRq4sWZmuSZ%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'f14rtuo688aa3m649ilttvcran'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235484, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'hTLABKo+5X7sH6SqKdYigEdY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734027690, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768585890, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.1241435114.1734025881'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'FN4lcAA6S28cx_2sIVii9if0zi7Fr7Ji'}, {'domain': '.gorodrabot.ru', 'expiry': 1734097880, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1765561890, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734025881920372946'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027093, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'C7bXjes27ENhVd9x'}, {'domain': '.gorodrabot.ru', 'expiry': 1765561879, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'xB7Fj1tSLlzyPOYAN5v3'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027093, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]
    if cookies_dropdown == '2':
        cookies = [{'domain': '.gorodrabot.ru', 'expiry': 1734027135, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734025935'}, {'domain': '.gorodrabot.ru', 'expiry': 1768585932, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734025926.1.1.1734025932.54.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765561932, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734025932'}, {'domain': '.gorodrabot.ru', 'expiry': 1736617932, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350837%2C%22WGH5PNS_GD0kKjB_Vg0DvVLSw8l3VPg_%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'e4clj440p7gfq7ht01bj3lf46l'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235529, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1gk5jVmPhDQbzek1ij7MsUdY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734027733, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768585932, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.832975510.1734025926'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'JWF2py4FVSbe85vATe-2exGRgfmgwXdZ'}, {'domain': '.gorodrabot.ru', 'expiry': 1734097926, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1765561932, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734025926478274501'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027135, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'OoGnxgTPe4ClRYUf'}, {'domain': '.gorodrabot.ru', 'expiry': 1765561925, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'IWAjh2aUdNvndS6ZJo3F'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027135, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]

    if cookies_dropdown == '3':
        cookies = [{'domain': '.gorodrabot.ru', 'expiry': 1734027178, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734025978'}, {'domain': '.gorodrabot.ru', 'expiry': 1768585976, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734025970.1.1.1734025976.54.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765561975, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734025975'}, {'domain': '.gorodrabot.ru', 'expiry': 1736617975, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350836%2C%22cCgtD1awfi4kph0XxdT_Hl_Al9E0ESh9%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 's09ra1n6vfb6aludoagq0dqri8'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235573, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'Zy2be1Pmt8UXOIP1JjEa3UdY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734027776, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768585976, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.1182116415.1734025970'}, {'domain': '.gorodrabot.ru', 'expiry': 1765561975, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734025969522096537'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'xDrXrNPxcRdxDMVY_RYuKZa2Vfar1gkS'}, {'domain': '.gorodrabot.ru', 'expiry': 1734097969, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027178, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'ejGko4vTEB3VbfD3'}, {'domain': '.gorodrabot.ru', 'expiry': 1765561968, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'kQzdiCzLb8N5TjGbqMAA'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027178, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]

    if cookies_dropdown == '4':
        cookies =[{'domain': '.gorodrabot.ru', 'expiry': 1734027226, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734026026'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586023, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734026016.1.1.1734026023.53.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562023, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026023'}, {'domain': '.gorodrabot.ru', 'expiry': 1736618023, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350835%2C%22As8crQAJ4U9Vziu2Pqv4yTa1MYqTaikk%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '826mcgqb753rb3jat9f7g2hts3'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235619, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '7DDkUMNdz7VFl3/NAJCx9UdY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734027823, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586023, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.1599594.1734026016'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'ekaac3LwZPvqJkMTn-2IrC51SEKC0Dej'}, {'domain': '.gorodrabot.ru', 'expiry': 1734098016, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562023, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026016941723711'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027226, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '3juXuK8gopM2TyC2'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562015, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'yFDGEOGT6N8VTZrzY0S1'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027226, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]

    if cookies_dropdown == '5':
        cookies = [{'domain': '.gorodrabot.ru', 'expiry': 1734027273, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734026073'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586070, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734026063.1.1.1734026070.53.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562070, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026070'}, {'domain': '.gorodrabot.ru', 'expiry': 1736618070, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350834%2C%22b0UyZyQ2Mb2OsxXX-oCe-A8bl_kDqqoC%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'b7fi9kktlbdnvc5nbgpadj3nk1'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235666, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'cmg2NAYtlkIRnb3MV+Xb5UdY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734027870, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586070, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.2107819697.1734026064'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562070, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026063885751908'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'vSjFnyzmUK7rYNzFMtRjhn6wWrwKMHuD'}, {'domain': '.gorodrabot.ru', 'expiry': 1734098062, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027273, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'qUSNppjkGFYrYXBi'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562062, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'rxMzMj6OTEGu5gFqdO4c'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027273, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]

    if cookies_dropdown == '6':
        cookies = [{'domain': '.gorodrabot.ru', 'expiry': 1734027314, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734026114'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586112, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734026105.1.1.1734026112.53.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562111, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026111'}, {'domain': '.gorodrabot.ru', 'expiry': 1736618111, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350833%2C%22biOv_lEmMpfiN9Pmwt78oUiv_jPPv7Ob%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '25iloljvjn0k07fsf4n4ovf2lr'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235708, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'N0PaScUYZRxeOiCmZXBbl0dY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734027912, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586112, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.1739846543.1734026106'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562111, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026105352696721'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'uJI8S0w5Hyld-DCOS4dcmNTLKn3tNOoy'}, {'domain': '.gorodrabot.ru', 'expiry': 1734098105, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027314, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GHUbt3f8AnTXPoM5'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562104, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'hwGSh5EObYDX7QU9HCu4'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027314, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]

    if cookies_dropdown == '7':
        cookies7 = [{'domain': '.gorodrabot.ru', 'expiry': 1734027357, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734026157'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586155, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734026149.1.1.1734026155.54.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562154, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026154'}, {'domain': '.gorodrabot.ru', 'expiry': 1736618154, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350832%2C%228LB0-FqaGK4xZNnFqyBOVZPtz29wrea_%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'tkl6k9ujipoinqf45kgu9be1jt'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235753, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'q12WG5KXEHfVCdVPZjYWM0dY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734027955, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586155, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.1510375618.1734026149'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'iEeAACsSO8fsCOOMDs0YAvpgP_QBkWBX'}, {'domain': '.gorodrabot.ru', 'expiry': 1734098149, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562154, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026149266795654'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027357, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'v3VlY5VoPZuNQqOQ'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562148, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'DNhQNgxhT9Es6nhd8JTL'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027357, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]

    if cookies_dropdown == '8':
        cookies = [{'domain': '.gorodrabot.ru', 'expiry': 1734027403, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734026203'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586201, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734026191.1.1.1734026201.50.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562200, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026200'}, {'domain': '.gorodrabot.ru', 'expiry': 1736618200, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350831%2C%22jtDr-vowb_SmDo9-bVopJMaPx_WN2Doe%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 't2ub3eioqbk0h30au1jreo25p4'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235795, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '19ftBOvR0at+RA6x9IXsZUdY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734028001, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586201, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.377006753.1734026192'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '5kFIx-NsQ_9OkaCwPLzretr-6FbgUeC1'}, {'domain': '.gorodrabot.ru', 'expiry': 1734098191, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562200, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026192462156506'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027403, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'vTnenACBSNxGcITS'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562190, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'HgTXRVjwlKHY8dLDIgXU'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027403, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]

    if cookies_dropdown == '9':
        cookies = [{'domain': '.gorodrabot.ru', 'expiry': 1734027442, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734026242'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586240, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734026234.1.1.1734026240.54.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562239, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026239'}, {'domain': '.gorodrabot.ru', 'expiry': 1736618239, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350829%2C%22xkLufsMrGf6UUhQTR3D6OhCLfHbGYvoz%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'aa80gfpcri1s4c6ja64k66pmo5'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235837, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'PzTQHwm7c27W43DaKRBrJkdY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734028040, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586240, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.2134599479.1734026235'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'eUEh2vVNR9ra48HZ5VYPvVBsxjPJBg7A'}, {'domain': '.gorodrabot.ru', 'expiry': 1734098234, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562239, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026234107142700'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027442, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'eHBrszJkbp9fJ19b'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562233, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'Fh1AHg7ZgvSfOS27KZAc'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027442, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]

    if cookies_dropdown == '10':
        cookies = [{'domain': '.gorodrabot.ru', 'expiry': 1734027442, 'httpOnly': False, 'name': '__ddg10_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1734026242'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586240, 'httpOnly': False, 'name': '_ga_NK4HJRW8FT', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1734026234.1.1.1734026240.54.0.0'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562239, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026239'}, {'domain': '.gorodrabot.ru', 'expiry': 1736618239, 'httpOnly': True, 'name': '_identity', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%5B1350829%2C%22xkLufsMrGf6UUhQTR3D6OhCLfHbGYvoz%22%2C2592000%5D'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'aa80gfpcri1s4c6ja64k66pmo5'}, {'domain': '.gorodrabot.ru', 'expiry': 1735235837, 'httpOnly': False, 'name': 'cycada', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'PzTQHwm7c27W43DaKRBrJkdY0vP8GU2bWfdZzatojTU='}, {'domain': '.gorodrabot.ru', 'expiry': 1734028040, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'b'}, {'domain': '.gorodrabot.ru', 'expiry': 1768586240, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.2134599479.1734026235'}, {'domain': '.gorodrabot.ru', 'httpOnly': True, 'name': '_csrf-frontend', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'eUEh2vVNR9ra48HZ5VYPvVBsxjPJBg7A'}, {'domain': '.gorodrabot.ru', 'expiry': 1734098234, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562239, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1734026234107142700'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027442, 'httpOnly': False, 'name': '__ddg8_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'eHBrszJkbp9fJ19b'}, {'domain': '.gorodrabot.ru', 'expiry': 1765562233, 'httpOnly': True, 'name': '__ddg1_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'Fh1AHg7ZgvSfOS27KZAc'}, {'domain': '.gorodrabot.ru', 'expiry': 1734027442, 'httpOnly': False, 'name': '__ddg9_', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '95.87.74.249'}]


    # Открываем страницу перед запросом
    driver.get('https://gorodrabot.ru')
    for i in cookies:
        driver.add_cookie(i)
        
    driver.get(url)
    time.sleep(3)
    
    general = BeautifulSoup(driver.page_source, 'html.parser')  
    main_page = general.find('div', class_='result-list')

    # Создаем список для хранения нужных ссылок
    pagination = set()
    pagination_old = []
    
    pagin = main_page.find_all('ul', class_='result-list__pager pager')

    # Проходим по всем найденным спискам
    for paginator in pagin:
        # Найдем все элементы `<a>` в списке
        links = paginator.find_all('a')
        
        # Проходим по всем ссылкам
        for link in links:
            # Получаем текст ссылки
            text = link.get_text()
            
            # Проверяем наличие цифр в тексте
            if re.search(r'\d', text):
                # Если цифра найдена, добавляем ссылку в множество
                pagination.add(link['href'])
            
    # сбор ссылок на профиль и сохронения их в valid_links
    valid_links = set()
    cv_table = main_page.find_all('a', class_='snippet__title-link link')
    for link in cv_table:
        href = link.get('href')
        valid_links.add(href)
    
    while True:
        # Получаем первый элемент из отсортированного множества
        try:
            next_url = min(pagination)
        except:
            for i in valid_links:
                print(i)
                detail_page_gorodrabot(url=f'https://domkadrov.ru/{i}', driver=driver)
            break

        pagination_old.append(next_url)

        driver.get(url=next_url)
        time.sleep(3)
        general = BeautifulSoup(driver.page_source, 'html.parser')  
        main_page = general.find('div', class_='result-list')
        
        pagin = main_page.find_all('ul', class_='result-list__pager pager')

        # Проходим по всем найденным спискам
        for paginator in pagin:
            # Найдем все элементы `<a>` в списке
            links = paginator.find_all('a')

            # Проходим по всем ссылкам
            for link in links:
                # Получаем текст ссылки
                text = link.get_text()

                # Проверяем наличие цифр в тексте
                if re.search(r'\d', text):
                    # Если цифра найдена, добавляем ссылку в множество
                    pagination.add(link['href'])

        # Проходим по всем ссылкам профиля 
        cv_table = main_page.find_all('a', class_='snippet__title-link link')
        for link in cv_table:
            href = link.get('href')
            valid_links.add(href)
        
        for i in valid_links:
            print(i)
            detail_page_gorodrabot(url=i, driver=driver)
            
        valid_links.clear()
        
        pagination.remove(next_url)
        
