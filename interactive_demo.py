#!/usr/bin/env python3
"""
Интерактивная демонстрация работы MIXTRIX🍸
"""

import sqlite3
import random

def interactive_demo():
    """Интерактивная демонстрация возможностей бота"""
    
    print("🍸 MIXTRIX - Интерактивная демонстрация")
    print("=" * 50)
    
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    # Демонстрация поиска
    print("\n🔍 Демонстрация поиска:")
    search_queries = [
        "фейхоа",
        "молекулярный",
        "фудпейринг",
        "текила",
        "джин",
        "ром",
        "морошка",
        "дыня"
    ]
    
    for query in search_queries:
        cursor.execute("SELECT name, source FROM recipes WHERE ingredients LIKE ? OR name LIKE ? OR description LIKE ? LIMIT 3", 
                      (f"%{query}%", f"%{query}%", f"%{query}%"))
        results = cursor.fetchall()
        if results:
            print(f"\n  Поиск '{query}':")
            for name, source in results:
                print(f"    • {name} ({source})")
    
    # Демонстрация команд
    print("\n📋 Демонстрация команд:")
    
    commands_demo = [
        ("/el_copitas", "Авторские рецепты El Copitas Bar"),
        ("/molecular", "Молекулярные техники"),
        ("/flavor_principles", "Принципы фудпейринга"),
        ("/iba", "Официальные рецепты IBA"),
        ("/liquid_intelligence", "Научные коктейли")
    ]
    
    for command, description in commands_demo:
        print(f"  {command}: {description}")
        
        # Получаем примеры для каждой команды
        if command == "/el_copitas":
            cursor.execute("SELECT name, description FROM recipes WHERE source = 'El Copitas Bar' LIMIT 2")
        elif command == "/molecular":
            cursor.execute("SELECT name, description FROM recipes WHERE category = 'liquid_intelligence_technique' LIMIT 2")
        elif command == "/flavor_principles":
            cursor.execute("SELECT name, description FROM recipes WHERE category = 'flavor_bible_principle' LIMIT 2")
        elif command == "/iba":
            cursor.execute("SELECT name, description FROM recipes WHERE source = 'IBA Official' LIMIT 2")
        elif command == "/liquid_intelligence":
            cursor.execute("SELECT name, description FROM recipes WHERE source = 'Liquid Intelligence' AND category LIKE '%cocktail%' LIMIT 2")
        
        examples = cursor.fetchall()
        for name, desc in examples:
            print(f"    • {name}: {desc[:60]}...")
    
    # Демонстрация генерации рецептов
    print("\n🤖 Демонстрация генерации рецептов:")
    
    generation_examples = [
        "создай коктейль с фейхоа",
        "молекулярный коктейль с дыней",
        "классический мартини",
        "летний коктейль с ягодами",
        "мексиканский коктейль с текилой"
    ]
    
    for example in generation_examples:
        print(f"\n  Пользователь: {example}")
        
        # Имитируем ответ бота
        if "фейхоа" in example:
            cursor.execute("SELECT name, ingredients, method, description FROM recipes WHERE ingredients LIKE '%фейхоа%' LIMIT 1")
            recipe = cursor.fetchone()
            if recipe:
                print(f"  Бот: 🍸 Вот авторский рецепт с фейхоа из El Copitas Bar:")
                print(f"       **{recipe[0]}**")
                print(f"       {recipe[1]}")
                print(f"       Метод: {recipe[2]}")
                print(f"       {recipe[3]}")
        
        elif "молекулярный" in example:
            print("  Бот: 🧪 Для молекулярного коктейля с дыней рекомендую:")
            print("       • Clarified Melon Juice (очищенный дынный сок)")
            print("       • Spherification technique (сферификация)")
            print("       • Temperature control (контроль температуры)")
            print("       • pH balance (баланс pH)")
        
        elif "классический мартини" in example:
            cursor.execute("SELECT name, ingredients, method FROM recipes WHERE name LIKE '%Martini%' AND source = 'IBA Official' LIMIT 1")
            recipe = cursor.fetchone()
            if recipe:
                print(f"  Бот: 🍸 Классический рецепт из IBA:")
                print(f"       **{recipe[0]}**")
                print(f"       {recipe[1]}")
                print(f"       Метод: {recipe[2]}")
        
        elif "летний" in example:
            print("  Бот: ☀️ Летние коктейли с ягодами:")
            print("       • Cloudberry Margo (маргарита с морошкой)")
            print("       • Blueberry Margo (маргарита с черникой)")
            print("       • Strawberry Paloma (палома с клубникой)")
            print("       • Melon Margo (маргарита с дыней)")
        
        elif "мексиканский" in example:
            cursor.execute("SELECT name, ingredients FROM recipes WHERE source = 'El Copitas Bar' AND ingredients LIKE '%текила%' LIMIT 2")
            recipes = cursor.fetchall()
            print("  Бот: 🇲🇽 Мексиканские коктейли с текилой:")
            for name, ingredients in recipes:
                print(f"       • {name}: {ingredients[:50]}...")
    
    # Демонстрация фудпейринга
    print("\n🍽️ Демонстрация фудпейринга:")
    
    pairing_examples = [
        ("текила", "Текила отлично сочетается с:"),
        ("джин", "Джин гармонирует с:"),
        ("ром", "Ром прекрасно дополняет:")
    ]
    
    for spirit, intro in pairing_examples:
        print(f"\n  Пользователь: что сочетается с {spirit}?")
        print(f"  Бот: {intro}")
        
        # Получаем примеры сочетаний
        cursor.execute("SELECT name, ingredients FROM recipes WHERE ingredients LIKE ? AND source = 'The Flavor Bible' LIMIT 2", 
                      (f"%{spirit}%",))
        pairings = cursor.fetchall()
        
        if pairings:
            for name, ingredients in pairings:
                print(f"       • {name}: {ingredients[:60]}...")
        else:
            # Альтернативные сочетания
            if spirit == "текила":
                print("       • Лаймом и солью (классика)")
                print("       • Агавой и мескалем")
                print("       • Острыми перцами и специями")
            elif spirit == "джин":
                print("       • Тоником и лаймом")
                print("       • Вермутом и оливками")
                print("       • Травяными нотами")
            elif spirit == "ром":
                print("       • Лаймом и сахаром")
                print("       • Тропическими фруктами")
                print("       • Пряностями и специями")
    
    conn.close()
    
    print("\n🎯 Итоговая статистика:")
    print("=" * 30)
    print("📊 Всего рецептов: 519")
    print("📚 Источников знаний: 8")
    print("🎯 Команд: 20")
    print("🤖 AI интеграция: YandexGPT")
    print("🛡️ Безопасность: проверка возраста, фильтрация")
    print("🍽️ Фудпейринг: принципы сочетания вкусов")
    print("🧪 Молекулярная миксология: научные техники")
    print("🍸 Авторские рецепты: креативные техники")
    
    print("\n🎉 MIXTRIX🍸 полностью готов к работе!")
    print("Бот может:")
    print("• Генерировать рецепты с помощью AI")
    print("• Искать по ингредиентам и техникам")
    print("• Предлагать сочетания вкусов")
    print("• Объяснять молекулярные техники")
    print("• Показывать авторские рецепты")
    print("• Давать сезонные советы")
    print("• Обучать принципам барменства")

if __name__ == "__main__":
    interactive_demo()














