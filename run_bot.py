#!/usr/bin/env python3
"""
Скрипт для запуска MixMatrixBot
"""

import os
import sys
from database import init_sample_data

def main():
    """Основная функция запуска бота"""
    print("🍹 MixMatrixBot - Запуск...")
    
    # Проверяем наличие файла .env
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("Создайте файл .env с токенами:")
        print("TELEGRAM_BOT_TOKEN=ваш_токен")
        print("XAI_API_KEY=ваш_ключ")
        return
    
    # Проверяем наличие базы данных
    if not os.path.exists('cocktails.db'):
        print("📊 Инициализация базы данных...")
        init_sample_data()
    
    # Импортируем и запускаем бота
    try:
        from bot import executor, dp
        print("✅ Бот готов к работе!")
        print("Нажмите Ctrl+C для остановки")
        executor.start_polling(dp, skip_updates=True)
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что все зависимости установлены: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()
