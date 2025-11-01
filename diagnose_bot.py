#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
from dotenv import load_dotenv

def test_imports():
    """Тест импортов"""
    print("=== Тест импортов ===")
    
    try:
        import asyncio
        print("✓ asyncio")
    except ImportError as e:
        print(f"✗ asyncio: {e}")
        return False

    try:
        from aiogram import Bot, Dispatcher, types
        print("✓ aiogram")
    except ImportError as e:
        print(f"✗ aiogram: {e}")
        return False

    try:
        import requests
        print("✓ requests")
    except ImportError as e:
        print(f"✗ requests: {e}")
        return False

    try:
        from database import CocktailDatabase
        print("✓ database")
    except ImportError as e:
        print(f"✗ database: {e}")
        return False

    try:
        from hybrid_processor import HybridCocktailProcessor
        print("✓ hybrid_processor")
    except ImportError as e:
        print(f"✗ hybrid_processor: {e}")
        return False

    try:
        from cocktail_party_processor import CocktailPartyProcessor
        print("✓ cocktail_party_processor")
    except ImportError as e:
        print(f"✗ cocktail_party_processor: {e}")
        return False

    return True

def test_environment():
    """Тест переменных окружения"""
    print("\n=== Тест переменных окружения ===")
    
    try:
        load_dotenv('env_file.txt')
        print("✓ Переменные окружения загружены")
    except Exception as e:
        print(f"✗ Ошибка загрузки переменных: {e}")
        return False

    required_vars = ['TELEGRAM_BOT_TOKEN', 'YANDEX_API_KEY', 'FOLDER_ID']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {'*' * 10}...{value[-4:]}")
        else:
            print(f"✗ {var}: НЕ НАЙДЕН")
            return False

    return True

async def test_telegram_api():
    """Тест подключения к Telegram API"""
    print("\n=== Тест Telegram API ===")
    
    try:
        from aiogram import Bot
        
        bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
        
        try:
            bot_info = await bot.get_me()
            print(f"✓ Telegram API: @{bot_info.username} ({bot_info.first_name})")
            return True
        except Exception as e:
            print(f"✗ Telegram API: {e}")
            return False
        finally:
            await bot.session.close()
            
    except Exception as e:
        print(f"✗ Ошибка тестирования Telegram API: {e}")
        return False

def test_yandex_api():
    """Тест Yandex API"""
    print("\n=== Тест Yandex API ===")
    
    try:
        import requests
        
        headers = {
            "Authorization": f"Api-Key {os.getenv('YANDEX_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        data = {
            "modelUri": f"gpt://{os.getenv('FOLDER_ID')}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 100
            },
            "messages": [
                {
                    "role": "user",
                    "text": "Привет! Это тест подключения."
                }
            ]
        }
        
        response = requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✓ Yandex API: подключение успешно")
            return True
        else:
            print(f"✗ Yandex API: HTTP {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Ошибка тестирования Yandex API: {e}")
        return False

def test_database():
    """Тест базы данных"""
    print("\n=== Тест базы данных ===")
    
    try:
        from database import CocktailDatabase
        
        db = CocktailDatabase()
        print("✓ База данных инициализирована")
        
        # Проверяем, есть ли рецепты
        recipes = db.get_all_recipes()
        print(f"✓ Найдено рецептов: {len(recipes)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Ошибка базы данных: {e}")
        return False

async def main():
    """Основная функция тестирования"""
    print("=== Диагностика бота MixMatrix ===")
    
    # Тест импортов
    if not test_imports():
        print("\n❌ КРИТИЧЕСКАЯ ОШИБКА: Проблемы с импортами")
        return
    
    # Тест переменных окружения
    if not test_environment():
        print("\n❌ КРИТИЧЕСКАЯ ОШИБКА: Проблемы с переменными окружения")
        return
    
    # Тест базы данных
    if not test_database():
        print("\n⚠️ ПРЕДУПРЕЖДЕНИЕ: Проблемы с базой данных")
    
    # Тест Telegram API
    if not await test_telegram_api():
        print("\n❌ КРИТИЧЕСКАЯ ОШИБКА: Проблемы с Telegram API")
        return
    
    # Тест Yandex API
    if not test_yandex_api():
        print("\n⚠️ ПРЕДУПРЕЖДЕНИЕ: Проблемы с Yandex API")
    
    print("\n=== Результат диагностики ===")
    print("✓ Все основные компоненты работают")
    print("✓ Бот готов к запуску")
    print("\nДля запуска бота используйте: python bot.py")

if __name__ == "__main__":
    asyncio.run(main())









