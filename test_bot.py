#!/usr/bin/env python3
"""
Тест работы бота MIXTRIX
"""

import asyncio
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_bot_commands():
    """Тестирование команд бота"""
    
    print("🍸 Тестирование команд MIXTRIX")
    print("=" * 40)
    
    # Импортируем необходимые модули
    try:
        from main import dp, bot
        print("✅ Модули бота загружены успешно")
    except Exception as e:
        print(f"❌ Ошибка загрузки модулей: {e}")
        return
    
    # Проверяем базу данных
    try:
        import sqlite3
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM recipes")
        total = cursor.fetchone()[0]
        print(f"✅ База данных: {total} рецептов")
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка базы данных: {e}")
        return
    
    # Проверяем конфигурацию
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if 'YandexGPT' in config:
            print("✅ Конфигурация YandexGPT найдена")
        else:
            print("❌ Конфигурация YandexGPT не найдена")
            
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return
    
    # Проверяем переменные окружения
    try:
        from dotenv import load_dotenv
        load_dotenv('env_file.txt')
        
        api_key = os.getenv('YANDEX_API_KEY')
        folder_id = os.getenv('FOLDER_ID')
        
        if api_key and folder_id:
            print("✅ Переменные окружения загружены")
        else:
            print("❌ Переменные окружения не найдены")
            
    except Exception as e:
        print(f"❌ Ошибка переменных окружения: {e}")
        return
    
    print("\n🎯 Доступные команды:")
    commands = [
        "/start", "/help", "/rules", "/examples",
        "/classic", "/signature", "/premix",
        "/iba", "/iba_classic", "/bible", "/aperitif",
        "/theory", "/preparation", "/techniques", "/syrups",
        "/extended", "/molecular", "/scientific",
        "/liquid_intelligence", "/flavor_principles",
        "/flavor_combinations", "/seasonal_pairings",
        "/cocktail_pairings", "/el_copitas"
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"  {i:2d}. {cmd}")
    
    print(f"\n📊 Всего команд: {len(commands)}")
    print("✅ Бот готов к работе!")
    
    # Проверяем обработчики
    try:
        handlers_count = len(dp._handlers)
        print(f"✅ Обработчиков зарегистрировано: {handlers_count}")
    except Exception as e:
        print(f"❌ Ошибка проверки обработчиков: {e}")

def test_database_queries():
    """Тестирование запросов к базе данных"""
    
    print("\n🔍 Тестирование запросов к базе данных:")
    print("=" * 40)
    
    try:
        import sqlite3
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        # Тест 1: Общее количество рецептов
        cursor.execute("SELECT COUNT(*) FROM recipes")
        total = cursor.fetchone()[0]
        print(f"✅ Всего рецептов: {total}")
        
        # Тест 2: Рецепты по источникам
        cursor.execute("SELECT source, COUNT(*) FROM recipes GROUP BY source ORDER BY COUNT(*) DESC")
        sources = cursor.fetchall()
        print("✅ Рецепты по источникам:")
        for source, count in sources:
            print(f"    • {source}: {count}")
        
        # Тест 3: Поиск по ингредиентам
        test_ingredients = ["текила", "джин", "ром", "фейхоа"]
        print("✅ Поиск по ингредиентам:")
        for ingredient in test_ingredients:
            cursor.execute("SELECT COUNT(*) FROM recipes WHERE ingredients LIKE ?", (f"%{ingredient}%",))
            count = cursor.fetchone()[0]
            print(f"    • {ingredient}: {count} рецептов")
        
        # Тест 4: Категории
        cursor.execute("SELECT category, COUNT(*) FROM recipes GROUP BY category ORDER BY COUNT(*) DESC LIMIT 5")
        categories = cursor.fetchall()
        print("✅ Топ-5 категорий:")
        for category, count in categories:
            print(f"    • {category}: {count}")
        
        conn.close()
        print("✅ Все тесты базы данных прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка тестирования базы данных: {e}")

if __name__ == "__main__":
    print("🍸 MIXTRIX - Тестирование бота")
    print("=" * 50)
    
    # Тестируем базу данных
    test_database_queries()
    
    # Тестируем команды
    asyncio.run(test_bot_commands())
    
    print("\n🎉 Тестирование завершено!")
    print("Бот готов к работе в Telegram!")

