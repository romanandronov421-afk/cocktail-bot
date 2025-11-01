#!/usr/bin/env python3
"""
Тестирование функций бота без подключения к Telegram
Проверяет основные функции: создание рецептов, новости, поиск и т.д.
"""

import asyncio
import sys
import os
from datetime import datetime

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_news_function():
    """Тест функции получения новостей"""
    print("\n" + "="*50)
    print("🧪 ТЕСТ: Получение новостей из российских источников")
    print("="*50)
    
    try:
        # Импортируем функцию из bot.py
        from dotenv import load_dotenv
        load_dotenv('env_file.txt')
        
        # Проверяем наличие источников
        import bot
        if hasattr(bot, 'RUSSIAN_HORECA_SOURCES'):
            sources = bot.RUSSIAN_HORECA_SOURCES
            print(f"✅ Найдено источников: {len(sources)}")
            for name, info in list(sources.items())[:3]:
                print(f"  - {info['name']}")
        
        # Тестируем функцию получения новостей
        if hasattr(bot, 'get_russian_horeca_news'):
            print("\n📰 Тестирую функцию get_russian_horeca_news()...")
            print("   (Это может занять 10-15 секунд)")
            
            news = await bot.get_russian_horeca_news()
            
            if news and "❌ Ошибка" not in news:
                print("✅ Новости получены успешно!")
                print(f"\n📄 Первые 200 символов:\n{news[:200]}...")
                return True
            else:
                print(f"⚠️  Получен ответ: {news[:100]}")
                return False
        else:
            print("❌ Функция get_russian_horeca_news не найдена")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_flavor_pairs():
    """Тест базы вкусовых сочетаний"""
    print("\n" + "="*50)
    print("🧪 ТЕСТ: База вкусовых сочетаний")
    print("="*50)
    
    try:
        import bot
        
        if hasattr(bot, 'FLAVOR_PAIRS'):
            pairs = bot.FLAVOR_PAIRS
            print(f"✅ Найдено вкусовых сочетаний: {len(pairs)}")
            
            # Проверяем несколько примеров
            test_flavors = ['яблоко', 'клубника', 'огурец', 'лимон']
            for flavor in test_flavors:
                if flavor in pairs:
                    combinations = pairs[flavor]
                    print(f"  ✅ {flavor}: {len(combinations)} сочетаний")
                    print(f"     Примеры: {', '.join(combinations[:3])}")
            
            return True
        else:
            print("❌ FLAVOR_PAIRS не найдено")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

async def test_seasonal_ingredients():
    """Тест сезонных ингредиентов"""
    print("\n" + "="*50)
    print("🧪 ТЕСТ: Сезонные ингредиенты")
    print("="*50)
    
    try:
        import bot
        
        if hasattr(bot, 'SEASONAL_INGREDIENTS'):
            seasons = bot.SEASONAL_INGREDIENTS
            current_season = getattr(bot, 'CURRENT_SEASON', 'autumn')
            
            print(f"✅ Текущий сезон: {current_season}")
            
            if current_season in seasons:
                ingredients = seasons[current_season]
                print(f"✅ Ингредиенты текущего сезона: {len(ingredients)}")
                print(f"   Примеры: {', '.join(ingredients[:5])}")
                return True
            else:
                print(f"⚠️  Сезон {current_season} не найден в SEASONAL_INGREDIENTS")
                return False
        else:
            print("❌ SEASONAL_INGREDIENTS не найдено")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

async def test_database():
    """Тест базы данных"""
    print("\n" + "="*50)
    print("🧪 ТЕСТ: База данных")
    print("="*50)
    
    try:
        from database import CocktailDatabase
        
        db = CocktailDatabase()
        print("✅ База данных инициализирована")
        
        # Тестируем поиск
        test_queries = ['джин', 'мохито', 'виски']
        for query in test_queries:
            try:
                results = db.search_recipes(query)
                count = len(results) if results else 0
                print(f"  ✅ Поиск '{query}': найдено {count} рецептов")
            except Exception as e:
                print(f"  ⚠️  Поиск '{query}': ошибка ({str(e)[:50]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка БД: {e}")
        return False

async def main():
    """Главная функция тестирования"""
    print("="*50)
    print("🧪 ТЕСТИРОВАНИЕ ФУНКЦИЙ БОТА")
    print("="*50)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'База вкусовых сочетаний': await test_flavor_pairs(),
        'Сезонные ингредиенты': await test_seasonal_ingredients(),
        'База данных': await test_database(),
        'Новости из российских источников': await test_news_function(),
    }
    
    print("\n" + "="*50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("="*50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n✅ Пройдено: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("🚀 Бот готов к работе!")
    else:
        print(f"\n⚠️  {total - passed} тест(ов) не пройдено")
    
    print("="*50)

if __name__ == '__main__':
    asyncio.run(main())

