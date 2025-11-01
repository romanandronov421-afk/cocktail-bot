#!/usr/bin/env python3
"""
MIXTRIX Professional Database Population
Заполнение профессиональной базы данных классическими коктейлями
и знаниями из профессиональных книг барного ремесла
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List

class MIXTRIXDatabasePopulator:
    """Класс для заполнения профессиональной базы данных MIXTRIX"""
    
    def __init__(self, db_path: str = "mixtrix_professional.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def populate_ingredients_catalog(self):
        """Заполнение каталога профессиональных ингредиентов"""
        print("📦 Заполнение каталога ингредиентов...")
        
        # Базовые спирты с детальной информацией
        base_spirits = [
            {
                "name": "джин лондонский",
                "name_en": "London Dry Gin",
                "category": "base_spirits",
                "subcategory": "gin",
                "alcohol_content": 40.0,
                "flavor_profile": ["juniper", "citrus", "herbal", "botanical"],
                "seasonality": {"spring": True, "summer": True, "autumn": True, "winter": True},
                "russian_availability": {"spring": True, "summer": True, "autumn": True, "winter": True},
                "substitutes": ["джин голландский", "джин американский"],
                "pairing_suggestions": ["цитрусы", "тоник", "вермут", "оливки"],
                "cost_tier": "medium",
                "description": "Классический лондонский джин с выраженным вкусом можжевельника",
                "origin": "Великобритания"
            },
            {
                "name": "водка премиум",
                "name_en": "Premium Vodka",
                "category": "base_spirits",
                "subcategory": "vodka",
                "alcohol_content": 40.0,
                "flavor_profile": ["neutral", "clean", "smooth"],
                "seasonality": {"spring": True, "summer": True, "autumn": True, "winter": True},
                "russian_availability": {"spring": True, "summer": True, "autumn": True, "winter": True},
                "substitutes": ["водка стандартная", "водка люкс"],
                "pairing_suggestions": ["цитрусы", "ягоды", "травы", "специи"],
                "cost_tier": "high",
                "description": "Премиальная водка с чистым вкусом и мягкостью",
                "origin": "Россия"
            },
            {
                "name": "ром белый",
                "name_en": "White Rum",
                "category": "base_spirits",
                "subcategory": "rum",
                "alcohol_content": 40.0,
                "flavor_profile": ["sweet", "tropical", "vanilla", "caramel"],
                "seasonality": {"spring": True, "summer": True, "autumn": False, "winter": False},
                "russian_availability": {"spring": True, "summer": True, "autumn": False, "winter": False},
                "substitutes": ["ром золотой", "ром темный"],
                "pairing_suggestions": ["тропические фрукты", "кокос", "лайм", "мята"],
                "cost_tier": "medium",
                "description": "Белый ром с тропическими нотами",
                "origin": "Карибы"
            }
        ]
        
        # Ликёры и биттеры
        liqueurs = [
            {
                "name": "кампари",
                "name_en": "Campari",
                "category": "liqueurs",
                "subcategory": "bitter_liqueur",
                "alcohol_content": 25.0,
                "flavor_profile": ["bitter", "herbal", "citrus", "spicy"],
                "seasonality": {"spring": True, "summer": True, "autumn": True, "winter": True},
                "russian_availability": {"spring": True, "summer": True, "autumn": True, "winter": True},
                "substitutes": ["апероль", "цинаро"],
                "pairing_suggestions": ["вермут", "цитрусы", "газировка", "горькие травы"],
                "cost_tier": "medium",
                "description": "Итальянский горький ликёр с травяными нотами",
                "origin": "Италия"
            },
            {
                "name": "трипл сек",
                "name_en": "Triple Sec",
                "category": "liqueurs",
                "subcategory": "orange_liqueur",
                "alcohol_content": 30.0,
                "flavor_profile": ["sweet", "orange", "citrus", "floral"],
                "seasonality": {"spring": True, "summer": True, "autumn": True, "winter": True},
                "russian_availability": {"spring": True, "summer": True, "autumn": True, "winter": True},
                "substitutes": ["куантро", "гранд марнье", "синий кюрасао"],
                "pairing_suggestions": ["цитрусы", "текила", "джин", "ром"],
                "cost_tier": "medium",
                "description": "Апельсиновый ликёр с выраженным цитрусовым вкусом",
                "origin": "Франция"
            }
        ]
        
        # Сезонные ингредиенты для России
        seasonal_ingredients = [
            {
                "name": "ревень",
                "name_en": "Rhubarb",
                "category": "seasonal",
                "subcategory": "spring_vegetable",
                "alcohol_content": 0.0,
                "flavor_profile": ["tart", "vegetal", "acidic"],
                "seasonality": {"spring": True, "summer": False, "autumn": False, "winter": False},
                "russian_availability": {"spring": True, "summer": False, "autumn": False, "winter": False},
                "substitutes": ["щавель", "лимонная кислота"],
                "pairing_suggestions": ["джин", "водка", "мед", "имбирь"],
                "cost_tier": "low",
                "description": "Весенний овощ с кислым вкусом, популярен в России",
                "origin": "Россия"
            },
            {
                "name": "облепиха",
                "name_en": "Sea Buckthorn",
                "category": "seasonal",
                "subcategory": "autumn_berry",
                "alcohol_content": 0.0,
                "flavor_profile": ["tart", "citrus", "vitamin_c"],
                "seasonality": {"spring": False, "summer": False, "autumn": True, "winter": True},
                "russian_availability": {"spring": False, "summer": False, "autumn": True, "winter": True},
                "substitutes": ["клюква", "брусника"],
                "pairing_suggestions": ["водка", "мед", "травы", "специи"],
                "cost_tier": "low",
                "description": "Осенняя ягода с высоким содержанием витамина C",
                "origin": "Россия"
            },
            {
                "name": "брусника",
                "name_en": "Lingonberry",
                "category": "seasonal",
                "subcategory": "autumn_berry",
                "alcohol_content": 0.0,
                "flavor_profile": ["tart", "sweet", "earthy"],
                "seasonality": {"spring": False, "summer": False, "autumn": True, "winter": True},
                "russian_availability": {"spring": False, "summer": False, "autumn": True, "winter": True},
                "substitutes": ["клюква", "облепиха"],
                "pairing_suggestions": ["водка", "коньяк", "мед", "ваниль"],
                "cost_tier": "low",
                "description": "Традиционная русская ягода с терпким вкусом",
                "origin": "Россия"
            }
        ]
        
        # Добавляем все ингредиенты в базу
        all_ingredients = base_spirits + liqueurs + seasonal_ingredients
        
        for ingredient in all_ingredients:
            try:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO ingredients 
                    (name, name_en, category, subcategory, alcohol_content, flavor_profile, 
                     seasonality, russian_availability, substitutes, pairing_suggestions, 
                     cost_tier, description, origin)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ingredient["name"],
                    ingredient["name_en"],
                    ingredient["category"],
                    ingredient["subcategory"],
                    ingredient["alcohol_content"],
                    json.dumps(ingredient["flavor_profile"]),
                    json.dumps(ingredient["seasonality"]),
                    json.dumps(ingredient["russian_availability"]),
                    json.dumps(ingredient["substitutes"]),
                    json.dumps(ingredient["pairing_suggestions"]),
                    ingredient["cost_tier"],
                    ingredient["description"],
                    ingredient["origin"]
                ))
            except Exception as e:
                print(f"❌ Ошибка добавления ингредиента {ingredient['name']}: {e}")
        
        self.conn.commit()
        print(f"✅ Добавлено {len(all_ingredients)} профессиональных ингредиентов")
    
    def populate_classic_cocktails(self):
        """Заполнение классическими коктейлями из профессиональных источников"""
        print("🍸 Заполнение классическими коктейлями...")
        
        # Классические коктейли из Savoy Cocktail Book
        savoy_cocktails = [
            {
                "id": "savoy_001",
                "name": "Мартини",
                "name_en": "Martini",
                "category": "classic",
                "difficulty": "intermediate",
                "base_spirit": "джин лондонский",
                "ingredients": {
                    "джин лондонский": {"amount": 60, "unit": "ml", "technique": "stir"},
                    "сухой вермут": {"amount": 10, "unit": "ml", "technique": "stir"},
                    "оливка": {"amount": 1, "unit": "шт", "technique": "garnish"}
                },
                "method": "Перемешать в стакане для смешивания со льдом, процедить в охлажденный бокал",
                "glassware": "коктейльный бокал",
                "garnish": "оливка или лимонная цедра",
                "description": "Классический коктейль, символ элегантности и утонченности",
                "description_en": "Classic cocktail, symbol of elegance and sophistication",
                "history": "Создан в конце 19 века, назван в честь мартини-вермута",
                "flavor_profile": ["dry", "herbal", "smooth", "elegant"],
                "food_pairings": ["устрицы", "икра", "сыр пармезан", "оливки"],
                "seasonal_availability": ["spring", "summer", "autumn", "winter"],
                "prep_time": 120,
                "cost_estimate": 150.0,
                "profit_margin": 0.7,
                "iba_status": True,
                "source_book": "The Savoy Cocktail Book",
                "author": "Harry Craddock"
            },
            {
                "id": "savoy_002",
                "name": "Негрони",
                "name_en": "Negroni",
                "category": "classic",
                "difficulty": "beginner",
                "base_spirit": "джин лондонский",
                "ingredients": {
                    "джин лондонский": {"amount": 30, "unit": "ml", "technique": "stir"},
                    "красный вермут": {"amount": 30, "unit": "ml", "technique": "stir"},
                    "кампари": {"amount": 30, "unit": "ml", "technique": "stir"},
                    "апельсиновая цедра": {"amount": 1, "unit": "шт", "technique": "garnish"}
                },
                "method": "Перемешать все ингредиенты со льдом, процедить в стакан со льдом",
                "glassware": "стакан олд-фешн",
                "garnish": "апельсиновая цедра",
                "description": "Итальянский классический коктейль с горьковатым вкусом",
                "description_en": "Italian classic cocktail with bitter taste",
                "history": "Создан в 1919 году во Флоренции графом Камилло Негрони",
                "flavor_profile": ["bitter", "herbal", "citrus", "complex"],
                "food_pairings": ["паста", "сыр горгонзола", "оливки", "анчоусы"],
                "seasonal_availability": ["spring", "summer", "autumn", "winter"],
                "prep_time": 90,
                "cost_estimate": 120.0,
                "profit_margin": 0.75,
                "iba_status": True,
                "source_book": "The Savoy Cocktail Book",
                "author": "Harry Craddock"
            }
        ]
        
        # Коктейли из The Joy of Mixology
        joy_cocktails = [
            {
                "id": "joy_001",
                "name": "Манхеттен",
                "name_en": "Manhattan",
                "category": "classic",
                "difficulty": "intermediate",
                "base_spirit": "виски ржаной",
                "ingredients": {
                    "виски ржаной": {"amount": 60, "unit": "ml", "technique": "stir"},
                    "красный вермут": {"amount": 30, "unit": "ml", "technique": "stir"},
                    "биттерс ангостура": {"amount": 2, "unit": "dash", "technique": "stir"},
                    "вишня": {"amount": 1, "unit": "шт", "technique": "garnish"}
                },
                "method": "Перемешать в стакане для смешивания со льдом, процедить в охлажденный бокал",
                "glassware": "коктейльный бокал",
                "garnish": "вишня мараскино",
                "description": "Классический американский коктейль с богатым вкусом",
                "description_en": "Classic American cocktail with rich flavor",
                "history": "Создан в 1870-х годах в Нью-Йорке",
                "flavor_profile": ["rich", "sweet", "spicy", "complex"],
                "food_pairings": ["стейк", "сыр чеддер", "орехи", "шоколад"],
                "seasonal_availability": ["autumn", "winter"],
                "prep_time": 120,
                "cost_estimate": 180.0,
                "profit_margin": 0.8,
                "iba_status": True,
                "source_book": "The Joy of Mixology",
                "author": "Gary Regan"
            }
        ]
        
        # Сезонные коктейли для России
        seasonal_cocktails = [
            {
                "id": "seasonal_001",
                "name": "Ревеневый Джин Физз",
                "name_en": "Rhubarb Gin Fizz",
                "category": "seasonal",
                "difficulty": "intermediate",
                "base_spirit": "джин лондонский",
                "ingredients": {
                    "джин лондонский": {"amount": 50, "unit": "ml", "technique": "shake"},
                    "ревеневый сироп": {"amount": 25, "unit": "ml", "technique": "shake"},
                    "сок лайма": {"amount": 20, "unit": "ml", "technique": "shake"},
                    "содовая": {"amount": 100, "unit": "ml", "technique": "top"},
                    "мята": {"amount": 3, "unit": "лист", "technique": "garnish"}
                },
                "method": "Встряхнуть первые три ингредиента со льдом, процедить в стакан со льдом, долить содовой",
                "glassware": "хайбол",
                "garnish": "листья мяты",
                "description": "Весенний коктейль с русским ревенем и освежающим вкусом",
                "description_en": "Spring cocktail with Russian rhubarb and refreshing taste",
                "history": "Современная интерпретация классического физза с русскими ингредиентами",
                "flavor_profile": ["tart", "refreshing", "herbal", "spring"],
                "food_pairings": ["зеленый салат", "рыба", "козьи сыры", "зелень"],
                "seasonal_availability": ["spring"],
                "prep_time": 150,
                "cost_estimate": 200.0,
                "profit_margin": 0.6,
                "iba_status": False,
                "source_book": "MIXTRIX Seasonal Collection",
                "author": "MIXTRIX Team"
            },
            {
                "id": "seasonal_002",
                "name": "Облепиховый Хот Тодди",
                "name_en": "Sea Buckthorn Hot Toddy",
                "category": "seasonal",
                "difficulty": "beginner",
                "base_spirit": "водка премиум",
                "ingredients": {
                    "водка премиум": {"amount": 50, "unit": "ml", "technique": "build"},
                    "облепиховый сироп": {"amount": 30, "unit": "ml", "technique": "build"},
                    "мед": {"amount": 15, "unit": "ml", "technique": "build"},
                    "горячая вода": {"amount": 150, "unit": "ml", "technique": "top"},
                    "корица": {"amount": 1, "unit": "палочка", "technique": "garnish"}
                },
                "method": "Смешать все ингредиенты в кружке, добавить горячую воду, перемешать",
                "glassware": "ирландская кружка",
                "garnish": "палочка корицы",
                "description": "Зимний согревающий коктейль с русской облепихой",
                "description_en": "Winter warming cocktail with Russian sea buckthorn",
                "history": "Современная интерпретация горячего тодди с русскими ингредиентами",
                "flavor_profile": ["warming", "tart", "spicy", "vitamin_c"],
                "food_pairings": ["печенье", "орехи", "мед", "имбирь"],
                "seasonal_availability": ["winter"],
                "prep_time": 180,
                "cost_estimate": 180.0,
                "profit_margin": 0.7,
                "iba_status": False,
                "source_book": "MIXTRIX Seasonal Collection",
                "author": "MIXTRIX Team"
            }
        ]
        
        # Добавляем все коктейли
        all_cocktails = savoy_cocktails + joy_cocktails + seasonal_cocktails
        
        for cocktail in all_cocktails:
            try:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO cocktails 
                    (id, name, name_en, category, difficulty, base_spirit, ingredients, 
                     method, glassware, garnish, description, description_en, history, 
                     flavor_profile, food_pairings, seasonal_availability, prep_time, 
                     cost_estimate, profit_margin, iba_status, source_book, author)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cocktail["id"],
                    cocktail["name"],
                    cocktail["name_en"],
                    cocktail["category"],
                    cocktail["difficulty"],
                    cocktail["base_spirit"],
                    json.dumps(cocktail["ingredients"]),
                    cocktail["method"],
                    cocktail["glassware"],
                    cocktail["garnish"],
                    cocktail["description"],
                    cocktail["description_en"],
                    cocktail["history"],
                    json.dumps(cocktail["flavor_profile"]),
                    json.dumps(cocktail["food_pairings"]),
                    json.dumps(cocktail["seasonal_availability"]),
                    cocktail["prep_time"],
                    cocktail["cost_estimate"],
                    cocktail["profit_margin"],
                    cocktail["iba_status"],
                    cocktail["source_book"],
                    cocktail["author"]
                ))
            except Exception as e:
                print(f"❌ Ошибка добавления коктейля {cocktail['name']}: {e}")
        
        self.conn.commit()
        print(f"✅ Добавлено {len(all_cocktails)} профессиональных коктейлей")
    
    def populate_food_pairings(self):
        """Заполнение базы данных фудпейринга"""
        print("🍽️ Заполнение базы фудпейринга...")
        
        # Фудпейринги на основе Flavor Bible
        food_pairings = [
            {
                "cocktail_id": "savoy_001",
                "dish_name": "устрицы",
                "dish_category": "seafood",
                "pairing_type": "complementary",
                "description": "Классическое сочетание сухого мартини с устрицами",
                "confidence_score": 0.9,
                "source": "Flavor Bible"
            },
            {
                "cocktail_id": "savoy_001",
                "dish_name": "икра",
                "dish_category": "luxury",
                "pairing_type": "complementary",
                "description": "Элегантное сочетание с икрой",
                "confidence_score": 0.85,
                "source": "Flavor Bible"
            },
            {
                "cocktail_id": "savoy_002",
                "dish_name": "паста карбонара",
                "dish_category": "italian",
                "pairing_type": "complementary",
                "description": "Итальянский коктейль с итальянской пастой",
                "confidence_score": 0.8,
                "source": "Flavor Bible"
            },
            {
                "cocktail_id": "joy_001",
                "dish_name": "стейк рибай",
                "dish_category": "meat",
                "pairing_type": "complementary",
                "description": "Богатый виски с сочным стейком",
                "confidence_score": 0.9,
                "source": "Flavor Bible"
            }
        ]
        
        for pairing in food_pairings:
            try:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO food_pairings 
                    (cocktail_id, dish_name, dish_category, pairing_type, 
                     description, confidence_score, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    pairing["cocktail_id"],
                    pairing["dish_name"],
                    pairing["dish_category"],
                    pairing["pairing_type"],
                    pairing["description"],
                    pairing["confidence_score"],
                    pairing["source"]
                ))
            except Exception as e:
                print(f"❌ Ошибка добавления фудпейринга: {e}")
        
        self.conn.commit()
        print(f"✅ Добавлено {len(food_pairings)} фудпейрингов")
    
    def populate_seasonal_menus(self):
        """Заполнение сезонных меню"""
        print("📋 Заполнение сезонных меню...")
        
        seasonal_menus = [
            {
                "id": "spring_menu_2024",
                "name": "Весеннее меню 2024",
                "type": "seasonal",
                "season": "spring",
                "theme": "Пробуждение природы",
                "cocktails": ["seasonal_001", "savoy_001"],
                "target_audience": "молодые профессионалы",
                "price_range": "medium-high",
                "description": "Свежие весенние коктейли с русскими ингредиентами",
                "created_by": "MIXTRIX Team"
            },
            {
                "id": "winter_menu_2024",
                "name": "Зимнее меню 2024",
                "type": "seasonal",
                "season": "winter",
                "theme": "Тепло и уют",
                "cocktails": ["seasonal_002", "joy_001"],
                "target_audience": "семейные пары",
                "price_range": "medium",
                "description": "Согревающие зимние коктейли с русскими ягодами",
                "created_by": "MIXTRIX Team"
            }
        ]
        
        for menu in seasonal_menus:
            try:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO cocktail_menus 
                    (id, name, type, season, theme, cocktails, target_audience, 
                     price_range, description, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    menu["id"],
                    menu["name"],
                    menu["type"],
                    menu["season"],
                    menu["theme"],
                    json.dumps(menu["cocktails"]),
                    menu["target_audience"],
                    menu["price_range"],
                    menu["description"],
                    menu["created_by"]
                ))
            except Exception as e:
                print(f"❌ Ошибка добавления меню: {e}")
        
        self.conn.commit()
        print(f"✅ Добавлено {len(seasonal_menus)} сезонных меню")
    
    def populate_horeca_news(self):
        """Заполнение новостей HORECA индустрии"""
        print("📰 Заполнение новостей HORECA...")
        
        horeca_news = [
            {
                "title": "Новые тренды в коктейльной культуре 2024",
                "content": "В 2024 году наблюдается рост интереса к сезонным коктейлям с локальными ингредиентами...",
                "source": "Difford's Guide",
                "category": "trends",
                "tags": ["тренды", "сезонность", "локальные ингредиенты"],
                "published_at": datetime.now(),
                "is_featured": True
            },
            {
                "title": "Российские бармены на международных конкурсах",
                "content": "Российские бармены показывают отличные результаты на международных соревнованиях...",
                "source": "Bar Magazine",
                "category": "competitions",
                "tags": ["конкурсы", "бармены", "Россия"],
                "published_at": datetime.now(),
                "is_featured": False
            }
        ]
        
        for news in horeca_news:
            try:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO horeca_news 
                    (title, content, source, category, tags, published_at, is_featured)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    news["title"],
                    news["content"],
                    news["source"],
                    news["category"],
                    json.dumps(news["tags"]),
                    news["published_at"],
                    news["is_featured"]
                ))
            except Exception as e:
                print(f"❌ Ошибка добавления новости: {e}")
        
        self.conn.commit()
        print(f"✅ Добавлено {len(horeca_news)} новостей HORECA")
    
    def populate_all(self):
        """Заполнение всей базы данных"""
        print("🍸 Заполнение профессиональной базы данных MIXTRIX...")
        print("=" * 60)
        
        self.populate_ingredients_catalog()
        self.populate_classic_cocktails()
        self.populate_food_pairings()
        self.populate_seasonal_menus()
        self.populate_horeca_news()
        
        print("=" * 60)
        print("✅ Профессиональная база данных MIXTRIX заполнена!")
        print("📊 Статистика:")
        print("• Ингредиенты: профессиональный каталог")
        print("• Коктейли: классические и сезонные")
        print("• Фудпейринг: на основе Flavor Bible")
        print("• Меню: сезонные предложения")
        print("• Новости: HORECA индустрия")
    
    def close(self):
        """Закрытие соединения с базой данных"""
        self.conn.close()

if __name__ == "__main__":
    populator = MIXTRIXDatabasePopulator()
    populator.populate_all()
    populator.close()












