#!/usr/bin/env python3
"""Проверка статуса бота"""

import os
import sys
from datetime import datetime

print("=" * 50)
print("🔍 ПРОВЕРКА СТАТУСА БОТА")
print("=" * 50)
print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 1. Проверка файлов
print("📁 Проверка файлов:")
files = ['bot.py', 'env_file.txt', 'database.py', 'cocktails.db']
for file in files:
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    print(f"  {status} {file}")

print()

# 2. Проверка переменных окружения
print("🔐 Проверка переменных окружения:")
try:
    from dotenv import load_dotenv
    load_dotenv('env_file.txt')
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    yandex = os.getenv('YANDEX_API_KEY')
    folder = os.getenv('FOLDER_ID')
    
    vars_ok = all([token, yandex, folder])
    if vars_ok:
        print("  ✅ Все переменные установлены")
        print(f"     Token: {token[:10]}... ({len(token)} символов)")
        print(f"     Yandex API: {yandex[:10]}... ({len(yandex)} символов)")
        print(f"     Folder ID: {folder}")
    else:
        print("  ❌ Некоторые переменные не установлены")
        if not token:
            print("     ❌ TELEGRAM_BOT_TOKEN")
        if not yandex:
            print("     ❌ YANDEX_API_KEY")
        if not folder:
            print("     ❌ FOLDER_ID")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

print()

# 3. Проверка процессов Python
print("🐍 Проверка процессов Python:")
try:
    import subprocess
    result = subprocess.run(['powershell', '-Command', 'Get-Process python -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count'], 
                          capture_output=True, text=True)
    count = result.stdout.strip()
    if count and count.isdigit() and int(count) > 0:
        print(f"  ✅ Найдено процессов Python: {count}")
        print("     Бот может быть запущен!")
    else:
        print("  ⚠️  Процессы Python не найдены")
        print("     Запустите бота: python bot.py")
except:
    print("  ⚠️  Не удалось проверить процессы")

print()
print("=" * 50)
print("📋 ИНСТРУКЦИЯ:")
print("=" * 50)
print("1. Откройте Telegram")
print("2. Найдите вашего бота")
print("3. Отправьте /start")
print("4. Проверьте команду /news")
print()
print("💡 Если бот не отвечает:")
print("   - Проверьте, что он запущен (python bot.py)")
print("   - Проверьте интернет-соединение")
print("   - Проверьте логи в консоли")
print("=" * 50)

