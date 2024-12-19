from parsing.modules.csv import save_excel
from undetected_chromedriver import By
from bs4 import BeautifulSoup

import undetected_chromedriver as uc
import time


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

def login():
    coocs = []
    driver = init_driver()
    driver.get(url='https://www.domkadrov.ru/empenter.php')
    # print(driver.page_source)
    time.sleep(20)
    for i in driver.get_cookies():
        coocs.append(i)
    driver.quit()
        
    print( coocs)

def detail_page(url, driver):
    """
    Функция для получения телефонов с поддержкой бесконечного скроллинга
    """
    
    driver.get(url)
    time.sleep(3)
    general = BeautifulSoup(driver.page_source, 'html.parser')  
    try:
        fio = general.find('div', class_='test3').text
    except:
        fio = None
    try:
        address = general.find('table', class_='test6cv').find(string='Адрес:').find_next('td').text
    except:
        address = None
    try:
        phone = general.find('table', class_='test6cv').find(string='Мобильный телефон:').find_next('td').text
    except:
        phone = None
    try:
        specialty = general.find('table', class_='test6cv').find(string='Специальность:').find_next('td').text
    except:
        specialty = None
    try:
        date_of_birth = general.find('td', class_='test5text').find(string='Дата рождения:').find_next('td').text
    except:
        date_of_birth = None
    try:
        family_position = general.find('td', class_='test5text').find(string='Семейное положение:').find_next('td').text
    except:
        family_position = None
    try:
        education = general.find('td', class_='test5text').find(string='Образование / Квалификация:').find_next('td').text
    except:
        education = None
    try:
        languages = general.find('td', class_='test5text').find(string='Языки:').find_next('td').text
    except:
        languages = None
    
    save_excel(fio=fio, phone=phone, adress=address, spesiolist=specialty, date_birth=date_of_birth, famaly_status=family_position, edu=education, lang=languages)
    

def pagination(cookies_list, compfunction_text_input: str, city_text_value: str):
    """
    Обработка списка объявлений с пропуском уже обработанных
    """
    driver = init_driver()
    
    # Открываем страницу перед запросом
    driver.get('https://www.domkadrov.ru')
    for i in cookies_list:
        driver.add_cookie(i)

    # фильтрация поиска
    driver.get('https://www.domkadrov.ru/hrentry.php')
    compfunction_text = driver.find_element(By.CSS_SELECTOR, 'input[name="compfunction_text"]')
    compfunction_text.clear()
    compfunction_text.send_keys(compfunction_text_input)
    
    city_text = driver.find_element(By.CSS_SELECTOR, 'input[name="city_text"]')
    city_text.clear()
    city_text.send_keys(city_text_value)
    
    submit = driver.find_element(By.CSS_SELECTOR, 'input[value="Найти"]')
    submit.click()
    
    time.sleep(6)
    
    general = BeautifulSoup(driver.page_source, 'html.parser')  
    main_page = general.find('td', id='tdframe')

    # Создаем список для хранения нужных ссылок
    pagination = set()
    pagination_old = []
    
    pagin = main_page.find_all('div', class_='test4')[3]
    # Находим все ссылки в этом блоке
    links = pagin.find_all('a')

    # Проходим по всем ссылкам и добавляем те, которые начинаются с "hrsearch.php"
    for link in links:
        href = link.get('href')
        if href.startswith('hrsearch.php'):
            pagination.add(href)
            
    # сбор ссылок на профиль и сохронения их в valid_links
    valid_links = set()
    cv_table = main_page.find('table', class_='test6t')
    for item in cv_table.find_all('a'):
        href = item.get('href')
        
        # Проверяем, начинается ли ссылка с "hrcandcv.php?"
        if href.startswith("hrcandcv.php?"):
            # Проверяем, содержит ли текст элемента слово "Скрыто"
            if "Скрыто" not in item.text:
                valid_links.add(href)    
    
    while True:
        # Получаем первый элемент из отсортированного множества
        try:
            next_url = min(pagination)
        except:
            for i in valid_links:
                detail_page(url=f'https://domkadrov.ru/{i}', driver=driver)
            break
        
        pagination_old.append(next_url)

        driver.get(url=f'https://domkadrov.ru/{next_url}')
        time.sleep(3)
        general = BeautifulSoup(driver.page_source, 'html.parser')  
        main_page = general.find('td', id='tdframe')
        
        cv_table = main_page.find('table', class_='test6t')
        for item in cv_table.find_all('a'):
            href = item.get('href')
            
            # Проверяем, начинается ли ссылка с "hrcandcv.php?"
            if href.startswith("hrcandcv.php?"):
                # Проверяем, содержит ли текст элемента слово "Скрыто"
                if "Скрыто" not in item.text:
                    valid_links.add(href)
        
        pagin = main_page.find_all('div', class_='test4')[3]
        # Находим все ссылки в этом блоке
        links = pagin.find_all('a')

        # Проходим по всем ссылкам и добавляем те, которые начинаются с "hrsearch.php"
        for link in links:
            href = link.get('href')
            if href.startswith('hrsearch.php'):
                if href not in pagination_old:
                    pagination.add(href)
        
        for i in valid_links:
            detail_page(url=f'https://domkadrov.ru/{i}', driver=driver)
            
        valid_links.clear()
        
        pagination.remove(next_url)