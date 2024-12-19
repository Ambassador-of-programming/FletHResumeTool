from parsing.modules.generate_password import generate_password
from parsing.modules.encrypt import encrypt_list, decrypt_list
from parsing.excel import read_excel_phone_numbers
from parsing.hr import pagination, init_driver
from parsing.hr_new import pagination_new
from undetected_chromedriver import By

import signal, os, multiprocessing
import flet as ft
import random
import string
import time


def generate_random_email():
    # Списки доменов
    domains = ['gmail.com', 'mail.ru']
    
    # Генерация случайного имени пользователя (8-12 символов)
    username_length = random.randint(8, 30)
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(username_length))
    
    # Выбор случайного домена
    domain = random.choice(domains)
    
    # Создание email-адреса
    email = f"{username}@{domain}"
    
    return email

def run_pagination(url):
    pagination(url=url)

async def main_menu(page: ft.Page):
    class GorodRabot:
        def __init__(self, page: ft.Page):
            self.page = page
            
            self.city = ['Краснодар', 'Уфа', 'Екатеринбург']
            self.city_dropdown = ft.Dropdown(
                width=150,
                options=[ft.dropdown.Option(platform) for platform in self.city],
                label="Выберите город",
                border_color="#1E3A8A",
                color="white",
                bgcolor="#1E3A8A",
                focused_bgcolor="#2A4A9A",
                focused_color="white",
                text_style=ft.TextStyle(color="white"),
                visible=True
            )
            
            self.cookies_drop = [1,2,3,4,5,6,7,8,9,10,]
            self.cookies_dropdown = ft.Dropdown(
                width=150,
                options=[ft.dropdown.Option(platform) for platform in self.cookies_drop],
                label="Выберите аккаунт",
                border_color="#1E3A8A",
                color="white",
                bgcolor="#1E3A8A",
                focused_bgcolor="#2A4A9A",
                focused_color="white",
                text_style=ft.TextStyle(color="white"),
                visible=True
            )

            self.profi = ft.TextField(
                label="Профессия",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                width=150,
                visible=True,
            )

            self.start_button = ft.ElevatedButton(
                "Старт",
                width=250,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=30),
                    elevation=5,
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                    animation_duration=300,
                ),
                disabled=False,
                on_click=self.start_clicked,
                visible=True
            )
            
            self.divider_3 = ft.Divider(height=1, color="#CCCCCC", visible=True)
            self.divider_6 = ft.Divider(height=1, color="#CCCCCC", visible=True)
            
            self.platform_menu = ft.ExpansionPanelList(
                controls=[
                    ft.ExpansionPanel(
                        expanded=False,
                        header=ft.Container(
                            content=ft.Text("Новый посредник в парсинге"),
                            alignment=ft.alignment.center
                        ),
                        content=ft.Container(
                            content=ft.Column([          
                                self.profi,
                                self.city_dropdown,
                                self.cookies_dropdown,
                                                                
                                self.divider_6,
                                self.start_button,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=10
                        )
                    )
                ]
            )
        async def start_clicked(self, e):
            if self.start_button.text == "Старт":
                if all([self.city_dropdown.value, self.profi.value, self.cookies_dropdown.value]):
                    self.start_button.style.bgcolor = {"": "#FF5252"}
                    self.start_button.text = "Стоп"
                    
                    if self.city_dropdown.value == 'Краснодар':
                        link = f'https://krasnodar.gorodrabot.ru/resumes?q={self.profi.value.strip()}&sort=date'
                    
                    if self.city_dropdown.value == 'Уфа':
                        link = f'https://ufa.gorodrabot.ru/resumes?q={self.profi.value.strip()}&sort=date'
                    
                    if self.city_dropdown.value == 'Екатеринбург':
                        link = f'https://ekaterinburg.gorodrabot.ru/resumes?q={self.profi.value.strip()}&sort=date'

                    main_pid = multiprocessing.Process(
                        target=pagination_new,
                        args=(link, self.cookies_dropdown.value, )
                    )
                    main_pid.start()
                    
                    page.session.set('main_pid', main_pid.pid)
            else:

                main_pid = page.session.get('main_pid')
                if main_pid:
                    try:
                        os.kill(main_pid, signal.SIGTERM)
                    except ProcessLookupError:
                        print(f"Process with PID {main_pid} not found")

                self.start_button.style.bgcolor = {"": "#4CAF50"}
                self.start_button.text = "Старт"
            await self.start_button.update_async()

            
            
    class RegisterCapthca:
        def __init__(self, page: ft.Page):
            self.page = page
            
            
            self.text_result = ft.Text(visible=False)
            self.captcha_img = ft.Image(
                src='icon.png',
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN,
                visible=False
            )
            
            self.captcha_text = ft.TextField(
                label="введите капчу",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                width=150,
                on_submit=self.captcha_text_submit,
                visible=False,
                
            )
            self.captcha_text_result = False

            self.start_button = ft.ElevatedButton(
                "Старт",
                width=250,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=30),
                    elevation=5,
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                    animation_duration=300,
                ),
                disabled=False,
                on_click=self.browser,
                visible=True
            )
            
            self.divider_3 = ft.Divider(height=1, color="#CCCCCC", visible=True)
            self.divider_6 = ft.Divider(height=1, color="#CCCCCC", visible=True)
            
            self.platform_menu = ft.ExpansionPanelList(
                controls=[
                    ft.ExpansionPanel(
                        expanded=False,
                        header=ft.Container(
                            content=ft.Text("Регистрация в парсинге"),
                            alignment=ft.alignment.center
                        ),
                        content=ft.Container(
                            content=ft.Column([          
                                self.text_result,
                                self.captcha_img,
                                self.captcha_text,
                                                                
                                self.divider_6,
                                self.start_button,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=10
                        )
                    )
                ]
            )
            
        def captcha_text_submit(self, event):
            self.captcha_text_result = True
            
        def browser(self, event):
            import time
            driver = init_driver()
            # Очищаем кэш сайта перед каждым запросом

            driver.get(url='https://www.domkadrov.ru/employernew.php')
            
            # Отрасль компании-работодателя
            industry_text = driver.find_element(By.CSS_SELECTOR, 'input[name="industry_text"]')
            industry_text.send_keys("Кадровое агентство")
            time.sleep(2)
            
            # Город работодателя
            city_text = driver.find_element(By.CSS_SELECTOR, 'input[name="city_text"]')
            city_text.send_keys("Москва")
            time.sleep(2)
            
            # Электронный адрес работодателя
            generate_email = generate_random_email()
            # print(generate_email)
            email = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
            email.send_keys(generate_email)
            time.sleep(2)
            
            # Пароль
            generate_pass = generate_password()
            # print(generate_pass)
            passwd = driver.find_element(By.CSS_SELECTOR, 'input[name="passwd"]')
            passwd.send_keys(generate_pass)
            time.sleep(2)
            
            # Повторите пароль
            repasswd = driver.find_element(By.CSS_SELECTOR, 'input[name="repasswd"]')
            repasswd.send_keys(generate_pass)
            time.sleep(2)
            
            try:
                img = driver.find_element(By.CSS_SELECTOR, 'img[alt="captcha"]').get_attribute('src')
                self.captcha_img.visible = True
                self.captcha_img.src = img
                self.captcha_img.update()
                
                self.captcha_text.visible = True
                self.captcha_text.update()

                while True:
                    if self.captcha_text_result == True:
                        # captcha
                        repasswd = driver.find_element(By.CSS_SELECTOR, 'input[name="captcha"]')
                        repasswd.send_keys(self.captcha_text.value)
                        break
            except:
                pass
            
            # Зарегистрировать
            repasswd = driver.find_element(By.CSS_SELECTOR, 'input[value="Зарегистрировать"]')
            repasswd.click()
            
            time.sleep(10)
            
            try:
                driver.find_element(By.LINK_TEXT, "Выход")
            except:
                self.text_result.visible = True
                self.text_result.color = 'RED'
                self.text_result.value = 'Не зарегистрирован'
                self.text_result.update()
                time.sleep(10)
                driver.quit()
            
            # вход после регистрации
            try:
                login_auth = driver.find_element(By.CSS_SELECTOR, 'input[name="id"]')
                login_auth.clear()
                login_auth.send_keys(generate_email)
                
                pass_auth = driver.find_element(By.CSS_SELECTOR, 'input[name="passwd"]')
                pass_auth.clear()
                pass_auth.send_keys(generate_pass)
                
                auth = driver.find_element(By.CSS_SELECTOR, 'input[value="Вход"]')
                auth.click()
            except:
                pass
            
            time.sleep(6)
                
            coocs = []
            for i in driver.get_cookies():
                coocs.append(i)
            
            encrypted_list, encryption_key = encrypt_list(coocs)
            
            page.client_storage.set('encrypted_list', list(encrypted_list))
            page.client_storage.set('encryption_key', list(encryption_key))

            self.text_result.visible = True
            self.text_result.color = 'GREEN'
            self.text_result.value = 'Зарегистрирован'
            self.text_result.update()
            driver.quit()
            
    class PhoneSendWhatsApp:
        def __init__(self, page: ft.Page):
            self.page = page
            
            self.mess_text = ft.TextField(
                label="Добавить текст сообщения",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
            )
            
            self.instance_id = ft.TextField(
                label="Добавить instance_id",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
            )
            self.access_token = ft.TextField(
                label="Добавить access_token",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
            )
            
            self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
            self.page.overlay.append(self.pick_files_dialog)
            self.add_text_button = ft.ElevatedButton(
                "Прикрепить Excel номера",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                on_click=self.open_file_picker,
                icon=ft.icons.FILE_DOWNLOAD,
                visible=True
            )
            
            self.start_button = ft.ElevatedButton(
                "Старт",
                width=250,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=30),
                    elevation=5,
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                    animation_duration=300,
                ),
                disabled=False,
                on_click=self.start_clicked,
                visible=True
            )
            self.divider_3 = ft.Divider(height=1, color="#CCCCCC", visible=True)
            self.divider_4 = ft.Divider(height=1, color="#CCCCCC", visible=True)
            self.divider_5 = ft.Divider(height=1, color="#CCCCCC", visible=True)
            self.divider_6 = ft.Divider(height=1, color="#CCCCCC", visible=True)
            
            
            self.platform_menu = ft.ExpansionPanelList(
                controls=[
                    ft.ExpansionPanel(
                        expanded=False,
                        header=ft.Container(
                            content=ft.Text("Рассылка с Excel базы"),
                            alignment=ft.alignment.center
                        ),
                        content=ft.Container(
                            content=ft.Column([          
                                self.mess_text,
                                self.divider_3,
                                                                
                                self.instance_id,
                                self.access_token,
                                self.divider_5,
                                
                                self.add_text_button,
                                self.divider_6,
                                self.start_button,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=10
                        )
                    )
                ]
            )
        
        def pick_files_result(self, e: ft.FilePickerResultEvent):
            if e.files:
                self.selected_file_path = e.files[0].path
            else:
                self.selected_file_path = None

        async def open_file_picker(self, e):
            await self.pick_files_dialog.pick_files_async(allow_multiple=False)

        async def start_clicked(self, e):
            if self.start_button.text == "Старт":
                if all([self.mess_text.value, self.instance_id.value, self.access_token.value]):
                    self.start_button.style.bgcolor = {"": "#FF5252"}
                    self.start_button.text = "Стоп"
                    
                    
                    main_pid = multiprocessing.Process(
                        target=read_excel_phone_numbers,
                        args=(self.selected_file_path, self.instance_id.value, self.access_token.value, self.mess_text.value,)
                    )
                    main_pid.start()
                    # page.session.set('main_pid', main_pid.pid)
 
            
    class ParsingMenu:
        def __init__(self, page: ft.Page):
            self.page = page
            self.platforms = ["HR"]

            self.dropdown = ft.Dropdown(
                width=250,
                options=[ft.dropdown.Option(platform) for platform in self.platforms],
                label="Выберите платформу",
                hint_text="Платформа",
                border_color="#1E3A8A",
                color="white",
                bgcolor="#1E3A8A",
                focused_bgcolor="#2A4A9A",
                focused_color="white",
                text_style=ft.TextStyle(color="white"),
                on_change=self.dropdown_changed
            )
            
            self.specialty  = ft.TextField(
                label="Специальность ",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=250
            )
            
            self.city  = ft.TextField(
                label="Город",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=250
            )
                      
            self.start_button = ft.ElevatedButton(
                "Старт",
                width=250,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=30),
                    elevation=5,
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                    animation_duration=300,
                ),
                disabled=True,
                on_click=self.start_clicked,
                visible=False
            )
            self.divider_1 = ft.Divider(height=1, color="#CCCCCC", visible=False)
            self.divider_2 = ft.Divider(height=1, color="#CCCCCC", visible=False)
            self.divider_3 = ft.Divider(height=1, color="#CCCCCC", visible=False)
            self.divider_4 = ft.Divider(height=1, color="#CCCCCC", visible=False)            
            
            self.platform_menu = ft.ExpansionPanelList(
                controls=[
                    ft.ExpansionPanel(
                        expanded=False,
                        header=ft.Container(
                            content=ft.Text("Настройки парсинга"),
                            alignment=ft.alignment.center
                        ),
                        content=ft.Container(
                            content=ft.Column([
                                self.dropdown,
                                self.divider_1,
                                
                                self.specialty,
                                self.divider_2,
                                
                                self.city,
                                self.divider_3,
                  
                                self.start_button,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=10
                        )
                    )
                ]
            )

            self.title = ft.Text("HR агентство", size=32, weight=ft.FontWeight.BOLD, color="#1E3A8A", text_align=ft.TextAlign.CENTER)
            self.subtitle = ft.Text("Ваш надежный партнер в мире рекрутинга", size=16, color="#64748B", italic=True, text_align=ft.TextAlign.CENTER)
            self.logo = ft.Icon(ft.icons.HOME_WORK, size=100, color="#1E3A8A")

            self.selected_file_path = None
        

        async def start_clicked(self, e):
            if self.start_button.text == "Старт":
                if self.dropdown.value == 'HR':
                
                    if all([self.specialty.value, self.city.value]):
                        self.start_button.style.bgcolor = {"": "#FF5252"}
                        self.start_button.text = "Стоп"
                        
                        value1 = bytes(await page.client_storage.get_async("encrypted_list"))
                        value2 = bytes(await page.client_storage.get_async("encryption_key"))
                        
                        decrypt = decrypt_list(value1, value2)
                 
                        main_pid = multiprocessing.Process(
                            target=pagination,
                            args=(decrypt, self.specialty.value, self.city.value, )
                        )

                        main_pid.start()

                        page.session.set('main_pid', main_pid.pid)

            else:

                main_pid = page.session.get('main_pid')
                if main_pid:
                    try:
                        os.kill(main_pid, signal.SIGTERM)
                    except ProcessLookupError:
                        print(f"Process with PID {main_pid} not found")

                self.start_button.style.bgcolor = {"": "#4CAF50"}
                self.start_button.text = "Старт"
            await self.start_button.update_async()

        async def dropdown_changed(self, e):
            self.divider_1.visible = True
            self.divider_2.visible = True
            self.divider_3.visible = True
            self.divider_4.visible = True
            
            self.dropdown.visible = True
            self.specialty.visible = True
            
            self.city.visible = True
                                
            self.start_button.visible = True
            self.start_button.disabled = not self.dropdown.value
            
            await page.update_async()

    parsing_instance = ParsingMenu(page)
    phone_instance = PhoneSendWhatsApp(page)
    register_instance = RegisterCapthca(page)
    gorodrabot_instance = GorodRabot(page)
    return ft.Container(
        content=ft.Container(
            content=ft.Column(
                [
                    parsing_instance.logo,
                    parsing_instance.title,
                    parsing_instance.subtitle,
                    ft.Container(height=20),
                    parsing_instance.platform_menu, 
                    phone_instance.platform_menu,
                    register_instance.platform_menu,
                    gorodrabot_instance.platform_menu,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=300,  # Ограничиваем ширину содержимого
            alignment=ft.alignment.center
        ),
        expand=True,
        alignment=ft.alignment.center,  # Центрируем внутренний контейнер
        padding=40,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#F0F4F8", "#E2E8F0"]
        )
    )