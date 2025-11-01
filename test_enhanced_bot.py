#!/usr/bin/env python3
"""
Тестовый скрипт для проверки улучшенного процессора фудпейринга
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_enhanced_processor():
    """Тест улучшенного процессора фудпейринга"""
    try:
        from enhanced_foodpairing_processor import EnhancedFoodPairingProcessor
        
        print("🍸 Тестирование улучшенного процессора фудпейринга...")
        print("=" * 60)
        
        # Инициализируем процессор
        processor = EnhancedFoodPairingProcessor()
        
        print("✅ Процессор успешно инициализирован!")
        print(f"📊 Загружено вкусовых комбинаций: {len(processor.flavor_combinations)}")
        print(f"📊 Загружено рецептов: {len(processor.recipe_database)}")
        print(f"📊 Загружено правил фудпейринга: {len(processor.food_pairing_rules)}")
        
        print("\n" + "=" * 60)
        print("🧪 Тест 1: Генерация рецепта с фудпейрингом")
        print("=" * 60)
        
        # Тест генерации рецепта с фудпейрингом
        recipe = await processor.generate_recipe_with_foodpairing(
            base_spirit="джин",
            dish="стейк",
            mocktail=False,
            season="autumn"
        )
        
        print("🍸 Сгенерированный рецепт:")
        print("-" * 40)
        print(recipe)
        
        print("\n" + "=" * 60)
        print("🧪 Тест 2: Сезонные рекомендации")
        print("=" * 60)
        
        # Тест сезонных рекомендаций
        recommendations = processor.get_seasonal_recommendations("autumn")
        print("🍂 Сезонные рекомендации:")
        print("-" * 40)
        print(recommendations)
        
        print("\n" + "=" * 60)
        print("🧪 Тест 3: Вкусовые комбинации")
        print("=" * 60)
        
        # Тест получения лучших комбинаций для спирта
        best_combinations = processor._get_best_combinations_for_spirit("джин")
        print("🍽️ Лучшие комбинации для джина:")
        print("-" * 40)
        for i, combo in enumerate(best_combinations[:5], 1):
            ingredients_str = " + ".join(combo['ingredients'])
            print(f"{i}. {ingredients_str} - {combo['description']} (сила: {combo['strength']}/5)")
        
        print("\n" + "=" * 60)
        print("✅ Все тесты завершены успешно!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_bot_integration():
    """Тест интеграции с ботом"""
    try:
        print("\n🤖 Тестирование интеграции с ботом...")
        print("=" * 60)
        
        # Проверяем импорт основных модулей
        from database import CocktailDatabase
        from hybrid_processor import HybridCocktailProcessor
        from cocktail_party_processor import CocktailPartyProcessor
        from enhanced_foodpairing_processor import EnhancedFoodPairingProcessor
        
        print("✅ Все модули успешно импортированы!")
        
        # Проверяем инициализацию базы данных
        db = CocktailDatabase()
        recipes = db.get_all_recipes()
        print(f"✅ База данных: {len(recipes)} рецептов")
        
        # Проверяем гибридный процессор
        hybrid_processor = HybridCocktailProcessor()
        print("✅ Гибридный процессор инициализирован")
        
        # Проверяем процессор коктейльной вечеринки
        party_processor = CocktailPartyProcessor()
        print("✅ Процессор коктейльной вечеринки инициализирован")
        
        # Проверяем улучшенный процессор фудпейринга
        enhanced_processor = EnhancedFoodPairingProcessor()
        print("✅ Улучшенный процессор фудпейринга инициализирован")
        
        print("\n🎉 Интеграция с ботом работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании интеграции: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования улучшенного бота MIXTRIX🍸")
    print("=" * 80)
    
    # Тест 1: Улучшенный процессор фудпейринга
    test1_success = await test_enhanced_processor()
    
    # Тест 2: Интеграция с ботом
    test2_success = await test_bot_integration()
    
    print("\n" + "=" * 80)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 80)
    
    if test1_success:
        print("✅ Тест улучшенного процессора фудпейринга: ПРОЙДЕН")
    else:
        print("❌ Тест улучшенного процессора фудпейринга: ПРОВАЛЕН")
    
    if test2_success:
        print("✅ Тест интеграции с ботом: ПРОЙДЕН")
    else:
        print("❌ Тест интеграции с ботом: ПРОВАЛЕН")
    
    if test1_success and test2_success:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("🍸 Бот готов к работе с улучшенными возможностями фудпейринга!")
    else:
        print("\n⚠️ Некоторые тесты провалены. Проверьте ошибки выше.")
    
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())






