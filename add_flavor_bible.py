#!/usr/bin/env python3
"""
Скрипт для добавления знаний из "The Flavor Bible" Карен Пейдж и Эндрю Дорненбурга в MIXTRIX🍸
"""

import sqlite3
import os

def add_flavor_bible_knowledge():
    """Добавление знаний из "The Flavor Bible" """
    
    # Подключаемся к базе данных
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    print("🍽️ Добавление знаний из 'The Flavor Bible' в MIXTRIX...")
    
    # Принципы фудпейринга из The Flavor Bible
    flavor_principles = [
        # Основные принципы сочетания вкусов
        ("Sweet & Sour Balance", "Баланс сладкого и кислого", "Основной принцип гармонии вкусов", "принцип", "flavor_bible_principle", "The Flavor Bible", "Классический баланс сладкого и кислого", "палитра", "нет", "легкий", "понимание"),
        ("Fat & Acid Balance", "Баланс жирного и кислого", "Жирность смягчает кислотность", "принцип", "flavor_bible_principle", "The Flavor Bible", "Жирные компоненты уравновешивают кислоту", "палитра", "нет", "легкий", "понимание"),
        ("Salt Enhancement", "Усиление вкуса солью", "Соль усиливает все вкусы", "принцип", "flavor_bible_principle", "The Flavor Bible", "Соль как усилитель вкуса", "палитра", "нет", "легкий", "понимание"),
        ("Umami Depth", "Глубина умами", "Пятый вкус добавляет глубину", "принцип", "flavor_bible_principle", "The Flavor Bible", "Умами как основа вкусовой глубины", "палитра", "нет", "средний", "понимание"),
        ("Texture Contrast", "Контраст текстур", "Разные текстуры создают интерес", "принцип", "flavor_bible_principle", "The Flavor Bible", "Контрастные текстуры в одном блюде", "палитра", "нет", "средний", "понимание"),
        ("Temperature Contrast", "Контраст температур", "Горячее и холодное вместе", "принцип", "flavor_bible_principle", "The Flavor Bible", "Температурный контраст усиливает восприятие", "палитра", "нет", "средний", "понимание"),
        ("Aromatic Complexity", "Ароматическая сложность", "Сложные ароматы привлекают внимание", "принцип", "flavor_bible_principle", "The Flavor Bible", "Многослойные ароматы создают глубину", "палитра", "нет", "сложный", "понимание"),
        ("Seasonal Harmony", "Сезонная гармония", "Ингредиенты одного сезона сочетаются", "принцип", "flavor_bible_principle", "The Flavor Bible", "Сезонные ингредиенты естественно сочетаются", "палитра", "нет", "легкий", "понимание"),
        ("Cultural Authenticity", "Культурная аутентичность", "Традиционные сочетания проверены временем", "принцип", "flavor_bible_principle", "The Flavor Bible", "Культурные традиции как основа сочетаний", "палитра", "нет", "средний", "понимание"),
        ("Personal Preference", "Личные предпочтения", "Вкусы субъективны", "принцип", "flavor_bible_principle", "The Flavor Bible", "Учет личных вкусовых предпочтений", "палитра", "нет", "легкий", "понимание"),
    ]
    
    # Классические сочетания вкусов из The Flavor Bible
    flavor_combinations = [
        # Классические сочетания
        ("Tomato + Basil", "Помидор + Базилик", "Классическое итальянское сочетание", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Свежесть базилика с кислотностью томата", "тарелка", "нет", "легкий", "мгновенно"),
        ("Lemon + Thyme", "Лимон + Тимьян", "Цитрусовая свежесть с травяными нотами", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Кислота лимона с ароматом тимьяна", "тарелка", "нет", "легкий", "мгновенно"),
        ("Chocolate + Orange", "Шоколад + Апельсин", "Горький шоколад с цитрусовой свежестью", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Горькость шоколада с кислотностью апельсина", "тарелка", "нет", "легкий", "мгновенно"),
        ("Strawberry + Balsamic", "Клубника + Бальзамик", "Сладкая ягода с кислым уксусом", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Сладость клубники с кислотностью бальзамика", "тарелка", "нет", "средний", "мгновенно"),
        ("Parmesan + Honey", "Пармезан + Мед", "Соленый сыр с сладким медом", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Умами пармезана с сладостью меда", "тарелка", "нет", "средний", "мгновенно"),
        ("Coconut + Lime", "Кокос + Лайм", "Тропическая сладость с цитрусовой кислотой", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Жирность кокоса с кислотностью лайма", "тарелка", "нет", "легкий", "мгновенно"),
        ("Ginger + Sesame", "Имбирь + Кунжут", "Острота имбиря с ореховыми нотами", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Пряность имбиря с умами кунжута", "тарелка", "нет", "средний", "мгновенно"),
        ("Mint + Cucumber", "Мята + Огурец", "Освежающая свежесть", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Ментоловая свежесть с водянистой чистотой", "тарелка", "нет", "легкий", "мгновенно"),
        ("Vanilla + Salt", "Ваниль + Соль", "Сладкая ваниль с соленой глубиной", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Сладость ванили с соленой глубиной", "тарелка", "нет", "легкий", "мгновенно"),
        ("Cinnamon + Apple", "Корица + Яблоко", "Теплая пряность с фруктовой сладостью", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Пряность корицы с кислотностью яблока", "тарелка", "нет", "легкий", "мгновенно"),
        
        # Сложные сочетания
        ("Smoked Salmon + Dill + Cream", "Копченый лосось + Укроп + Сливки", "Дымность с травяной свежестью и жирностью", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Умами лосося с ароматом укропа и жирностью сливок", "тарелка", "нет", "сложный", "мгновенно"),
        ("Dark Chocolate + Sea Salt + Olive Oil", "Темный шоколад + Морская соль + Оливковое масло", "Горькость с соленостью и жирностью", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Горькость шоколада с соленостью и жирностью масла", "тарелка", "нет", "сложный", "мгновенно"),
        ("Roasted Beet + Goat Cheese + Walnuts", "Запеченная свекла + Козий сыр + Грецкие орехи", "Землистость с кислинкой и ореховыми нотами", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Сладость свеклы с кислотностью сыра и ореховыми нотами", "тарелка", "нет", "сложный", "мгновенно"),
        ("Pomegranate + Pistachio + Rose", "Гранат + Фисташки + Роза", "Кислотность с ореховыми и цветочными нотами", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Кислотность граната с ореховыми и розовыми нотами", "тарелка", "нет", "сложный", "мгновенно"),
        ("Miso + Maple Syrup + Butter", "Мисо + Кленовый сироп + Масло", "Умами с сладостью и жирностью", "сочетание", "flavor_bible_combination", "The Flavor Bible", "Умами мисо с сладостью сиропа и жирностью масла", "тарелка", "нет", "сложный", "мгновенно"),
    ]
    
    # Сезонные сочетания из The Flavor Bible
    seasonal_pairings = [
        # Весенние сочетания
        ("Spring Asparagus + Lemon + Butter", "Весенняя спаржа + Лимон + Масло", "Свежесть весны с цитрусовой кислотой", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Зеленая свежесть спаржи с кислотностью лимона", "тарелка", "нет", "легкий", "мгновенно"),
        ("Pea Shoots + Mint + Ricotta", "Гороховые побеги + Мята + Рикотта", "Зеленая свежесть с ментоловыми нотами", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Свежесть побегов с ментолом и нежностью сыра", "тарелка", "нет", "средний", "мгновенно"),
        ("Rhubarb + Strawberry + Vanilla", "Ревень + Клубника + Ваниль", "Кислотность ревеня с сладостью клубники", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Кислотность ревеня с сладостью клубники и ванилью", "тарелка", "нет", "средний", "мгновенно"),
        
        # Летние сочетания
        ("Summer Tomato + Basil + Mozzarella", "Летний помидор + Базилик + Моцарелла", "Классическое летнее сочетание", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Сочность томата с ароматом базилика и нежностью сыра", "тарелка", "нет", "легкий", "мгновенно"),
        ("Corn + Lime + Chili", "Кукуруза + Лайм + Чили", "Сладость кукурузы с кислотностью и остротой", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Сладость кукурузы с кислотностью лайма и остротой чили", "тарелка", "нет", "средний", "мгновенно"),
        ("Peach + Prosciutto + Arugula", "Персик + Прошутто + Руккола", "Сладость персика с соленостью и горечью", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Сладость персика с умами прошутто и горечью рукколы", "тарелка", "нет", "сложный", "мгновенно"),
        
        # Осенние сочетания
        ("Pumpkin + Sage + Brown Butter", "Тыква + Шалфей + Коричневое масло", "Сладость тыквы с травяными нотами", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Сладость тыквы с ароматом шалфея и ореховыми нотами масла", "тарелка", "нет", "средний", "мгновенно"),
        ("Apple + Cinnamon + Caramel", "Яблоко + Корица + Карамель", "Классическое осеннее сочетание", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Кислотность яблока с пряностью корицы и сладостью карамели", "тарелка", "нет", "легкий", "мгновенно"),
        ("Mushroom + Thyme + Cream", "Грибы + Тимьян + Сливки", "Землистость грибов с травяными нотами", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Умами грибов с ароматом тимьяна и жирностью сливок", "тарелка", "нет", "средний", "мгновенно"),
        
        # Зимние сочетания
        ("Citrus + Fennel + Olive Oil", "Цитрусы + Фенхель + Оливковое масло", "Яркость цитрусов с анисовыми нотами", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Кислотность цитрусов с анисовыми нотами фенхеля", "тарелка", "нет", "средний", "мгновенно"),
        ("Pomegranate + Dark Chocolate + Sea Salt", "Гранат + Темный шоколад + Морская соль", "Кислотность с горькостью и соленостью", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Кислотность граната с горькостью шоколада и соленостью", "тарелка", "нет", "сложный", "мгновенно"),
        ("Chestnut + Vanilla + Brandy", "Каштан + Ваниль + Бренди", "Ореховые ноты с сладостью и алкоголем", "сезонное", "flavor_bible_seasonal", "The Flavor Bible", "Ореховые ноты каштана с сладостью ванили и алкоголем", "тарелка", "нет", "сложный", "мгновенно"),
    ]
    
    # Фудпейринг для коктейлей из The Flavor Bible
    cocktail_pairings = [
        # Классические фудпейринги для коктейлей
        ("Martini + Olives", "Мартини + Оливки", "Сухой джин с солеными оливками", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Сухость джина с умами оливок", "коктейль", "оливка", "легкий", "мгновенно"),
        ("Manhattan + Steak", "Манхэттен + Стейк", "Виски с мясными нотами", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Дымность виски с умами стейка", "коктейль", "вишня", "средний", "мгновенно"),
        ("Margarita + Tacos", "Маргарита + Тако", "Текила с мексиканской едой", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Кислотность текилы с пряностью тако", "коктейль", "лайм", "легкий", "мгновенно"),
        ("Negroni + Charcuterie", "Негрони + Шаркутери", "Горький коктейль с мясными закусками", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Горькость негрони с умами мясных закусок", "коктейль", "апельсин", "средний", "мгновенно"),
        ("Old Fashioned + Dark Chocolate", "Олд фешен + Темный шоколад", "Виски с горьким шоколадом", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Дымность виски с горькостью шоколада", "коктейль", "апельсин", "средний", "мгновенно"),
        ("Daiquiri + Ceviche", "Дайкири + Севиче", "Ром с цитрусовой рыбой", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Сладость рома с кислотностью севиче", "коктейль", "лайм", "средний", "мгновенно"),
        ("Gin Fizz + Smoked Salmon", "Джин физз + Копченый лосось", "Джин с дымным лососем", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Свежесть джина с умами лосося", "коктейль", "лимон", "средний", "мгновенно"),
        ("Bloody Mary + Brunch", "Кровавая Мэри + Бранч", "Томатный коктейль с утренней едой", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Кислотность томата с утренними блюдами", "коктейль", "сельдерей", "легкий", "мгновенно"),
        ("Mojito + Grilled Shrimp", "Мохито + Жареные креветки", "Мятный ром с морепродуктами", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Ментоловая свежесть с умами креветок", "коктейль", "мята", "средний", "мгновенно"),
        ("Cosmopolitan + Sushi", "Космополитен + Суши", "Водка с японской едой", "фудпейринг", "flavor_bible_cocktail", "The Flavor Bible", "Чистота водки с умами суши", "коктейль", "лайм", "средний", "мгновенно"),
    ]
    
    # Объединяем все рецепты
    all_recipes = flavor_principles + flavor_combinations + seasonal_pairings + cocktail_pairings
    
    try:
        # Добавляем рецепты в базу данных
        cursor.executemany("""
            INSERT OR IGNORE INTO recipes 
            (name, ingredients, method, base_spirit, category, source, 
             description, glassware, garnish, difficulty, prep_time) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, all_recipes)
        
        conn.commit()
        print(f"✅ Успешно добавлено {len(all_recipes)} рецептов из 'The Flavor Bible'!")
        
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
        
        # Показываем количество рецептов из The Flavor Bible
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE source = 'The Flavor Bible'")
        flavor_count = cursor.fetchone()[0]
        print(f"🍽️ Рецептов из 'The Flavor Bible': {flavor_count}")
        
    except Exception as e:
        print(f"❌ Ошибка при добавлении рецептов: {e}")
    
    finally:
        conn.close()

def show_flavor_bible_categories():
    """Показать категории рецептов из The Flavor Bible"""
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT category FROM recipes WHERE source = 'The Flavor Bible' ORDER BY category")
    categories = cursor.fetchall()
    
    print("\n📋 Категории рецептов из 'The Flavor Bible':")
    for category in categories:
        print(f"  • {category[0]}")
    
    conn.close()

def main():
    """Основная функция"""
    print("🍽️ MIXTRIX - Добавление знаний из 'The Flavor Bible'")
    print("=" * 50)
    
    # Проверяем существование базы данных
    if not os.path.exists('cocktails.db'):
        print("❌ База данных не найдена. Запустите main.py для создания базы.")
        return
    
    # Добавляем знания из The Flavor Bible
    add_flavor_bible_knowledge()
    
    # Показываем категории
    show_flavor_bible_categories()
    
    print("\n🎉 Готово! Знания из 'The Flavor Bible' добавлены в MIXTRIX🍸")
    print("Перезапустите бота для применения изменений.")

if __name__ == "__main__":
    main()














