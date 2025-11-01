#!/usr/bin/env python3
"""
Скрипт для создания файла .env
"""

import os

def create_env_file():
    """Создание файла .env"""
    print("🔧 Создание файла .env...")
    
    env_content = """BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q
YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Файл .env создан!")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании .env: {e}")
        return False

def main():
    """Основная функция"""
    print("🍹 MixMatrixBot - Создание файла .env")
    print("=" * 50)
    
    if create_env_file():
        print("\n🎉 Готово!")
        print("📋 Теперь вы можете запустить бота:")
        print("python main.py")
    else:
        print("\n❌ Не удалось создать файл .env")
        print("📝 Создайте файл .env вручную, скопировав содержимое из env_new.txt")

if __name__ == "__main__":
    main()
















