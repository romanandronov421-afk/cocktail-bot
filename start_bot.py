#!/usr/bin/env python3
"""
Скрипт для запуска MixMatrixBot с готовыми настройками
"""

import os
import sys
import asyncio
import shutil

def setup_environment():
    """Настройка окружения"""
    print("🔧 Настройка окружения...")
    
    # Копируем env_final.txt в .env
    if os.path.exists('env_final.txt'):
        try:
            shutil.copy('env_final.txt', '.env')
            print("✅ Файл .env создан!")
        except Exception as e:
            print(f"❌ Ошибка при создании .env: {e}")
            return False
    else:
        print("❌ Файл env_final.txt не найден!")
        return False
    
    return True

def check_dependencies():
    """Проверка зависимостей"""
    print("📦 Проверка зависимостей...")
    
    try:
        import aiogram
        import requests
        import dotenv
        print("✅ Все зависимости установлены!")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("📝 Установите зависимости: pip install -r requirements.txt")
        return False

def test_yandex_api():
    """Тест Yandex API"""
    print("🧪 Тестирование Yandex API...")
    
    try:
        from dotenv import load_dotenv
        import requests
        
        load_dotenv()
        
        api_key = os.getenv('YANDEX_API_KEY')
        folder_id = os.getenv('FOLDER_ID')
        
        if not api_key or not folder_id:
            print("❌ Не найдены YANDEX_API_KEY или FOLDER_ID")
            return False
        
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Authorization": f"Api-Key {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "modelUri": f"gpt://{folder_id}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 50
            },
            "messages": [
                {
                    "role": "user",
                    "text": "Привет! Создай простой рецепт коктейля."
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            print("✅ Yandex API работает!")
            return True
        else:
            print(f"❌ Ошибка Yandex API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании API: {e}")
        return False

async def start_bot():
    """Запуск бота"""
    print("🍹 Запуск MixMatrixBot...")
    
    try:
        from bot import main as bot_main
        print("✅ Бот готов к работе!")
        print("📱 Найдите вашего бота в Telegram и отправьте /start")
        print("⏹️  Нажмите Ctrl+C для остановки")
        await bot_main()
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

def main():
    """Основная функция"""
    print("🍹 MixMatrixBot - Автоматический запуск")
    print("=" * 50)
    
    # Настройка окружения
    if not setup_environment():
        return
    
    # Проверка зависимостей
    if not check_dependencies():
        return
    
    # Тест API
    if not test_yandex_api():
        print("⚠️  Yandex API не работает, но бот может запуститься")
    
    # Запуск бота
    print("\n🚀 Запускаем бота...")
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":
    main()



