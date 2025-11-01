#!/usr/bin/env python3
"""
Простой тест для проверки работы бота
"""

import os
import sys

def test_imports():
    """Тест импортов"""
    print("🔍 Тестирование импортов...")
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта dotenv: {e}")
        return False
    
    try:
        import aiogram
        print("✅ aiogram импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта aiogram: {e}")
        return False
    
    try:
        import requests
        print("✅ requests импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта requests: {e}")
        return False
    
    return True

def test_environment():
    """Тест переменных окружения"""
    print("\n🔍 Тестирование переменных окружения...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv('env_file.txt')
        
        api_key = os.getenv('YANDEX_API_KEY')
        folder_id = os.getenv('FOLDER_ID')
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if api_key:
            print("✅ YANDEX_API_KEY найден")
        else:
            print("❌ YANDEX_API_KEY не найден")
            
        if folder_id:
            print("✅ FOLDER_ID найден")
        else:
            print("❌ FOLDER_ID не найден")
            
        if bot_token:
            print("✅ TELEGRAM_BOT_TOKEN найден")
        else:
            print("❌ TELEGRAM_BOT_TOKEN не найден")
            
        return bool(api_key and folder_id and bot_token)
        
    except Exception as e:
        print(f"❌ Ошибка загрузки переменных окружения: {e}")
        return False

def test_database():
    """Тест базы данных"""
    print("\n🔍 Тестирование базы данных...")
    
    try:
        import sqlite3
        
        if not os.path.exists('cocktails.db'):
            print("❌ Файл cocktails.db не найден")
            return False
            
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        # Проверяем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✅ Найдено таблиц: {len(tables)}")
        
        for table in tables:
            print(f"   • {table[0]}")
        
        # Проверяем рецепты
        if ('recipes',) in tables:
            cursor.execute("SELECT COUNT(*) FROM recipes")
            count = cursor.fetchone()[0]
            print(f"✅ Рецептов в БД: {count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка работы с БД: {e}")
        return False

def test_bot_modules():
    """Тест модулей бота"""
    print("\n🔍 Тестирование модулей бота...")
    
    try:
        from database import CocktailDatabase
        print("✅ CocktailDatabase импортирован")
        
        db = CocktailDatabase()
        print("✅ База данных инициализирована")
        
        recipes = db.get_all_recipes()
        print(f"✅ Получено рецептов: {len(recipes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка модулей бота: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🍸 MIXTRIX Bot - Проверка работоспособности")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_environment,
        test_database,
        test_bot_modules
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Результаты: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Бот готов к работе!")
        return True
    else:
        print("⚠️ Некоторые тесты не пройдены. Проверьте конфигурацию.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)











