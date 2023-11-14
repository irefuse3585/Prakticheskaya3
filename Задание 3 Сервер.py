from flask import Flask, request
import hashlib
import time

app = Flask(__name__)

# Предположим, что у нас есть база данных пользователей
# Здесь это просто словарь для примера
users = {
    'user1': {
        'password': '5f4dcc3b5aa765d61d8327deb882cf99',  # пример хэша для пароля
        'last_attempt_time': 0
    }
}

@app.route('/')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if username in users:
        # Проверка времени между попытками входа
        current_time = time.time()
        if current_time - users[username]['last_attempt_time'] < 60:  # 60 секунд задержки
            return 'Слишком много попыток, попробуйте позже', 429

        users[username]['last_attempt_time'] = current_time

        # Проверка пароля
        password_hash = hashlib.md5(password.encode()).hexdigest()
        if password_hash == users[username]['password']:
            return 'Успешный вход в систему', 200
        else:
            return 'Неверный пароль', 401
    else:
        return 'Пользователь не найден', 404

app.run(debug=True)