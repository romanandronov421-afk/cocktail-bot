#!/usr/bin/env python3
"""
Расширенный класс для работы с функциями приложения "Коктейльная вечеринка"
"""

import sqlite3
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class CocktailPartyDatabase:
    """Расширенный класс для работы с функциями MIXTRIX"""
    
    def __init__(self, db_path: str = "cocktails.db"):
        self.db_path = db_path
    
    def add_user_ingredient(self, user_id: int, ingredient_name: str, category: str, amount: str = "", unit: str = "ml") -> bool:
        """Добавление ингредиента в бар пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO user_ingredients 
                    (user_id, ingredient_name, category, amount, unit)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, ingredient_name, category, amount, unit))
                return True
        except Exception as e:
            print(f"Ошибка добавления ингредиента: {e}")
            return False
    
    def get_user_ingredients(self, user_id: int) -> List[Dict]:
        """Получение ингредиентов пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ingredient_name, category, amount, unit 
                FROM user_ingredients 
                WHERE user_id = ?
                ORDER BY category, ingredient_name
            """, (user_id,))
            
            return [{
                'name': row[0],
                'category': row[1],
                'amount': row[2],
                'unit': row[3]
            } for row in cursor.fetchall()]
    
    def find_cocktails_by_ingredients(self, user_id: int) -> List[Dict]:
        """Поиск коктейлей, которые можно приготовить из имеющихся ингредиентов"""
        user_ingredients = self.get_user_ingredients(user_id)
        ingredient_names = [ing['name'].lower() for ing in user_ingredients]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes")
            all_recipes = cursor.fetchall()
            
            available_cocktails = []
            
            for recipe in all_recipes:
                recipe_id, name, ingredients_text, method, base_spirit, category, source, description, glassware, garnish, difficulty, prep_time, glass_type, history, season = recipe
                
                # Парсим ингредиенты
                try:
                    ingredients = json.loads(ingredients_text) if ingredients_text else {}
                except:
                    ingredients = {"ингредиенты": ingredients_text} if ingredients_text else {}
                
                # Проверяем, есть ли все необходимые ингредиенты
                recipe_ingredients = []
                if isinstance(ingredients, dict):
                    recipe_ingredients = [ing.lower() for ing in ingredients.keys()]
                elif isinstance(ingredients, str):
                    recipe_ingredients = [ingredients.lower()]
                
                # Проверяем совпадение ингредиентов
                matches = sum(1 for ing in recipe_ingredients if any(user_ing in ing for user_ing in ingredient_names))
                
                if matches > 0:
                    availability_percentage = (matches / len(recipe_ingredients)) * 100 if recipe_ingredients else 0
                    
                    available_cocktails.append({
                        'id': recipe_id,
                        'name': name,
                        'ingredients': ingredients,
                        'method': method,
                        'base_spirit': base_spirit,
                        'description': description,
                        'glass_type': glass_type,
                        'garnish': garnish,
                        'difficulty': difficulty,
                        'availability_percentage': availability_percentage,
                        'missing_ingredients': [ing for ing in recipe_ingredients if not any(user_ing in ing for user_ing in ingredient_names)]
                    })
            
            # Сортируем по проценту доступности
            return sorted(available_cocktails, key=lambda x: x['availability_percentage'], reverse=True)
    
    def rate_cocktail(self, user_id: int, cocktail_id: int, rating: int, review: str = "") -> bool:
        """Оценка коктейля пользователем"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO cocktail_ratings 
                    (user_id, cocktail_id, rating, review)
                    VALUES (?, ?, ?, ?)
                """, (user_id, cocktail_id, rating, review))
                return True
        except Exception as e:
            print(f"Ошибка оценки коктейля: {e}")
            return False
    
    def get_cocktail_rating(self, cocktail_id: int) -> Dict:
        """Получение рейтинга коктейля"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT AVG(rating), COUNT(rating), AVG(rating) * COUNT(rating) as weighted_score
                FROM cocktail_ratings 
                WHERE cocktail_id = ?
            """, (cocktail_id,))
            
            result = cursor.fetchone()
            return {
                'average_rating': result[0] if result[0] else 0,
                'total_ratings': result[1] if result[1] else 0,
                'weighted_score': result[2] if result[2] else 0
            }
    
    def add_to_favorites(self, user_id: int, cocktail_id: int) -> bool:
        """Добавление коктейля в избранное"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO favorite_cocktails 
                    (user_id, cocktail_id)
                    VALUES (?, ?)
                """, (user_id, cocktail_id))
                return True
        except Exception as e:
            print(f"Ошибка добавления в избранное: {e}")
            return False
    
    def get_favorites(self, user_id: int) -> List[Dict]:
        """Получение избранных коктейлей"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, fc.added_at
                FROM recipes r
                JOIN favorite_cocktails fc ON r.id = fc.cocktail_id
                WHERE fc.user_id = ?
                ORDER BY fc.added_at DESC
            """, (user_id,))
            
            recipes = cursor.fetchall()
            return [self._row_to_recipe_dict(recipe) for recipe in recipes]
    
    def create_custom_recipe(self, user_id: int, recipe_data: Dict) -> int:
        """Создание пользовательского рецепта"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO custom_recipes 
                    (user_id, name, ingredients, method, description, glass_type, garnish, difficulty, prep_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    recipe_data['name'],
                    json.dumps(recipe_data['ingredients']),
                    recipe_data['method'],
                    recipe_data.get('description', ''),
                    recipe_data.get('glass_type', ''),
                    recipe_data.get('garnish', ''),
                    recipe_data.get('difficulty', 'medium'),
                    recipe_data.get('prep_time', '')
                ))
                return cursor.lastrowid
        except Exception as e:
            print(f"Ошибка создания рецепта: {e}")
            return 0
    
    def get_custom_recipes(self, user_id: int) -> List[Dict]:
        """Получение пользовательских рецептов"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM custom_recipes 
                WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,))
            
            recipes = cursor.fetchall()
            return [self._custom_row_to_dict(recipe) for recipe in recipes]
    
    def create_collection(self, user_id: int, name: str, description: str, cocktail_ids: List[int], is_public: bool = False) -> int:
        """Создание подборки коктейлей"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO cocktail_collections 
                    (user_id, name, description, cocktail_ids, is_public)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, name, description, json.dumps(cocktail_ids), is_public))
                return cursor.lastrowid
        except Exception as e:
            print(f"Ошибка создания подборки: {e}")
            return 0
    
    def get_collections(self, user_id: int) -> List[Dict]:
        """Получение подборок пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM cocktail_collections 
                WHERE user_id = ? OR is_public = 1
                ORDER BY created_at DESC
            """, (user_id,))
            
            collections = cursor.fetchall()
            return [self._collection_row_to_dict(collection) for collection in collections]
    
    def advanced_search(self, filters: Dict) -> List[Dict]:
        """Продвинутый поиск коктейлей по фильтрам"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Базовый запрос
            query = "SELECT * FROM recipes WHERE 1=1"
            params = []
            
            # Фильтр по базовому спирту
            if filters.get('base_spirit'):
                query += " AND base_spirit LIKE ?"
                params.append(f"%{filters['base_spirit']}%")
            
            # Фильтр по сложности
            if filters.get('difficulty'):
                query += " AND difficulty = ?"
                params.append(filters['difficulty'])
            
            # Фильтр по категории
            if filters.get('category'):
                query += " AND category LIKE ?"
                params.append(f"%{filters['category']}%")
            
            # Фильтр по названию
            if filters.get('name'):
                query += " AND name LIKE ?"
                params.append(f"%{filters['name']}%")
            
            cursor.execute(query, params)
            recipes = cursor.fetchall()
            
            return [self._row_to_recipe_dict(recipe) for recipe in recipes]
    
    def get_ingredient_catalog(self, category: str = None) -> List[Dict]:
        """Получение каталога ингредиентов"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if category:
                cursor.execute("""
                    SELECT * FROM ingredient_catalog 
                    WHERE category = ?
                    ORDER BY name
                """, (category,))
            else:
                cursor.execute("""
                    SELECT * FROM ingredient_catalog 
                    ORDER BY category, name
                """)
            
            ingredients = cursor.fetchall()
            return [self._ingredient_row_to_dict(ingredient) for ingredient in ingredients]
    
    def _row_to_recipe_dict(self, row) -> Dict:
        """Преобразование строки БД в словарь рецепта"""
        try:
            ingredients = json.loads(row[3]) if row[3] else {}
        except:
            ingredients = {"ингредиенты": row[3]} if row[3] else {}
        
        return {
            'id': row[0],
            'name': row[1],
            'base_spirit': row[2],
            'ingredients': ingredients,
            'method': row[3],
            'garnish': row[5],
            'glass_type': row[6],
            'description': row[7],
            'history': row[8],
            'season': row[9],
            'difficulty': row[10],
            'created_at': row[11],
            'updated_at': row[12]
        }
    
    def _custom_row_to_dict(self, row) -> Dict:
        """Преобразование строки пользовательского рецепта в словарь"""
        try:
            ingredients = json.loads(row[3]) if row[3] else {}
        except:
            ingredients = {"ингредиенты": row[3]} if row[3] else {}
        
        return {
            'id': row[0],
            'user_id': row[1],
            'name': row[2],
            'ingredients': ingredients,
            'method': row[4],
            'description': row[5],
            'glass_type': row[6],
            'garnish': row[7],
            'difficulty': row[8],
            'prep_time': row[9],
            'created_at': row[10],
            'updated_at': row[11]
        }
    
    def _collection_row_to_dict(self, row) -> Dict:
        """Преобразование строки подборки в словарь"""
        try:
            cocktail_ids = json.loads(row[4]) if row[4] else []
        except:
            cocktail_ids = []
        
        return {
            'id': row[0],
            'user_id': row[1],
            'name': row[2],
            'description': row[3],
            'cocktail_ids': cocktail_ids,
            'is_public': bool(row[5]),
            'created_at': row[6],
            'updated_at': row[7]
        }
    
    def _ingredient_row_to_dict(self, row) -> Dict:
        """Преобразование строки ингредиента в словарь"""
        try:
            substitutes = json.loads(row[5]) if row[5] else []
        except:
            substitutes = []
        
        return {
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'subcategory': row[3],
            'description': row[4],
            'substitutes': substitutes,
            'is_alcoholic': bool(row[6]),
            'alcohol_content': row[7],
            'created_at': row[8]
        }
