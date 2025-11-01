import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class CocktailDatabase:
    """Класс для работы с базой данных коктейлей"""
    
    def __init__(self, db_path: str = "cocktails.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица рецептов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    base_spirit TEXT NOT NULL,
                    ingredients TEXT NOT NULL,  -- JSON строка
                    method TEXT NOT NULL,
                    garnish TEXT,
                    glass_type TEXT,
                    description TEXT,
                    history TEXT,
                    season TEXT,
                    difficulty TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица сезонных ингредиентов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS seasonal_ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month TEXT NOT NULL,
                    ingredient TEXT NOT NULL,
                    description TEXT,
                    pairing_suggestions TEXT,  -- JSON строка
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица трендов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trends (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    trend_name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    examples TEXT,  -- JSON строка
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица фудпейринга
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS food_pairing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    spirit TEXT NOT NULL,
                    ingredient TEXT NOT NULL,
                    pairing_strength INTEGER NOT NULL,  -- 1-5
                    notes TEXT,
                    source TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def add_recipe(self, recipe_data: Dict) -> int:
        """Добавление нового рецепта"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO recipes (
                    name, base_spirit, ingredients, method, garnish, 
                    glass_type, description, history, season, difficulty
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                recipe_data['name'],
                recipe_data['base_spirit'],
                json.dumps(recipe_data['ingredients']),
                recipe_data['method'],
                recipe_data.get('garnish', ''),
                recipe_data.get('glass_type', ''),
                recipe_data.get('description', ''),
                recipe_data.get('history', ''),
                recipe_data.get('season', ''),
                recipe_data.get('difficulty', 'medium')
            ))
            
            return cursor.lastrowid
    
    def get_recipe_by_name(self, name: str) -> Optional[Dict]:
        """Получение рецепта по имени"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes WHERE name = ?", (name,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_recipe_dict(row)
            return None
    
    def get_recipes_by_spirit(self, spirit: str) -> List[Dict]:
        """Получение рецептов по базовому спирту"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes WHERE base_spirit = ?", (spirit,))
            rows = cursor.fetchall()
            
            return [self._row_to_recipe_dict(row) for row in rows]
    
    def get_seasonal_recipes(self, month: str) -> List[Dict]:
        """Получение сезонных рецептов"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes WHERE season = ?", (month,))
            rows = cursor.fetchall()
            
            return [self._row_to_recipe_dict(row) for row in rows]
    
    def get_all_recipes(self) -> List[Dict]:
        """Получение всех рецептов"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes")
            rows = cursor.fetchall()
            
            return [self._row_to_recipe_dict(row) for row in rows]
    
    def add_seasonal_ingredient(self, month: str, ingredient: str, 
                              description: str = "", pairing_suggestions: List[str] = None):
        """Добавление сезонного ингредиента"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO seasonal_ingredients (month, ingredient, description, pairing_suggestions)
                VALUES (?, ?, ?, ?)
            """, (month, ingredient, description, json.dumps(pairing_suggestions or [])))
    
    def get_seasonal_ingredients(self, month: str) -> List[Dict]:
        """Получение сезонных ингредиентов для месяца"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM seasonal_ingredients WHERE month = ?", (month,))
            rows = cursor.fetchall()
            
            return [{
                'id': row[0],
                'month': row[1],
                'ingredient': row[2],
                'description': row[3],
                'pairing_suggestions': json.loads(row[4]) if row[4] else [],
                'created_at': row[5]
            } for row in rows]
    
    def add_trend(self, year: int, trend_name: str, description: str, 
                  examples: List[str] = None, is_active: bool = True):
        """Добавление тренда"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trends (year, trend_name, description, examples, is_active)
                VALUES (?, ?, ?, ?, ?)
            """, (year, trend_name, description, json.dumps(examples or []), is_active))
    
    def get_active_trends(self, year: int = None) -> List[Dict]:
        """Получение активных трендов"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if year:
                cursor.execute("SELECT * FROM trends WHERE year = ? AND is_active = 1", (year,))
            else:
                cursor.execute("SELECT * FROM trends WHERE is_active = 1")
            rows = cursor.fetchall()
            
            return [{
                'id': row[0],
                'year': row[1],
                'trend_name': row[2],
                'description': row[3],
                'examples': json.loads(row[4]) if row[4] else [],
                'is_active': bool(row[5]),
                'created_at': row[6]
            } for row in rows]
    
    def add_food_pairing(self, spirit: str, ingredient: str, 
                        pairing_strength: int, notes: str = "", source: str = ""):
        """Добавление фудпейринга"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO food_pairing (spirit, ingredient, pairing_strength, notes, source)
                VALUES (?, ?, ?, ?, ?)
            """, (spirit, ingredient, pairing_strength, notes, source))
    
    def get_food_pairings(self, spirit: str) -> List[Dict]:
        """Получение фудпейрингов для спирта"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM food_pairing 
                WHERE spirit = ? 
                ORDER BY pairing_strength DESC
            """, (spirit,))
            rows = cursor.fetchall()
            
            return [{
                'id': row[0],
                'spirit': row[1],
                'ingredient': row[2],
                'pairing_strength': row[3],
                'notes': row[4],
                'source': row[5],
                'created_at': row[6]
            } for row in rows]
    
    def _row_to_recipe_dict(self, row) -> Dict:
        """Преобразование строки БД в словарь рецепта"""
        # Пытаемся парсить ингредиенты как JSON, если не получается - используем как текст
        try:
            ingredients = json.loads(row[3]) if row[3] else {}
        except (json.JSONDecodeError, TypeError):
            # Если это не JSON, создаем словарь из текста
            ingredients = {"ингредиенты": row[3]} if row[3] else {}
        
        return {
            'id': row[0],
            'name': row[1],
            'base_spirit': row[2],
            'ingredients': ingredients,
            'method': row[4],
            'garnish': row[5],
            'glass_type': row[6],
            'description': row[7],
            'history': row[8],
            'season': row[9],
            'difficulty': row[10],
            'created_at': row[11],
            'updated_at': row[12]
        }
    
    def search_recipes(self, query: str) -> List[Dict]:
        """Поиск рецептов по названию или описанию"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM recipes 
                WHERE name LIKE ? OR description LIKE ? OR history LIKE ?
            """, (f"%{query}%", f"%{query}%", f"%{query}%"))
            rows = cursor.fetchall()
            
            return [self._row_to_recipe_dict(row) for row in rows]

def init_sample_data():
    """Инициализация базы данных с примерными данными"""
    db = CocktailDatabase()
    
    # Добавляем сезонные ингредиенты для России
    seasonal_ingredients = [
        # Зима
        ('winter', 'клюква', 'Тартовая зимняя клюква', ['водка', 'джин', 'ром']),
        ('winter', 'брусника', 'Сладкая брусника', ['водка', 'джин', 'коньяк']),
        ('winter', 'облепиха', 'Витаминная облепиха', ['водка', 'джин', 'текила']),
        ('winter', 'цитрусы', 'Свежие цитрусы', ['джин', 'водка', 'текила']),
        ('winter', 'корица', 'Теплая корица', ['ром', 'виски', 'коньяк']),
        ('winter', 'гвоздика', 'Пряная гвоздика', ['ром', 'виски', 'коньяк']),
        ('winter', 'мускатный орех', 'Ароматный мускат', ['ром', 'виски', 'коньяк']),
        ('winter', 'ваниль', 'Сладкая ваниль', ['ром', 'виски', 'коньяк']),
        
        # Весна
        ('spring', 'ревень', 'Кислый ревень', ['джин', 'водка', 'текила']),
        ('spring', 'щавель', 'Тартовый щавель', ['джин', 'водка', 'текила']),
        ('spring', 'молодые травы', 'Свежие весенние травы', ['джин', 'водка', 'текила']),
        ('spring', 'цветы сирени', 'Ароматные цветы сирени', ['джин', 'водка', 'коньяк']),
        ('spring', 'черемуха', 'Сладкая черемуха', ['джин', 'водка', 'коньяк']),
        ('spring', 'мелисса', 'Лимонная мелисса', ['джин', 'водка', 'текила']),
        ('spring', 'мята', 'Свежая мята', ['джин', 'водка', 'текила']),
        
        # Лето
        ('summer', 'клубника', 'Сладкая клубника', ['джин', 'водка', 'ром']),
        ('summer', 'малина', 'Ароматная малина', ['джин', 'водка', 'ром']),
        ('summer', 'смородина', 'Тартовая смородина', ['джин', 'водка', 'ром']),
        ('summer', 'крыжовник', 'Кислый крыжовник', ['джин', 'водка', 'текила']),
        ('summer', 'вишня', 'Сладкая вишня', ['джин', 'водка', 'ром']),
        ('summer', 'базилик', 'Ароматный базилик', ['джин', 'водка', 'текила']),
        ('summer', 'укроп', 'Свежий укроп', ['водка', 'джин', 'текила']),
        ('summer', 'петрушка', 'Зеленая петрушка', ['водка', 'джин', 'текила']),
        
        # Осень
        ('autumn', 'яблоки', 'Сезонные яблоки', ['джин', 'виски', 'кальвадос']),
        ('autumn', 'груши', 'Сладкие груши', ['джин', 'коньяк', 'виски']),
        ('autumn', 'сливы', 'Сочные сливы', ['джин', 'водка', 'коньяк']),
        ('autumn', 'тыква', 'Осенняя тыква', ['ром', 'виски', 'коньяк']),
        ('autumn', 'калина', 'Тартовая калина', ['водка', 'джин', 'ром']),
        ('autumn', 'рябина', 'Горьковатая рябина', ['водка', 'джин', 'ром']),
        ('autumn', 'орехи', 'Осенние орехи', ['ром', 'виски', 'коньяк']),
        ('autumn', 'мед', 'Натуральный мед', ['ром', 'виски', 'коньяк'])
    ]
    
    for ingredient in seasonal_ingredients:
        db.add_seasonal_ingredient(*ingredient)
    
    # Добавляем тренды 2025
    trends_2025 = [
        (2025, 'Zero-Proof Revolution', 'Сложные безалкогольные коктейли с ферментированными ингредиентами', 
         ['комбуча', 'кефир', 'квас', 'ферментированные овощи']),
        (2025, 'Fat-Washing', 'Настаивание спирта на жирах для создания кремовой текстуры', 
         ['масло', 'бекон', 'орехи', 'авокадо']),
        (2025, 'Сезонные ингредиенты', 'Локальные и сезонные продукты в коктейлях', 
         ['дикие травы', 'цветы', 'ферментированные фрукты']),
        (2025, 'Молекулярная гастрономия', 'Современные техники приготовления коктейлей', 
         ['сферы', 'пена', 'гели', 'криогенные методы'])
    ]
    
    for trend in trends_2025:
        db.add_trend(*trend)
    
    # Добавляем фудпейринги
    food_pairings = [
        ('джин', 'яблоки', 5, 'Классическое сочетание из The Flavor Bible', 'The Flavor Bible'),
        ('джин', 'груши', 4, 'Свежий и элегантный вкус', 'The Flavor Bible'),
        ('джин', 'клюква', 4, 'Тартовый контраст с джином', 'The Flavor Bible'),
        ('виски', 'корица', 5, 'Теплое и пряное сочетание', 'The Flavor Bible'),
        ('виски', 'тыква', 4, 'Осенний комфорт', 'The Flavor Bible'),
        ('ром', 'корица', 5, 'Карибская классика', 'The Flavor Bible'),
        ('ром', 'мускатный орех', 4, 'Тропическая пряность', 'The Flavor Bible'),
        ('текила', 'лайм', 5, 'Мексиканская классика', 'The Flavor Bible'),
        ('водка', 'клюква', 4, 'Чистый и свежий вкус', 'The Flavor Bible')
    ]
    
    for pairing in food_pairings:
        db.add_food_pairing(*pairing)
    
    print("✅ База данных инициализирована с примерными данными")

if __name__ == "__main__":
    init_sample_data()
