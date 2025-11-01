#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой скрипт для запуска MixMatrixBot
"""

import os
import sys
import shutil

def main():
    print("🚀 Запуск MixMatrixBot...")
    
    # Проверяем наличие файла .env
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        
        # Проверяем наличие env_ready.txt
        if os.path.exists('env_ready.txt'):
            print("📝 Найден файл env_ready.txt, копируем в .env...")
            try:
                shutil.copy('env_ready.txt', '.env')
                print("✅ Файл .env создан!")
            except Exception as e:
                print(f"❌ Ошибка при создании .env: {e}")
                return
        else:
            print("❌ Файл env_ready.txt также не найден!")
            print("📝 Создайте файл .env с содержимым:")
            print("BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q")
            print("YANDEX_API_KEY=ajegpjgsbgidg7av4mfj")
            print("FOLDER_ID=ajels2ea51569prr6uvb")
            return
    
    # Проверяем наличие main.py
    if not os.path.exists('main.py'):
        print("❌ Файл main.py не найден!")
        return
    
    print("✅ Все файлы найдены!")
    print("🚀 Запускаем бота...")
    
    # Запускаем main.py
    try:
        import main
        print("✅ Бот запущен!")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        print("💡 Попробуйте запустить: python main.py")

if __name__ == "__main__":
    main()
















