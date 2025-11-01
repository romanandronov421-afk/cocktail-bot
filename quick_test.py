#!/usr/bin/env python3
"""Быстрый тест основных функций бота"""

import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Проверка импортов...")
    from dotenv import load_dotenv
    load_dotenv('env_file.txt')
    
    print("Проверка переменных...")
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    yandex_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('FOLDER_ID')
    
    if token and yandex_key and folder_id:
        print("✅ Все переменные найдены")
        print(f"Token: {token[:10]}...")
        print(f"Yandex key: {yandex_key[:10]}...")
        print(f"Folder ID: {folder_id}")
        print("\n✅ Бот готов к запуску!")
        print("\nЗапуск бота...")
        print("=" * 50)
        exec(open('bot.py').read())
    else:
        print("❌ Не все переменные найдены")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

