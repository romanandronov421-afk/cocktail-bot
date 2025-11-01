#!/usr/bin/env python3
"""
Запуск бота MIXTRIX напрямую через Python
"""

import os
import sys
import asyncio
from datetime import datetime

def log(message):
    """Логирование"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    """Основная функция запуска"""
    print("🍸 MIXTRIX Bot - Прямой запуск")
    print("=" * 40)
    
    # Проверяем файлы
    if not os.path.exists('bot.py'):
        print("❌ Файл bot.py не найден!")
        input("Нажмите Enter для выхода...")
        return
    
    if not os.path.exists('env_file.txt'):
        print("❌ Файл env_file.txt не найден!")
        input("Нажмите Enter для выхода...")
        return
    
    print("✅ Все файлы найдены")
    
    # Проверяем переменные окружения
    try:
        from dotenv import load_dotenv
        load_dotenv('env_file.txt')
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if token:
            print("✅ Telegram Bot Token настроен")
        else:
            print("❌ Telegram Bot Token не настроен!")
            input("Нажмите Enter для выхода...")
            return
            
    except Exception as e:
        print(f"❌ Ошибка загрузки переменных: {e}")
        input("Нажмите Enter для выхода...")
        return
    
    print("\n🎯 Возможности бота:")
    print("• Фудпейринг на основе The Flavor Bible")
    print("• 300+ вкусовых комбинаций")
    print("• Интеграция всех профессиональных источников")
    print("• Сезонные рекомендации для России")
    
    print("\n🚀 Запуск бота...")
    print("📱 Для остановки нажмите Ctrl+C")
    print("=" * 40)
    
    try:
        # Импортируем и запускаем бота
        import bot
        print("✅ Бот успешно импортирован!")
        print("🎉 MIXTRIX Bot работает!")
        print("\n📱 Теперь вы можете:")
        print("• Найти бота в Telegram")
        print("• Отправить /start")
        print("• Использовать команды фудпейринга")
        
        # Запускаем основной цикл бота
        asyncio.run(bot.main())
        
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка запуска бота: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()






