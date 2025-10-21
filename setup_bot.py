#!/usr/bin/env python3
"""
Скрипт для автоматической настройки MixMatrixBot
"""

import os
import shutil
import configparser

def create_env_file():
    """Создание файла .env"""
    print("🔧 Создание файла .env...")
    
    env_content = """BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q
YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Файл .env создан!")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании .env: {e}")
        return False

def setup_config():
    """Настройка конфигурации"""
    print("🔧 Настройка конфигурации...")
    
    # Копируем config.example.ini в config.ini если его нет
    if not os.path.exists('config.ini'):
        if os.path.exists('config.example.ini'):
            shutil.copy('config.example.ini', 'config.ini')
            print("✅ Файл config.ini создан из примера!")
        else:
            print("❌ Файл config.example.ini не найден!")
            return False
    else:
        print("✅ Файл config.ini уже существует!")
    
    return True

def create_data_folder():
    """Создание папки data"""
    print("📁 Создание структуры папок...")
    
    try:
        os.makedirs('data', exist_ok=True)
        print("✅ Папка data создана!")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании папки data: {e}")
        return False

def check_dependencies():
    """Проверка зависимостей"""
    print("📦 Проверка зависимостей...")
    
    try:
        import aiogram
        import requests
        import configparser
        print("✅ Все зависимости установлены!")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("📝 Установите зависимости: pip install -r requirements.txt")
        return False

def main():
    """Основная функция"""
    print("🍹 MixMatrixBot - Автоматическая настройка")
    print("=" * 50)
    
    success = True
    
    # Создание файла .env
    if not create_env_file():
        success = False
    
    # Настройка конфигурации
    if not setup_config():
        success = False
    
    # Создание папок
    if not create_data_folder():
        success = False
    
    # Проверка зависимостей
    if not check_dependencies():
        success = False
    
    if success:
        print("\n🎉 Настройка завершена успешно!")
        print("📋 Следующие шаги:")
        print("1. Активируйте виртуальную среду: venv\\Scripts\\activate")
        print("2. Запустите бота: python main.py")
        print("\n📱 Найдите вашего бота в Telegram и отправьте /start")
        print("🍂 Сезонные ингредиенты октября: Гранат, Клюква, Айва, Груша, Яблоки, Черноплодка, Рябина")
    else:
        print("\n❌ Настройка завершена с ошибками")
        print("📝 Проверьте ошибки выше и исправьте их")

if __name__ == "__main__":
    main()



