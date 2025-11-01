#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os

def install_package(package):
    """Установка пакета через pip"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Основная функция"""
    print("=== Установка зависимостей и запуск бота ===")
    
    # Список пакетов для установки
    packages = ['aiogram', 'requests', 'python-dotenv']
    
    print("Устанавливаем зависимости...")
    for package in packages:
        print(f"Устанавливаем {package}...")
        if install_package(package):
            print(f"✓ {package} установлен")
        else:
            print(f"✗ Ошибка установки {package}")
            return
    
    print("\n✓ Все зависимости установлены!")
    
    # Проверяем файл с токенами
    print("\nПроверяем файл env_file.txt...")
    if not os.path.exists('env_file.txt'):
        print("✗ Файл env_file.txt не найден!")
        return
    
    print("✓ Файл env_file.txt найден")
    
    # Проверяем упрощенного бота
    print("\nПроверяем файл bot_simple.py...")
    if not os.path.exists('bot_simple.py'):
        print("✗ Файл bot_simple.py не найден!")
        return
    
    print("✓ Файл bot_simple.py найден")
    
    # Запускаем бота
    print("\n🚀 Запускаем бота...")
    try:
        subprocess.run([sys.executable, 'bot_simple.py'])
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка запуска бота: {e}")

if __name__ == "__main__":
    main()