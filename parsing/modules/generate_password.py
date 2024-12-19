import random
import string

def generate_password(length=8):
    # Набор символов
    digits = string.digits  # 0-9
    uppercase_letters = string.ascii_uppercase  # A-Z
    lowercase_letters = string.ascii_lowercase  # a-z

    # Генерируем по одному символу каждого типа
    password = [
        random.choice(digits),
        random.choice(uppercase_letters),
        random.choice(lowercase_letters)
    ]

    # Добавляем оставшиеся случайные символы
    all_characters = digits + uppercase_letters + lowercase_letters
    password.extend(random.choice(all_characters) for _ in range(length - 3))

    # Перемешиваем пароль
    random.shuffle(password)

    # Преобразуем список символов в строку
    return ''.join(password)