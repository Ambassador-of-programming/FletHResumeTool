import pandas as pd
import os


def save_excel(fio: str, phone: str, adress: str, spesiolist: str, date_birth: str, famaly_status: str, edu: str, lang: str):
    # Путь к файлу
    file_path = 'HR_Excel.xlsx'

    # Новые данные для сохранения
    new_data = {
        'ФИО': fio,
        'Номер телефона': phone,
        'Адрес': adress,
        'Специальность': spesiolist,
        'Дата рождения': date_birth,
        'Семейный статус': famaly_status,
        'Образование': edu,
        'Языки': lang,
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
