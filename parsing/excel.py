import pandas as pd
from parsing.rest_api.api import send_message


def read_excel_phone_numbers(file_path, instance_id, access_token, message):
    """
    Читает телефонные номера из всех столбцов Excel файла и возвращает их в виде списка
    
    Parameters:
    file_path (str): Путь к Excel файлу
    
    Returns:
    list: Список телефонных номеров
    """
    try:
        # Читаем Excel файл
        df = pd.read_excel(rf'{file_path}')
        
        phone_numbers = []
        
        # Проходим по всем столбцам
        for column in df.columns:
            # Преобразуем столбец в строки и собираем все непустые значения
            numbers = df[column].dropna().astype(str).tolist()
            
            # Очищаем номера от лишних символов и пробелов
            for number in numbers:
                # Убираем пробелы, тире, скобки и плюс в начале
                cleaned_number = ''.join(c for c in number if c.isdigit())
                
                # Проверяем, что строка содержит достаточно цифр (7-15 цифр считаем телефоном)
                if len(cleaned_number) >= 7 and len(cleaned_number) <= 15:
                    phone_numbers.append(cleaned_number)
        
        # Удаляем дубликаты
        phone_numbers = list(set(phone_numbers))
        for i in phone_numbers:
            send_message(i, message, instance_id, access_token)
    
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {str(e)}")
        return []
