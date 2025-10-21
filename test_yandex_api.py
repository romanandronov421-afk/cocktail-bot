#!/usr/bin/env python3
"""
Тест Yandex Cloud AI API
"""

import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def test_yandex_api():
    """Тестирование Yandex Cloud AI API"""
    print("🧪 Тестирование Yandex Cloud AI API...")
    
    # Получаем данные из переменных окружения
    api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('FOLDER_ID')
    
    if not api_key or not folder_id:
        print("❌ Не найдены YANDEX_API_KEY или FOLDER_ID в переменных окружения")
        return False
    
    print(f"✅ API Key: {api_key[:10]}...")
    print(f"✅ Folder ID: {folder_id}")
    
    # URL для Yandex Cloud AI
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
            "maxTokens": 100
        },
        "messages": [
            {
                "role": "user",
                "text": "Привет! Создай простой рецепт коктейля с джином."
            }
        ]
    }
    
    try:
        print("📡 Отправляем запрос к Yandex API...")
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API работает!")
            print("📝 Ответ:")
            print(result.get('result', {}).get('alternatives', [{}])[0].get('message', {}).get('text', 'Нет ответа'))
            return True
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"📝 Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при обращении к API: {e}")
        return False

def main():
    """Основная функция"""
    print("🍹 MixMatrixBot - Тест Yandex API")
    print("=" * 50)
    
    # Проверяем наличие файла .env
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("📝 Создайте файл .env с содержимым:")
        print("YANDEX_API_KEY=ajegpjgsbgidg7av4mfj")
        print("FOLDER_ID=ajels2ea51569prr6uvb")
        print("TELEGRAM_BOT_TOKEN=ваш_telegram_токен")
        print("XAI_API_KEY=ваш_xai_ключ")
        return
    
    # Тестируем API
    if test_yandex_api():
        print("\n🎉 Yandex API работает корректно!")
        print("✅ Бот готов к запуску!")
    else:
        print("\n❌ Проблемы с Yandex API")
        print("🔧 Проверьте ключи и настройки")

if __name__ == "__main__":
    main()



