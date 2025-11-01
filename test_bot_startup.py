#!/usr/bin/env python3
"""
Тестовый скрипт для проверки запуска бота
Проверяет все компоненты перед полным запуском
"""

import sys
import os

def test_imports():
    """Проверка импортов"""
    print("🔍 Проверка импортов...")
    try:
        import asyncio
        print("  ✅ asyncio")
        
        from dotenv import load_dotenv
        print("  ✅ dotenv")
        
        import requests
        print("  ✅ requests")
        
        from aiogram import Bot, Dispatcher
        print("  ✅ aiogram")
        
        from database import CocktailDatabase
        print("  ✅ database")
        
        from hybrid_processor import HybridCocktailProcessor
        print("  ✅ hybrid_processor")
        
        from cocktail_party_processor import CocktailPartyProcessor
        print("  ✅ cocktail_party_processor")
        
        from enhanced_foodpairing_processor import EnhancedFoodPairingProcessor
        print("  ✅ enhanced_foodpairing_processor")
        
        return True
    except ImportError as e:
        print(f"  ❌ Ошибка импорта: {e}")
        return False

def test_env_variables():
    """Проверка переменных окружения"""
    print("\n🔍 Проверка переменных окружения...")
    
    from dotenv import load_dotenv
    load_dotenv('env_file.txt')
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'YANDEX_API_KEY', 'FOLDER_ID']
    all_ok = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Показываем только первые и последние символы для безопасности
            masked = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
            print(f"  ✅ {var}: {masked}")
        else:
            print(f"  ❌ {var}: НЕ НАЙДЕН")
            all_ok = False
    
    return all_ok

def test_database():
    """Проверка базы данных"""
    print("\n🔍 Проверка базы данных...")
    
    try:
        from database import CocktailDatabase
        db = CocktailDatabase()
        print("  ✅ База данных инициализирована")
        
        # Проверяем количество рецептов
        try:
            recipes = db.search_recipes("test")
            print(f"  ✅ Поиск работает (найдено рецептов: {len(recipes) if recipes else 0})")
        except:
            print("  ⚠️  Поиск не работает, но это не критично")
        
        return True
    except Exception as e:
        print(f"  ❌ Ошибка БД: {e}")
        return False

def test_processors():
    """Проверка процессоров"""
    print("\n🔍 Проверка процессоров...")
    
    try:
        from hybrid_processor import HybridCocktailProcessor
        hybrid = HybridCocktailProcessor()
        print("  ✅ HybridCocktailProcessor")
        
        from cocktail_party_processor import CocktailPartyProcessor
        party = CocktailPartyProcessor()
        print("  ✅ CocktailPartyProcessor")
        
        from enhanced_foodpairing_processor import EnhancedFoodPairingProcessor
        enhanced = EnhancedFoodPairingProcessor()
        print("  ✅ EnhancedFoodPairingProcessor")
        
        return True
    except Exception as e:
        print(f"  ❌ Ошибка процессоров: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_bot_import():
    """Проверка импорта основного файла бота"""
    print("\n🔍 Проверка импорта bot.py...")
    
    try:
        # Пытаемся импортировать основные функции
        import bot
        print("  ✅ bot.py импортирован успешно")
        
        # Проверяем наличие основных переменных
        if hasattr(bot, 'RUSSIAN_HORECA_SOURCES'):
            print(f"  ✅ Российские источники новостей: {len(bot.RUSSIAN_HORECA_SOURCES)}")
        
        if hasattr(bot, 'FLAVOR_PAIRS'):
            print(f"  ✅ Вкусовые сочетания: {len(bot.FLAVOR_PAIRS)}")
        
        if hasattr(bot, 'SEASONAL_INGREDIENTS'):
            print(f"  ✅ Сезонные ингредиенты загружены")
        
        return True
    except Exception as e:
        print(f"  ❌ Ошибка импорта bot.py: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Главная функция тестирования"""
    print("=" * 50)
    print("🧪 ТЕСТИРОВАНИЕ ЗАПУСКА БОТА")
    print("=" * 50)
    
    results = {
        'imports': test_imports(),
        'env': test_env_variables(),
        'database': test_database(),
        'processors': test_processors(),
        'bot_import': test_bot_import()
    }
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("🚀 Бот готов к запуску!")
        print("\nДля запуска используйте: python bot.py")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        print("⚠️  Исправьте ошибки перед запуском")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

