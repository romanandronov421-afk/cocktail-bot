#!/usr/bin/env python3
"""
Анализ базы знаний рецептов бота MIXTRIX
"""

import sqlite3
import json

def analyze_database():
    """Анализ базы данных рецептов"""
    print("🍹 MIXTRIX Bot - Анализ базы знаний рецептов")
    print("=" * 60)
    
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    # Общая статистика
    cursor.execute('SELECT COUNT(*) FROM recipes')
    total_recipes = cursor.fetchone()[0]
    print(f"📊 Всего рецептов в базе: {total_recipes}")
    print()
    
    # Источники рецептов
    print("📚 Источники рецептов:")
    print("-" * 40)
    cursor.execute('SELECT source, COUNT(*) FROM recipes GROUP BY source ORDER BY COUNT(*) DESC')
    sources = cursor.fetchall()
    
    for source, count in sources:
        percentage = (count / total_recipes) * 100
        print(f"• {source}: {count} рецептов ({percentage:.1f}%)")
    
    print()
    
    # Категории коктейлей
    print("🍸 Категории коктейлей:")
    print("-" * 40)
    cursor.execute('SELECT category, COUNT(*) FROM recipes GROUP BY category ORDER BY COUNT(*) DESC LIMIT 10')
    categories = cursor.fetchall()
    
    for category, count in categories:
        print(f"• {category}: {count} рецептов")
    
    print()
    
    # Базовые спирты
    print("🥃 Базовые спирты:")
    print("-" * 40)
    cursor.execute('SELECT base_spirit, COUNT(*) FROM recipes GROUP BY base_spirit ORDER BY COUNT(*) DESC')
    spirits = cursor.fetchall()
    
    for spirit, count in spirits:
        print(f"• {spirit}: {count} рецептов")
    
    print()
    
    # Сложность приготовления
    print("⚡ Сложность приготовления:")
    print("-" * 40)
    cursor.execute('SELECT difficulty, COUNT(*) FROM recipes GROUP BY difficulty ORDER BY COUNT(*) DESC')
    difficulties = cursor.fetchall()
    
    for difficulty, count in difficulties:
        print(f"• {difficulty}: {count} рецептов")
    
    print()
    
    # Примеры рецептов
    print("🌟 Примеры рецептов:")
    print("-" * 40)
    cursor.execute('SELECT name, base_spirit, source FROM recipes ORDER BY RANDOM() LIMIT 5')
    examples = cursor.fetchall()
    
    for name, spirit, source in examples:
        print(f"• {name} ({spirit}) - {source}")
    
    print()
    
    # Сезонные ингредиенты
    print("🍂 Сезонные ингредиенты:")
    print("-" * 40)
    cursor.execute('SELECT month, COUNT(*) FROM seasonal_ingredients GROUP BY month ORDER BY month')
    seasonal = cursor.fetchall()
    
    for month, count in seasonal:
        print(f"• {month}: {count} ингредиентов")
    
    print()
    
    # Тренды
    print("📈 Тренды коктейлей:")
    print("-" * 40)
    cursor.execute('SELECT trend_name, year FROM trends WHERE is_active = 1 ORDER BY year DESC')
    trends = cursor.fetchall()
    
    for trend_name, year in trends:
        print(f"• {trend_name} ({year})")
    
    print()
    
    # Фудпейринг
    print("🍽️ Фудпейринг:")
    print("-" * 40)
    cursor.execute('SELECT spirit, COUNT(*) FROM food_pairing GROUP BY spirit ORDER BY COUNT(*) DESC')
    pairings = cursor.fetchall()
    
    for spirit, count in pairings:
        print(f"• {spirit}: {count} сочетаний")
    
    conn.close()
    
    print("=" * 60)
    print("✅ Анализ завершен!")

if __name__ == "__main__":
    analyze_database()











