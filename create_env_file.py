#!/usr/bin/env python3
"""
Скрипт для создания файла .env
"""

import os
import shutil

def create_env_file():
    """Создание файла .env из env_final.txt"""
    print("🔧 Создание файла .env...")
    
    try:
        # Копируем env_final.txt в .env
        shutil.copy('env_final.txt', '.env')
        print("✅ Файл .env успешно создан!")
        
        # Проверяем, что файл создался
        if os.path.exists('.env'):
            print("✅ Файл .env существует и готов к использованию!")
            return True
        else:
            print("❌ Файл .env не был создан!")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при создании файла .env: {e}")
        return False

def main():
    """Основная функция"""
    print("🍹 MixMatrixBot - Создание файла .env")
    print("=" * 50)
    
    if create_env_file():
        print("\n🎉 Готово!")
        print("📋 Теперь вы можете запустить бота:")
        print("1. Активируйте виртуальную среду: venv\\Scripts\\activate")
        print("2. Запустите бота: python run_bot.py")
        print("\n📱 Найдите вашего бота в Telegram и отправьте /start")
    else:
        print("\n❌ Не удалось создать файл .env")
        print("📝 Создайте файл .env вручную, скопировав содержимое из env_final.txt")

if __name__ == "__main__":
    main()
















