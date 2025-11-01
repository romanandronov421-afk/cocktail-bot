#!/usr/bin/env python3
"""
Скрипт для добавления новых рецептов в базу данных MIXTRIX🍸
"""

import sqlite3
import os

def add_new_recipes():
    """Добавление новых рецептов в базу данных"""
    
    # Подключаемся к базе данных
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    print("🍸 Добавление новых рецептов в MIXTRIX...")
    
    # Новые рецепты для добавления
    new_recipes = [
        # Современные рецепты
        ("Espresso Martini", "60 мл водка, 30 мл эспрессо, 20 мл кофейный ликер, 10 мл сахарный сироп", 
         "Шейк со льдом, подача в коктейльном бокале", "водка", "современный", "MIXTRIX", 
         "Кофейный коктейль с кофеином", "коктейльный", "кофейные зерна", "средний", "4 мин"),
        
        ("Aperol Spritz", "60 мл Aperol, 90 мл Просекко, 30 мл содовая", 
         "Билд в бокале со льдом", "аперитив", "классический", "MIXTRIX", 
         "Итальянский аперитив", "винный", "апельсиновая долька", "легкий", "2 мин"),
        
        ("French 75", "30 мл джин, 15 мл лимонный сок, 10 мл сахарный сироп, 60 мл шампанское", 
         "Шейк джин с соком и сиропом, добавить шампанское", "джин", "классический", "MIXTRIX", 
         "Элегантный коктейль с шампанским", "флейта", "лимонная цедра", "средний", "3 мин"),
        
        # Сезонные рецепты
        ("Apple Cider Mule", "60 мл водка, 120 мл яблочный сидр, 30 мл лаймовый сок, имбирь", 
         "Билд в медной кружке со льдом", "водка", "сезонный", "MIXTRIX", 
         "Осенний вариант Moscow Mule", "медная кружка", "яблочная долька", "легкий", "3 мин"),
        
        ("Cranberry Cosmopolitan", "60 мл водка, 30 мл трипл сек, 30 мл клюквенный сок, 15 мл лаймовый сок", 
         "Шейк со льдом, подача в коктейльном бокале", "водка", "сезонный", "MIXTRIX", 
         "Праздничный коктейль с клюквой", "коктейльный", "клюква", "средний", "3 мин"),
        
        # Безалкогольные рецепты
        ("Virgin Mojito", "30 мл лаймовый сок, 20 мл сахарный сироп, 8 листьев мяты, содовая", 
         "Мудл мяты, добавить ингредиенты, подача в хайбол", "безалкогольный", "mocktail", "MIXTRIX", 
         "Освежающий безалкогольный мохито", "хайбол", "мята и лайм", "легкий", "3 мин"),
        
        ("Shirley Temple", "30 мл гренадин, 120 мл имбирный эль, 30 мл лимонный сок", 
         "Билд в хайболе со льдом", "безалкогольный", "mocktail", "MIXTRIX", 
         "Классический детский коктейль", "хайбол", "вишня мараскино", "легкий", "2 мин"),
        
        # Примиксы
        ("Cinnamon Simple Syrup", "1 часть корица палочки, 1 часть сахара, 1 часть воды", 
         "Нагреть воду с корицей, растворить сахар, процедить", "сироп", "примикс", "MIXTRIX", 
         "Коричный сахарный сироп", "бутылка", "нет", "легкий", "15 мин"),
        
        ("Cardamom Syrup", "1 часть кардамон, 1 часть сахара, 1 часть воды", 
         "Нагреть воду с кардамоном, растворить сахар, процедить", "сироп", "примикс", "MIXTRIX", 
         "Кардамоновый сироп", "бутылка", "нет", "средний", "20 мин"),
        
        ("Smoky Syrup", "1 часть сахара, 1 часть воды, жидкий дым", 
         "Нагреть воду, растворить сахар, добавить жидкий дым", "сироп", "примикс", "MIXTRIX", 
         "Дымный сироп для коктейлей", "бутылка", "нет", "средний", "15 мин")
    ]
    
    try:
        # Добавляем рецепты в базу данных
        cursor.executemany("""
            INSERT OR IGNORE INTO recipes 
            (name, ingredients, method, base_spirit, category, source, 
             description, glassware, garnish, difficulty, prep_time) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, new_recipes)
        
        conn.commit()
        print(f"✅ Успешно добавлено {len(new_recipes)} новых рецептов!")
        
        # Показываем статистику
        cursor.execute("SELECT category, COUNT(*) FROM recipes GROUP BY category")
        stats = cursor.fetchall()
        
        print("\n📊 Статистика базы данных:")
        for category, count in stats:
            print(f"  {category}: {count} рецептов")
        
        # Показываем общее количество
        cursor.execute("SELECT COUNT(*) FROM recipes")
        total = cursor.fetchone()[0]
        print(f"\n📚 Всего рецептов в базе: {total}")
        
    except Exception as e:
        print(f"❌ Ошибка при добавлении рецептов: {e}")
    
    finally:
        conn.close()

def show_recipe_categories():
    """Показать все категории рецептов"""
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT category FROM recipes ORDER BY category")
    categories = cursor.fetchall()
    
    print("\n📋 Доступные категории:")
    for category in categories:
        print(f"  • {category[0]}")
    
    conn.close()

def search_recipes_by_category(category):
    """Поиск рецептов по категории"""
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, description FROM recipes WHERE category = ?", (category,))
    recipes = cursor.fetchall()
    
    print(f"\n🔍 Рецепты в категории '{category}':")
    for recipe in recipes:
        print(f"  • {recipe[0]}: {recipe[1]}")
    
    conn.close()

def main():
    """Основная функция"""
    print("🍸 MIXTRIX - Добавление новых рецептов")
    print("=" * 50)
    
    # Проверяем существование базы данных
    if not os.path.exists('cocktails.db'):
        print("❌ База данных не найдена. Запустите main.py для создания базы.")
        return
    
    # Добавляем новые рецепты
    add_new_recipes()
    
    # Показываем категории
    show_recipe_categories()
    
    # Пример поиска
    search_recipes_by_category('современный')
    
    print("\n🎉 Готово! Новые рецепты добавлены в MIXTRIX🍸")
    print("Перезапустите бота для применения изменений.")

if __name__ == "__main__":
    main()














