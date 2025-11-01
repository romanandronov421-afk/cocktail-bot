#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автономный скрипт для создания .env и запуска MixMatrixBot
"""

import os
import sys
import subprocess
import time

def create_env_file():
    """Создает файл .env с настройками бота"""
    
    env_content = """# Yandex Cloud AI API Configuration
YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q

# API Gateway Configuration (опционально)
API_GATEWAY_URL=https://your-api-gateway.url
API_GATEWAY_STAGING_URL=https://staging-api-gateway.url

# Model Configuration
DEFAULT_MODEL=yandexgpt
DEFAULT_MAX_TOKENS=1000
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9

# Cursor IDE Configuration
CURSOR_AI_PROVIDER=custom
CURSOR_AI_CUSTOM_API_URL=https://llm.api.cloud.yandex.net/foundationModels/v1/completion
CURSOR_AI_CUSTOM_API_KEY=ajegpjgsbgidg7av4mfj"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Файл .env успешно создан!")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании файла .env: {e}")
        return False

def check_dependencies():
    """Проверяет наличие необходимых зависимостей"""
    try:
        import aiogram
        import requests
        import sqlite3
        import configparser
        print("✅ Все зависимости установлены!")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("💡 Установите зависимости: pip install -r requirements.txt")
        return False

def start_bot():
    """Запускает бота"""
    try:
        print("🚀 Запускаем MixMatrixBot...")
        
        # Проверяем наличие main.py
        if not os.path.exists('main.py'):
            print("❌ Файл main.py не найден!")
            return False
        
        # Запускаем бота
        print("🎯 Бот запущен! Найдите его в Telegram и отправьте /start")
        print("📱 Команды бота:")
        print("   /recipe джин - создать рецепт с AI")
        print("   /seasonal - сезонные коктейли для октября")
        print("   /search текила - поиск в базе данных")
        print("   /menu conceptual 3 - концептуальное меню")
        print("\n🛑 Для остановки бота нажмите Ctrl+C")
        
        # Импортируем и запускаем main.py
        import main
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
        return True
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        return False

def main():
    """Основная функция"""
    print("🍹 MixMatrixBot - Автономный запуск")
    print("=" * 50)
    
    # Шаг 1: Создаем .env
    print("\n📝 Шаг 1: Создание файла .env...")
    if not create_env_file():
        print("❌ Не удалось создать файл .env!")
        return
    
    # Шаг 2: Проверяем зависимости
    print("\n🔍 Шаг 2: Проверка зависимостей...")
    if not check_dependencies():
        print("❌ Не все зависимости установлены!")
        return
    
    # Шаг 3: Запускаем бота
    print("\n🚀 Шаг 3: Запуск бота...")
    if not start_bot():
        print("❌ Не удалось запустить бота!")
        return
    
    print("\n🎉 MixMatrixBot успешно запущен!")

if __name__ == "__main__":
    main()
















