#!/usr/bin/env python3
"""
Демонстрация возможностей MIXTRIX🍸 с расширенной базой знаний
"""

import sqlite3
import os

def demonstrate_bot_capabilities():
    """Демонстрация возможностей бота"""
    
    print("🍸 MIXTRIX - Демонстрация возможностей бота")
    print("=" * 50)
    
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    # Общая статистика
    cursor.execute("SELECT COUNT(*) FROM recipes")
    total = cursor.fetchone()[0]
    print(f"📊 Всего рецептов в базе: {total}")
    
    # Статистика по источникам
    cursor.execute("SELECT source, COUNT(*) FROM recipes GROUP BY source ORDER BY COUNT(*) DESC")
    sources = cursor.fetchall()
    print("\n📚 Источники знаний:")
    for source, count in sources:
        print(f"  • {source}: {count} рецептов")
    
    # Статистика по категориям
    cursor.execute("SELECT category, COUNT(*) FROM recipes GROUP BY category ORDER BY COUNT(*) DESC LIMIT 10")
    categories = cursor.fetchall()
    print("\n🏷️ Топ-10 категорий:")
    for category, count in categories:
        print(f"  • {category}: {count} рецептов")
    
    # Примеры рецептов из разных источников
    print("\n🍸 Примеры рецептов из разных источников:")
    
    # IBA рецепты
    cursor.execute("SELECT name, ingredients, description FROM recipes WHERE source = 'IBA Official' LIMIT 3")
    iba_recipes = cursor.fetchall()
    print("\n📖 IBA Official:")
    for name, ingredients, desc in iba_recipes:
        print(f"  • {name}: {ingredients[:50]}...")
    
    # El Copitas рецепты
    cursor.execute("SELECT name, ingredients, description FROM recipes WHERE source = 'El Copitas Bar' LIMIT 3")
    el_copitas_recipes = cursor.fetchall()
    print("\n🍸 El Copitas Bar:")
    for name, ingredients, desc in el_copitas_recipes:
        print(f"  • {name}: {ingredients[:50]}...")
    
    # Liquid Intelligence рецепты
    cursor.execute("SELECT name, ingredients, description FROM recipes WHERE source = 'Liquid Intelligence' LIMIT 3")
    li_recipes = cursor.fetchall()
    print("\n🧪 Liquid Intelligence:")
    for name, ingredients, desc in li_recipes:
        print(f"  • {name}: {ingredients[:50]}...")
    
    # The Flavor Bible рецепты
    cursor.execute("SELECT name, ingredients, description FROM recipes WHERE source = 'The Flavor Bible' LIMIT 3")
    fb_recipes = cursor.fetchall()
    print("\n🍽️ The Flavor Bible:")
    for name, ingredients, desc in fb_recipes:
        print(f"  • {name}: {ingredients[:50]}...")
    
    # Поиск по ингредиентам
    print("\n🔍 Примеры поиска по ингредиентам:")
    
    search_terms = ["текила", "джин", "ром", "фейхоа", "морошка", "дыня", "шафран"]
    for term in search_terms:
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE ingredients LIKE ?", (f"%{term}%",))
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"  • '{term}': {count} рецептов")
    
    # Сложность рецептов
    cursor.execute("SELECT difficulty, COUNT(*) FROM recipes WHERE difficulty IS NOT NULL GROUP BY difficulty")
    difficulties = cursor.fetchall()
    print("\n⚡ Сложность рецептов:")
    for difficulty, count in difficulties:
        print(f"  • {difficulty}: {count} рецептов")
    
    # Время приготовления
    cursor.execute("SELECT prep_time, COUNT(*) FROM recipes WHERE prep_time IS NOT NULL GROUP BY prep_time ORDER BY COUNT(*) DESC LIMIT 5")
    prep_times = cursor.fetchall()
    print("\n⏱️ Время приготовления:")
    for prep_time, count in prep_times:
        print(f"  • {prep_time}: {count} рецептов")
    
    conn.close()
    
    print("\n🎯 Доступные команды бота:")
    commands = [
        "/start - приветствие и основная информация",
        "/help - справка по командам",
        "/rules - правила использования",
        "/examples - примеры использования",
        "/classic - классические рецепты из 'Код коктейля'",
        "/signature - авторские рецепты",
        "/premix - примиксы и сиропы",
        "/iba - официальные рецепты IBA",
        "/iba_classic - классические рецепты IBA",
        "/bible - рецепты из 'Библия бармена'",
        "/aperitif - рецепты аперитивов",
        "/theory - теория барменства",
        "/preparation - рецепты заготовок",
        "/techniques - техники приготовления",
        "/syrups - рецепты сиропов",
        "/extended - расширенные рецепты",
        "/molecular - молекулярные техники",
        "/scientific - научные заготовки",
        "/liquid_intelligence - научные коктейли",
        "/flavor_principles - принципы фудпейринга",
        "/flavor_combinations - сочетания вкусов",
        "/seasonal_pairings - сезонные сочетания",
        "/cocktail_pairings - фудпейринг для коктейлей",
        "/el_copitas - авторские рецепты El Copitas Bar",
        "/search [запрос] - поиск рецептов",
        "/recipe_detail [название] - подробный рецепт"
    ]
    
    for command in commands:
        print(f"  {command}")
    
    print("\n🤖 Возможности AI:")
    ai_features = [
        "Генерация рецептов с помощью YandexGPT",
        "Поиск по ингредиентам и техникам",
        "Рекомендации по сочетаниям вкусов",
        "Сезонные советы по ингредиентам",
        "Молекулярные техники приготовления",
        "Принципы фудпейринга",
        "Авторские рецепты с креативными техниками",
        "Проверка возраста для алкогольных напитков",
        "Фильтрация политических тем",
        "Образовательный контент о барменстве"
    ]
    
    for feature in ai_features:
        print(f"  • {feature}")
    
    print("\n🎉 MIXTRIX🍸 готов к работе!")
    print("Бот содержит 519 рецептов из 8 профессиональных источников")
    print("Поддерживает 20 команд для работы с различными категориями")
    print("Интегрирован с YandexGPT для генерации рецептов")

def show_sample_interactions():
    """Показать примеры взаимодействия с ботом"""
    
    print("\n💬 Примеры взаимодействия с ботом:")
    print("=" * 40)
    
    examples = [
        {
            "user": "/start",
            "bot": "🍸 Добро пожаловать в MIXTRIX! Я ваш эксперт по коктейлям с базой из 519 рецептов..."
        },
        {
            "user": "/el_copitas",
            "bot": "🍸 Авторские рецепты El Copitas Bar (63 шт.)\n\n• Feijoa Margo - Маргарита с фейхоа и имбирем..."
        },
        {
            "user": "/molecular",
            "bot": "🧪 Молекулярные техники (15 шт.)\n\n• Centrifuge - Разделение жидкостей по плотности..."
        },
        {
            "user": "/flavor_principles",
            "bot": "🍽️ Принципы фудпейринга (10 шт.)\n\n• Sweet & Sour Balance - Баланс сладкого и кислого..."
        },
        {
            "user": "создай коктейль с фейхоа",
            "bot": "🍸 Вот авторский рецепт с фейхоа из El Copitas Bar:\n\n**Feijoa Margo**\n40 мл текила, 25 мл фреш лимон..."
        },
        {
            "user": "какие техники молекулярной миксологии ты знаешь?",
            "bot": "🧪 Я знаю множество молекулярных техник из Liquid Intelligence:\n\n• Centrifuge (Центрифуга)..."
        },
        {
            "user": "что сочетается с текилой?",
            "bot": "🍽️ Текила отлично сочетается с:\n\n• Лаймом и солью (классика)\n• Агавой и мескалем..."
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Пользователь: {example['user']}")
        print(f"   Бот: {example['bot'][:100]}...")

if __name__ == "__main__":
    demonstrate_bot_capabilities()
    show_sample_interactions()














