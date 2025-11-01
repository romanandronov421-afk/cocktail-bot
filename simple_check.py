#!/usr/bin/env python3
"""Простая проверка готовности бота к запуску"""

print("🔍 Проверка готовности бота...")
print("=" * 50)

# 1. Проверка файлов
import os
files_to_check = ['bot.py', 'env_file.txt', 'database.py', 'cocktails.db']
print("\n📁 Проверка файлов:")
for file in files_to_check:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} - НЕ НАЙДЕН")

# 2. Проверка переменных окружения
print("\n🔐 Проверка переменных окружения:")
try:
    from dotenv import load_dotenv
    load_dotenv('env_file.txt')
    
    import os
    vars_to_check = {
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'YANDEX_API_KEY': os.getenv('YANDEX_API_KEY'),
        'FOLDER_ID': os.getenv('FOLDER_ID')
    }
    
    for var, value in vars_to_check.items():
        if value:
            print(f"  ✅ {var}: установлено ({len(value)} символов)")
        else:
            print(f"  ❌ {var}: НЕ УСТАНОВЛЕНО")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

# 3. Проверка импортов
print("\n📦 Проверка основных импортов:")
try:
    import asyncio
    print("  ✅ asyncio")
    
    from aiogram import Bot, Dispatcher
    print("  ✅ aiogram")
    
    import requests
    print("  ✅ requests")
    
    print("  ✅ Все основные библиотеки установлены")
except ImportError as e:
    print(f"  ❌ Ошибка импорта: {e}")

# 4. Проверка структуры bot.py
print("\n📄 Проверка структуры bot.py:")
try:
    with open('bot.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    checks = {
        'RUSSIAN_HORECA_SOURCES': 'RUSSIAN_HORECA_SOURCES' in content,
        'get_russian_horeca_news': 'def get_russian_horeca_news' in content or 'async def get_russian_horeca_news' in content,
        'news_command': '@dp.message(Command(\'news\'))' in content or "Command('news')" in content,
        'if __name__': 'if __name__ == \'__main__\':' in content
    }
    
    for name, found in checks.items():
        if found:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} - НЕ НАЙДЕНО")
            
except Exception as e:
    print(f"  ❌ Ошибка чтения bot.py: {e}")

print("\n" + "=" * 50)
print("✅ Проверка завершена!")
print("\nДля запуска бота используйте:")
print("  python bot.py")
print("=" * 50)
