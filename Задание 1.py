# -*- coding: utf-8 -*-

import time

class AuthSystem:
    def __init__(self, max_attempts=3, lockout_time=60):
        self.max_attempts = max_attempts
        self.lockout_time = lockout_time
        self.attempts = {}

    def is_locked(self, ip):
        if ip in self.attempts:
            attempts_count, lockout_timestamp = self.attempts[ip]
            if time.time() < lockout_timestamp:
                return True
        return False

    def record_attempt(self, ip, success):
        if success:
            if ip in self.attempts:
                del self.attempts[ip]
        else:
            if ip not in self.attempts:
                self.attempts[ip] = (1, 0)
            else:
                attempts_count, lockout_timestamp = self.attempts[ip]
                attempts_count += 1
                if attempts_count >= self.max_attempts:
                    lockout_timestamp = time.time() + self.lockout_time
                self.attempts[ip] = (attempts_count, lockout_timestamp)

    def can_attempt(self, ip):
        if self.is_locked(ip):
            print(f"IP {str(ip)} is temporarily locked due to multiple failed attempts.")
            return False
        return True

    def authenticate(self, username, password):
        return username == "admin" and password == "admin"

    def login(self, ip, username, password):
        if not self.can_attempt(ip):
            return False
        success = self.authenticate(username, password)
        self.record_attempt(ip, success)
        return success

# Пример использования
auth_system = AuthSystem()

def test_auth_system(auth_system):
    ip = '192.168.1.1'
    
    # Первая неудачная попытка
    result = auth_system.login(ip, 'admin', 'wrong_password')
    print(f"Попытка 1 (неправильный пароль): {'Успешно' if result else 'Неудачно'}")
    
    # Вторая неудачная попытка
    result = auth_system.login(ip, 'admin', 'wrong_password')
    print(f"Попытка 2 (неправильный пароль): {'Успешно' if result else 'Неудачно'}")
    
    # Третья неудачная попытка
    result = auth_system.login(ip, 'admin', 'wrong_password')
    print(f"Попытка 3 (неправильный пароль): {'Успешно' if result else 'Неудачно'}")
    
    # Четвертая попытка (превышено максимальное количество попыток)
    result = auth_system.login(ip, 'admin', 'admin')
    print(f"Попытка 4 (правильный пароль, но IP заблокирован): {'Успешно' if result else 'Неудачно'}")
    
    # Подождите время блокировки перед следующей попыткой
    print("Ожидание времени блокировки...")
    time.sleep(auth_system.lockout_time + 1)

    # Пятая попытка (после окончания времени блокировки)
    result = auth_system.login(ip, 'admin', 'admin')
    print(f"Попытка 5 (правильный пароль после окончания блокировки): {'Успешно' if result else 'Неудачно'}")

# Запуск теста
test_auth_system(auth_system)