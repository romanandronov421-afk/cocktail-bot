#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания файла .env
"""

import os

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

if __name__ == "__main__":
    print("🚀 Создание файла .env...")
    if create_env_file():
        print("🎉 Готово! Теперь можно запускать бота: python main.py")
    else:
        print("💡 Попробуйте создать файл .env вручную, скопировав содержимое из env_new_file.txt")



