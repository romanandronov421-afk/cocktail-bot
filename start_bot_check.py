#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Быстрая проверка и запуск бота"""
import os
import sys

print("=" * 60)
print("ПРОВЕРКА И ЗАПУСК COCKTAIL BOT")
print("=" * 60)

# Проверка файла env_file.txt
if not os.path.exists('env_file.txt'):
    print("❌ Файл env_file.txt не найден!")
    sys.exit(1)
print("✓ env_file.txt найден")

# Проверка bot.py
if not os.path.exists('bot.py'):
    print("❌ Файл bot.py не найден!")
    sys.exit(1)
print("✓ bot.py найден")

# Проверка зависимостей
print("\nПроверка зависимостей:")
try:
    import aiogram
    print("✓ aiogram установлен")
except ImportError:
    print("❌ aiogram не установлен")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv установлен")
except ImportError:
    print("❌ python-dotenv не установлен")
    sys.exit(1)

# Проверка переменных окружения
load_dotenv('env_file.txt')
token = os.getenv('TELEGRAM_BOT_TOKEN')
yandex_key = os.getenv('YANDEX_API_KEY')
folder_id = os.getenv('FOLDER_ID')

print("\nПроверка переменных окружения:")
if token:
    print(f"✓ TELEGRAM_BOT_TOKEN: OK ({len(token)} символов)")
else:
    print("❌ TELEGRAM_BOT_TOKEN отсутствует")
    sys.exit(1)

if yandex_key:
    print(f"✓ YANDEX_API_KEY: OK ({len(yandex_key)} символов)")
else:
    print("❌ YANDEX_API_KEY отсутствует")
    sys.exit(1)

if folder_id:
    print(f"✓ FOLDER_ID: OK")
else:
    print("❌ FOLDER_ID отсутствует")
    sys.exit(1)

# Проверка базы данных
print("\nПроверка базы данных:")
if os.path.exists('cocktails.db'):
    print("✓ cocktails.db существует")
else:
    print("⚠️  cocktails.db не найден (будет создан при первом запуске)")

print("\n" + "=" * 60)
print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ")
print("=" * 60)
print("\n🚀 Запуск бота...\n")

# Запуск бота
print("\n⚠️  Для остановки бота нажмите Ctrl+C\n")
try:
    # Прямой импорт и запуск
    import asyncio
    import importlib.util
    
    spec = importlib.util.spec_from_file_location("bot", "bot.py")
    bot_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot_module)
    
except KeyboardInterrupt:
    print("\n\n🛑 Бот остановлен пользователем")
    sys.exit(0)
except Exception as e:
    print(f"\n\n❌ Ошибка при запуске: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

