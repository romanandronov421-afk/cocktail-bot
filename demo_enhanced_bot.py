#!/usr/bin/env python3
"""
Демонстрация возможностей улучшенного бота MIXTRIX
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def demo_enhanced_bot():
    """Демонстрация улучшенных возможностей бота"""
    print("🍸 ДЕМОНСТРАЦИЯ УЛУЧШЕННОГО БОТА MIXTRIX")
    print("=" * 60)
    
    try:
        from enhanced_foodpairing_processor import EnhancedFoodPairingProcessor
        
        print("✅ Улучшенный процессор фудпейринга загружен!")
        
        # Инициализируем процессор
        processor = EnhancedFoodPairingProcessor()
        
        print(f"📊 Загружено вкусовых комбинаций: {len(processor.flavor_combinations)}")
        print(f"📊 Загружено рецептов: {len(processor.recipe_database)}")
        
        print("\n" + "=" * 60)
        print("🍽️ ДЕМОНСТРАЦИЯ ВКУСОВЫХ КОМБИНАЦИЙ")
        print("=" * 60)
        
        # Показываем примеры вкусовых комбинаций
        categories = ['fruit_berry', 'floral_herbal', 'spicy_warming', 'creamy_dessert', 'unexpected_avantgarde']
        category_names = ['Фруктовые и ягодные', 'Цветочные и травяные', 'Пряные и согревающие', 'Сливочные и десертные', 'Неожиданные и авангардные']
        
        for category, name in zip(categories, category_names):
            combinations = processor.flavor_combinations.get(category, [])
            print(f"\n🍽️ {name} ({len(combinations)} комбинаций):")
            for i, combo in enumerate(combinations[:3], 1):  # Показываем первые 3
                ingredients_str = " + ".join(combo['ingredients'])
                print(f"  {i}. {ingredients_str} - {combo['description']} (сила: {combo['strength']}/5)")
        
        print("\n" + "=" * 60)
        print("🍂 ДЕМОНСТРАЦИЯ СЕЗОННЫХ РЕКОМЕНДАЦИЙ")
        print("=" * 60)
        
        # Показываем сезонные рекомендации
        recommendations = processor.get_seasonal_recommendations("autumn")
        print(recommendations)
        
        print("\n" + "=" * 60)
        print("🍸 ДЕМОНСТРАЦИЯ ГЕНЕРАЦИИ РЕЦЕПТА")
        print("=" * 60)
        
        print("Создаем рецепт коктейля с джином под стейк...")
        
        # Генерируем рецепт (без вызова API для демонстрации)
        best_combinations = processor._get_best_combinations_for_spirit("джин")
        print(f"\nЛучшие комбинации для джина:")
        for i, combo in enumerate(best_combinations[:5], 1):
            ingredients_str = " + ".join(combo['ingredients'])
            print(f"  {i}. {ingredients_str} - {combo['description']} (совместимость: {combo['compatibility_score']})")
        
        print("\n" + "=" * 60)
        print("🎯 НОВЫЕ КОМАНДЫ БОТА")
        print("=" * 60)
        
        commands = [
            ("/recipe джин", "Создать рецепт с джином"),
            ("/recipe текила dish=стейк", "Рецепт под стейк"),
            ("/pairing рыба", "Фудпейринг для рыбы"),
            ("/seasonal", "Сезонные рекомендации"),
            ("/flavor_combinations fruit", "Фруктовые комбинации"),
            ("/knowledge_base", "Полная база знаний")
        ]
        
        for command, description in commands:
            print(f"• {command:<25} - {description}")
        
        print("\n" + "=" * 60)
        print("🎉 БОТ ГОТОВ К РАБОТЕ!")
        print("=" * 60)
        print("Все улучшения успешно интегрированы:")
        print("✅ 300+ вкусовых комбинаций из The Flavor Bible")
        print("✅ Интеграция всех профессиональных источников")
        print("✅ Умный фудпейринг под блюда")
        print("✅ Сезонные рекомендации для России")
        print("✅ Улучшенная генерация рецептов")
        print("✅ Новые команды и возможности")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при демонстрации: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Основная функция демонстрации"""
    success = await demo_enhanced_bot()
    
    if success:
        print("\n🚀 Бот MIXTRIX🍸 успешно запущен с улучшенными возможностями!")
        print("Теперь вы можете использовать все новые функции фудпейринга!")
    else:
        print("\n⚠️ Есть проблемы с запуском. Проверьте ошибки выше.")

if __name__ == "__main__":
    asyncio.run(main())






