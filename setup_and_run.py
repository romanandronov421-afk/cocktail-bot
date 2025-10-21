#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание файла .env и запуск бота
"""

import os
import sys

def create_env():
    """Создает файл .env с правильными настройками"""
    env_content = """YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb
TELEGRAM_BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q
DEFAULT_MODEL=yandexgpt
DEFAULT_MAX_TOKENS=1000
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Файл .env создан успешно!")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания .env: {e}")
        return False

def main():
    print("🍹 MixMatrixBot - Настройка и запуск")
    print("=" * 40)
    
    # Создаем .env
    if not create_env():
        return
    
    # Проверяем main.py
    if not os.path.exists('main.py'):
        print("❌ Файл main.py не найден!")
        return
    
    print("🚀 Запускаем бота...")
    print("📱 Найдите бота в Telegram и отправьте /start")
    print("🛑 Для остановки нажмите Ctrl+C")
    print("-" * 40)
    
    # Запускаем main.py
    try:
        import main
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()



