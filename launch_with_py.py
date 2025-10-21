#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Запуск MixMatrixBot через функцию py
"""

import os
import shutil
import subprocess
import sys

def create_env_file():
    """Создает файл .env из env_file.txt"""
    try:
        if os.path.exists('env_file.txt'):
            shutil.copy('env_file.txt', '.env')
            print("✅ Файл .env создан из env_file.txt")
            return True
        else:
            # Создаем .env напрямую
            env_content = """YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb
TELEGRAM_BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q
DEFAULT_MODEL=yandexgpt
DEFAULT_MAX_TOKENS=1000
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9"""
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)
            print("✅ Файл .env создан напрямую")
            return True
    except Exception as e:
        print(f"❌ Ошибка создания .env: {e}")
        return False

def launch_bot_with_py():
    """Запускает бота через функцию py"""
    try:
        print("🚀 Запуск бота через py...")
        
        # Проверяем наличие main.py
        if not os.path.exists('main.py'):
            print("❌ Файл main.py не найден!")
            return False
        
        # Запускаем через py
        result = subprocess.run(['py', 'main.py'], 
                              capture_output=False, 
                              text=True, 
                              cwd=os.getcwd())
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print("❌ Команда 'py' не найдена!")
        print("💡 Попробуйте использовать 'python' вместо 'py'")
        return False
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        return False

def main():
    print("🍹 MixMatrixBot - Запуск через py")
    print("=" * 40)
    
    # Создаем .env
    if not create_env_file():
        print("❌ Не удалось создать .env!")
        return
    
    # Запускаем бота
    print("\n🚀 Запуск бота...")
    print("📱 Найдите бота в Telegram и отправьте /start")
    print("🛑 Для остановки нажмите Ctrl+C")
    print("-" * 40)
    
    if launch_bot_with_py():
        print("✅ Бот успешно запущен!")
    else:
        print("❌ Не удалось запустить бота!")

if __name__ == "__main__":
    main()



