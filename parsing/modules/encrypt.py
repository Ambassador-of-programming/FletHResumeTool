from cryptography.fernet import Fernet
import json

def encrypt_list(input_list):
    # Генерируем ключ
    key = Fernet.generate_key()
    
    # Создаем шифратор
    f = Fernet(key)
    
    # Преобразуем список в строку JSON
    list_string = json.dumps(input_list)
    
    # Шифруем
    encrypted = f.encrypt(list_string.encode())
    
    return encrypted, key

def decrypt_list(encrypted_list, encryption_key):
    # Создаем дешифратор
    f = Fernet(encryption_key)
    
    # Дешифруем
    decrypted_string = f.decrypt(encrypted_list).decode()
    
    # Преобразуем обратно в список
    decrypted_list = json.loads(decrypted_string)
    
    return decrypted_list

# # Пример использования
# my_list = ['1', '2', '3']

# # Шифрование
# encrypted_list, encryption_key = encrypt_list(my_list)
# print("Зашифрованный список:", encrypted_list)
# print("Зашифрованный encryption_key:", encryption_key)


# # Дешифрование
# decrypted_list = decrypt_list(encrypted_list, encryption_key)
# print("Расшифрованный список:", decrypted_list)
# print(type(decrypted_list))