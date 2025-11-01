#!/usr/bin/env python3
"""
Простой скрипт для запуска MixMatrixBot
"""

import os
import sys
import asyncio

def check_environment():
    """Проверка окружения"""
    print("🔍 Проверка окружения...")
    
    # Проверяем наличие файла .env
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("📝 Создайте файл .env с содержимым:")
        print("TELEGRAM_BOT_TOKEN=ваш_telegram_токен")
        print("YANDEX_API_KEY=ajegpjgsbgidg7av4mfj")
        print("FOLDER_ID=ajels2ea51569prr6uvb")
        return False
    
    # Проверяем наличие виртуальной среды
    if not os.path.exists('venv'):
        print("❌ Виртуальная среда не найдена!")
        print("📝 Создайте виртуальную среду:")
        print("python -m venv venv")
        print("venv\\Scripts\\activate")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ Окружение готово!")
    return True

def main():
    """Основная функция"""
    print("🍹 MixMatrixBot - Проверка готовности")
    print("=" * 50)
    
    if not check_environment():
        print("\n❌ Бот не готов к запуску!")
        print("Исправьте ошибки выше и попробуйте снова.")
        return
    
    print("\n✅ Бот готов к запуску!")
    print("📋 Инструкции по запуску:")
    print("1. Активируйте виртуальную среду:")
    print("   venv\\Scripts\\activate")
    print("2. Запустите бота:")
    print("   python run_bot.py")
    print("\n🎯 Или используйте команду:")
    print("   venv\\Scripts\\python.exe run_bot.py")
    
    print("\n📱 Не забудьте:")
    print("• Получить TELEGRAM_BOT_TOKEN от @BotFather")
    print("• Получить XAI_API_KEY от x.ai")
    print("• Создать файл .env с токенами")

if __name__ == "__main__":
    main()
