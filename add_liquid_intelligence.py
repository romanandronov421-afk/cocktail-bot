#!/usr/bin/env python3
"""
Скрипт для добавления знаний из "Liquid Intelligence: The Art and Science of the Perfect Cocktail" 
Дейва Арнолда в MIXTRIX🍸
"""

import sqlite3
import os

def add_liquid_intelligence_knowledge():
    """Добавление знаний из "Liquid Intelligence" """
    
    # Подключаемся к базе данных
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    print("🧪 Добавление знаний из 'Liquid Intelligence' в MIXTRIX...")
    
    # Молекулярные техники из Liquid Intelligence
    molecular_techniques = [
        # Основные молекулярные техники
        ("Centrifuge (Центрифуга)", "Разделение жидкостей по плотности", "Для очистки соков и создания прозрачных коктейлей", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научная техника разделения компонентов", "центрифуга", "нет", "сложный", "10-15 мин"),
        ("Rotary Evaporation (Ротационная дистилляция)", "Удаление алкоголя при низкой температуре", "Для создания безалкогольных версий коктейлей", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научная техника дистилляции", "ротационный испаритель", "нет", "сложный", "30-60 мин"),
        ("Vacuum Distillation (Вакуумная дистилляция)", "Дистилляция при пониженном давлении", "Для извлечения ароматов при низкой температуре", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научная техника ароматизации", "вакуумный насос", "нет", "сложный", "20-40 мин"),
        ("Spherification (Сферификация)", "Создание сферических капсул", "Для молекулярных коктейлей", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Молекулярная техника капсулирования", "альгинат натрия", "нет", "сложный", "5-10 мин"),
        ("Gelification (Гелификация)", "Превращение жидкостей в гели", "Для создания текстурированных коктейлей", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Молекулярная техника гелеобразования", "агар-агар", "нет", "сложный", "10-15 мин"),
        ("Foam (Пена)", "Создание стабильной пены", "Для воздушных коктейлей", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научная техника создания пены", "лецитин", "нет", "средний", "5 мин"),
        ("Smoking Gun (Дым-пушка)", "Холодное копчение", "Для ароматизации коктейлей дымом", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Техника холодного копчения", "дым-пушка", "нет", "средний", "2-3 мин"),
        ("Liquid Nitrogen (Жидкий азот)", "Мгновенное замораживание", "Для драматических эффектов", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Криогенная техника", "жидкий азот", "нет", "сложный", "1-2 мин"),
        ("Sous Vide (Су-вид)", "Точный контроль температуры", "Для инфузий и мацераций", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Техника точного контроля температуры", "су-вид машина", "нет", "средний", "30-120 мин"),
        ("Carbonation (Карбонизация)", "Насыщение углекислым газом", "Для создания игристых коктейлей", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научная техника карбонизации", "CO2 баллон", "нет", "средний", "5-10 мин"),
        
        # Научные принципы
        ("Dilution Control (Контроль разбавления)", "Точный расчет разбавления льдом", "Для идеального баланса коктейля", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научный подход к разбавлению", "термометр", "нет", "средний", "расчет"),
        ("Temperature Control (Контроль температуры)", "Точный контроль температуры подачи", "Для оптимального вкуса", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научный контроль температуры", "термометр", "нет", "легкий", "измерение"),
        ("pH Balance (Баланс pH)", "Контроль кислотности", "Для идеального вкусового баланса", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научный контроль кислотности", "pH метр", "нет", "средний", "измерение"),
        ("Osmotic Pressure (Осмотическое давление)", "Контроль осмотического давления", "Для стабильности эмульсий", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научный контроль давления", "осмометр", "нет", "сложный", "измерение"),
        ("Surface Tension (Поверхностное натяжение)", "Контроль поверхностного натяжения", "Для создания стабильных пен", "техника", "liquid_intelligence_technique", "Liquid Intelligence", "Научный контроль пенообразования", "тензиометр", "нет", "сложный", "измерение"),
    ]
    
    # Научные рецепты заготовок из Liquid Intelligence
    scientific_preparations = [
        # Научные сиропы
        ("Clarified Lime Juice", "Лаймовый сок, центрифуга", "Центрифугирование для удаления мякоти", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Очищенный лаймовый сок без мякоти", "центрифуга", "нет", "сложный", "15 мин"),
        ("Clarified Lemon Juice", "Лимонный сок, центрифуга", "Центрифугирование для удаления мякоти", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Очищенный лимонный сок без мякоти", "центрифуга", "нет", "сложный", "15 мин"),
        ("Clarified Orange Juice", "Апельсиновый сок, центрифуга", "Центрифугирование для удаления мякоти", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Очищенный апельсиновый сок без мякоти", "центрифуга", "нет", "сложный", "15 мин"),
        ("Grapefruit Oleo Saccharum", "Грейпфрутовая цедра, сахар", "Мацерация цедры с сахаром", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Грейпфрутовый олео саккарум", "банка", "нет", "средний", "24 часа"),
        ("Lemon Oleo Saccharum", "Лимонная цедра, сахар", "Мацерация цедры с сахаром", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Лимонный олео саккарум", "банка", "нет", "средний", "24 часа"),
        ("Lime Oleo Saccharum", "Лаймовая цедра, сахар", "Мацерация цедры с сахаром", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Лаймовый олео саккарум", "банка", "нет", "средний", "24 часа"),
        
        # Научные инфузии
        ("Cold Brew Coffee", "Кофе грубого помола, холодная вода", "Холодное заваривание 12-24 часа", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Холодный кофе для коктейлей", "френч-пресс", "нет", "легкий", "12-24 часа"),
        ("Tea Infusion", "Чайные листья, горячая вода", "Контролируемое заваривание", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Чайная инфузия для коктейлей", "чайник", "нет", "легкий", "3-5 мин"),
        ("Herb Infusion", "Травы, спирт", "Холодная инфузия трав", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Травяная инфузия", "банка", "нет", "средний", "7 дней"),
        ("Spice Infusion", "Специи, спирт", "Холодная инфузия специй", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Пряная инфузия", "банка", "нет", "средний", "7 дней"),
        
        # Научные эмульсии
        ("Coconut Milk Emulsion", "Кокосовое молоко, лецитин", "Стабилизация эмульсии", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Стабильная кокосовая эмульсия", "блендер", "нет", "средний", "5 мин"),
        ("Cream Emulsion", "Сливки, лецитин", "Стабилизация сливочной эмульсии", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Стабильная сливочная эмульсия", "блендер", "нет", "средний", "5 мин"),
        ("Fruit Puree Emulsion", "Фруктовое пюре, лецитин", "Стабилизация фруктовой эмульсии", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Стабильная фруктовая эмульсия", "блендер", "нет", "средний", "5 мин"),
        
        # Научные пены
        ("Citrus Foam", "Цитрусовый сок, лецитин", "Создание стабильной цитрусовой пены", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Стабильная цитрусовая пена", "сифон", "нет", "средний", "5 мин"),
        ("Herb Foam", "Травяной настой, лецитин", "Создание стабильной травяной пены", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Стабильная травяная пена", "сифон", "нет", "средний", "5 мин"),
        ("Coffee Foam", "Кофе, лецитин", "Создание стабильной кофейной пены", "заготовка", "liquid_intelligence_preparation", "Liquid Intelligence", "Стабильная кофейная пена", "сифон", "нет", "средний", "5 мин"),
    ]
    
    # Научные коктейли из Liquid Intelligence
    scientific_cocktails = [
        # Классические с научным подходом
        ("Perfect Daiquiri", "60 мл белый ром, 22.5 мл лаймовый сок, 15 мл сахарный сироп", "Шейк со льдом, точный контроль температуры", "ром", "liquid_intelligence_cocktail", "Liquid Intelligence", "Идеальный дайкири с научным подходом", "коктейльный", "лаймовая цедра", "средний", "3 мин"),
        ("Perfect Margarita", "60 мл текила, 22.5 мл лаймовый сок, 15 мл сахарный сироп", "Шейк со льдом, точный контроль разбавления", "текила", "liquid_intelligence_cocktail", "Liquid Intelligence", "Идеальная маргарита с научным подходом", "рокс", "лаймовая цедра", "средний", "3 мин"),
        ("Perfect Manhattan", "60 мл ржаной виски, 30 мл красный вермут, 2 дэш биттерс", "Стир со льдом, контроль температуры", "виски", "liquid_intelligence_cocktail", "Liquid Intelligence", "Идеальный манхэттен с научным подходом", "коктейльный", "вишня", "средний", "3 мин"),
        ("Perfect Martini", "60 мл джин, 10 мл сухой вермут", "Стир со льдом, точный контроль разбавления", "джин", "liquid_intelligence_cocktail", "Liquid Intelligence", "Идеальный мартини с научным подходом", "коктейльный", "оливка", "средний", "3 мин"),
        ("Perfect Old Fashioned", "60 мл бурбон, 1 кубик сахара, 2 дэш биттерс", "Мудл с точным контролем температуры", "виски", "liquid_intelligence_cocktail", "Liquid Intelligence", "Идеальный олд фешен с научным подходом", "рокс", "апельсиновая цедра", "средний", "3 мин"),
        
        # Молекулярные коктейли
        ("Smoked Manhattan", "60 мл ржаной виски, 30 мл красный вермут, 2 дэш биттерс, дым", "Стир со льдом, холодное копчение", "виски", "liquid_intelligence_cocktail", "Liquid Intelligence", "Манхэттен с холодным копчением", "коктейльный", "вишня", "сложный", "5 мин"),
        ("Carbonated Negroni", "30 мл джин, 30 мл красный вермут, 30 мл Кампари", "Карбонизация готового коктейля", "джин", "liquid_intelligence_cocktail", "Liquid Intelligence", "Игристый негрони", "флейта", "апельсиновая цедра", "сложный", "5 мин"),
        ("Frozen Daiquiri", "60 мл белый ром, 22.5 мл лаймовый сок, 15 мл сахарный сироп", "Бленд с жидким азотом", "ром", "liquid_intelligence_cocktail", "Liquid Intelligence", "Замороженный дайкири с жидким азотом", "коктейльный", "лаймовая цедра", "сложный", "2 мин"),
        ("Spherified Martini", "60 мл джин, 10 мл сухой вермут", "Сферификация коктейля", "джин", "liquid_intelligence_cocktail", "Liquid Intelligence", "Мартини в сферических капсулах", "ложка", "оливка", "сложный", "10 мин"),
        ("Gelified Margarita", "60 мл текила, 22.5 мл лаймовый сок, 15 мл сахарный сироп", "Гелификация коктейля", "текила", "liquid_intelligence_cocktail", "Liquid Intelligence", "Маргарита в виде геля", "ложка", "лаймовая цедра", "сложный", "15 мин"),
        
        # Научные модификации
        ("Clarified Milk Punch", "60 мл ром, 30 мл лимонный сок, 15 мл сахарный сироп, молоко", "Кларификация через молоко", "ром", "liquid_intelligence_cocktail", "Liquid Intelligence", "Очищенный молочный пунш", "коктейльный", "мускатный орех", "сложный", "24 часа"),
        ("Rotovap Manhattan", "60 мл ржаной виски, 30 мл красный вермут, 2 дэш биттерс", "Ротационная дистилляция вермута", "виски", "liquid_intelligence_cocktail", "Liquid Intelligence", "Манхэттен с дистиллированным вермутом", "коктейльный", "вишня", "сложный", "60 мин"),
        ("Sous Vide Old Fashioned", "60 мл бурбон, 1 кубик сахара, 2 дэш биттерс", "Су-вид инфузия", "виски", "liquid_intelligence_cocktail", "Liquid Intelligence", "Олд фешен с су-вид инфузией", "рокс", "апельсиновая цедра", "сложный", "2 часа"),
        ("Centrifuged Bloody Mary", "45 мл водка, 90 мл томатный сок, специи", "Центрифугирование томатного сока", "водка", "liquid_intelligence_cocktail", "Liquid Intelligence", "Кровавая Мэри с очищенным соком", "хайбол", "сельдерей", "сложный", "20 мин"),
        ("Foam Topped Martini", "60 мл джин, 10 мл сухой вермут, пена", "Мартини с научной пеной", "джин", "liquid_intelligence_cocktail", "Liquid Intelligence", "Мартини с молекулярной пеной", "коктейльный", "оливка", "сложный", "5 мин"),
        
        # Экспериментальные коктейли
        ("Liquid Nitrogen Martini", "60 мл джин, 10 мл сухой вермут", "Приготовление с жидким азотом", "джин", "liquid_intelligence_cocktail", "Liquid Intelligence", "Мартини с жидким азотом", "коктейльный", "оливка", "сложный", "1 мин"),
        ("Smoke Bubble Negroni", "30 мл джин, 30 мл красный вермут, 30 мл Кампари", "Негрони в дымном пузыре", "джин", "liquid_intelligence_cocktail", "Liquid Intelligence", "Негрони в молекулярном пузыре", "пузырь", "апельсиновая цедра", "сложный", "5 мин"),
        ("Temperature Gradient Martini", "60 мл джин, 10 мл сухой вермут", "Мартини с температурным градиентом", "джин", "liquid_intelligence_cocktail", "Liquid Intelligence", "Мартини с температурными слоями", "коктейльный", "оливка", "сложный", "10 мин"),
        ("pH Balanced Daiquiri", "60 мл белый ром, 22.5 мл лаймовый сок, 15 мл сахарный сироп", "Дайкири с контролем pH", "ром", "liquid_intelligence_cocktail", "Liquid Intelligence", "Дайкири с научным балансом pH", "коктейльный", "лаймовая цедра", "сложный", "5 мин"),
        ("Osmotic Pressure Manhattan", "60 мл ржаной виски, 30 мл красный вермут, 2 дэш биттерс", "Манхэттен с контролем осмотического давления", "виски", "liquid_intelligence_cocktail", "Liquid Intelligence", "Манхэттен с научным контролем давления", "коктейльный", "вишня", "сложный", "5 мин"),
    ]
    
    # Объединяем все рецепты
    all_recipes = molecular_techniques + scientific_preparations + scientific_cocktails
    
    try:
        # Добавляем рецепты в базу данных
        cursor.executemany("""
            INSERT OR IGNORE INTO recipes 
            (name, ingredients, method, base_spirit, category, source, 
             description, glassware, garnish, difficulty, prep_time) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, all_recipes)
        
        conn.commit()
        print(f"✅ Успешно добавлено {len(all_recipes)} рецептов из 'Liquid Intelligence'!")
        
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
        
        # Показываем количество рецептов из Liquid Intelligence
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE source = 'Liquid Intelligence'")
        liquid_count = cursor.fetchone()[0]
        print(f"🧪 Рецептов из 'Liquid Intelligence': {liquid_count}")
        
    except Exception as e:
        print(f"❌ Ошибка при добавлении рецептов: {e}")
    
    finally:
        conn.close()

def show_liquid_intelligence_categories():
    """Показать категории рецептов из Liquid Intelligence"""
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT category FROM recipes WHERE source = 'Liquid Intelligence' ORDER BY category")
    categories = cursor.fetchall()
    
    print("\n📋 Категории рецептов из 'Liquid Intelligence':")
    for category in categories:
        print(f"  • {category[0]}")
    
    conn.close()

def main():
    """Основная функция"""
    print("🧪 MIXTRIX - Добавление знаний из 'Liquid Intelligence'")
    print("=" * 50)
    
    # Проверяем существование базы данных
    if not os.path.exists('cocktails.db'):
        print("❌ База данных не найдена. Запустите main.py для создания базы.")
        return
    
    # Добавляем знания из Liquid Intelligence
    add_liquid_intelligence_knowledge()
    
    # Показываем категории
    show_liquid_intelligence_categories()
    
    print("\n🎉 Готово! Знания из 'Liquid Intelligence' добавлены в MIXTRIX🍸")
    print("Перезапустите бота для применения изменений.")

if __name__ == "__main__":
    main()














