#!/usr/bin/env python3
"""
MIXTRIX AI Module
AI-модуль для генерации рецептов коктейлей с использованием фудпейринга
и знаний из профессиональных книг барного ремесла
"""

import asyncio
import json
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import sqlite3
from yandex_ai_gateway import YandexAIService

@dataclass
class FlavorProfile:
    """Профиль вкуса для фудпейринга"""
    primary: str
    secondary: List[str]
    intensity: str  # light, medium, strong
    acidity: str    # low, medium, high
    sweetness: str  # dry, medium, sweet
    bitterness: str # none, light, medium, strong

class MIXTRIXAI:
    """AI-модуль MIXTRIX для генерации рецептов и фудпейринга"""
    
    def __init__(self, db_path: str = "mixtrix_professional.db"):
        self.db_path = db_path
        self.yandex_service = YandexAIService()
        self.flavor_pairing_rules = self._load_flavor_pairing_rules()
        self.seasonal_patterns = self._load_seasonal_patterns()
        self.technique_database = self._load_technique_database()
    
    def _load_flavor_pairing_rules(self) -> Dict:
        """Загрузка правил фудпейринга из Flavor Bible"""
        return {
            "complementary": {
                "citrus": {
                    "foods": ["seafood", "poultry", "herbs", "vegetables"],
                    "description": "Цитрусы дополняют морепродукты и птицу"
                },
                "herbal": {
                    "foods": ["vegetables", "cheese", "meat", "fish"],
                    "description": "Травы гармонируют с овощами и сырами"
                },
                "spicy": {
                    "foods": ["meat", "chocolate", "fruits", "nuts"],
                    "description": "Специи усиливают вкус мяса и шоколада"
                },
                "bitter": {
                    "foods": ["sweet", "fatty", "rich", "chocolate"],
                    "description": "Горькое уравновешивает сладкое и жирное"
                },
                "sweet": {
                    "foods": ["spicy", "bitter", "acidic", "salty"],
                    "description": "Сладкое смягчает острое и горькое"
                }
            },
            "contrasting": {
                "sweet_salty": {
                    "description": "Сладкое и соленое создают контраст"
                },
                "acidic_rich": {
                    "description": "Кислое освежает жирное"
                },
                "spicy_cooling": {
                    "description": "Острое и охлаждающее"
                }
            }
        }
    
    def _load_seasonal_patterns(self) -> Dict:
        """Загрузка сезонных паттернов для России"""
        return {
            "spring": {
                "ingredients": ["ревень", "щавель", "молодые травы", "цитрусы"],
                "flavors": ["fresh", "green", "tart", "herbal"],
                "spirits": ["джин", "водка", "белое вино"],
                "techniques": ["shake", "build", "muddle"]
            },
            "summer": {
                "ingredients": ["ягоды", "косточковые фрукты", "травы", "цитрусы"],
                "flavors": ["bright", "fruity", "refreshing", "tropical"],
                "spirits": ["ром", "джин", "текила", "водка"],
                "techniques": ["shake", "blend", "build"]
            },
            "autumn": {
                "ingredients": ["яблоки", "груши", "орехи", "специи"],
                "flavors": ["warm", "spiced", "nutty", "rich"],
                "spirits": ["виски", "коньяк", "ром темный"],
                "techniques": ["stir", "build", "hot"]
            },
            "winter": {
                "ingredients": ["цитрусы", "специи", "орехи", "ягоды"],
                "flavors": ["warming", "spiced", "rich", "comforting"],
                "spirits": ["виски", "коньяк", "ром темный", "водка"],
                "techniques": ["hot", "stir", "build"]
            }
        }
    
    def _load_technique_database(self) -> Dict:
        """Загрузка базы данных техник приготовления"""
        return {
            "shake": {
                "description": "Встряхивание в шейкере",
                "use_for": ["соки", "сиропы", "яйца", "сливки"],
                "time": "10-15 секунд",
                "ice": "крупный лед"
            },
            "stir": {
                "description": "Перемешивание в стакане для смешивания",
                "use_for": ["спиртные напитки", "вермуты", "биттеры"],
                "time": "30-45 секунд",
                "ice": "крупный лед"
            },
            "build": {
                "description": "Построение в стакане",
                "use_for": ["хайболы", "лонг-дринки", "горячие коктейли"],
                "time": "мгновенно",
                "ice": "по необходимости"
            },
            "muddle": {
                "description": "Разминание ингредиентов",
                "use_for": ["травы", "фрукты", "сахар"],
                "time": "5-10 секунд",
                "ice": "без льда"
            },
            "blend": {
                "description": "Смешивание в блендере",
                "use_for": ["фрукты", "лед", "сливки"],
                "time": "15-30 секунд",
                "ice": "дробленый лед"
            }
        }
    
    async def generate_cocktail_recipe(self, 
                                     base_spirit: str,
                                     flavor_profile: FlavorProfile,
                                     difficulty: str,
                                     season: str,
                                     food_pairing: Optional[str] = None,
                                     target_audience: str = "general") -> Dict:
        """Генерация AI-рецепта коктейля"""
        
        # Получаем сезонные рекомендации
        seasonal_data = self.seasonal_patterns.get(season, self.seasonal_patterns["spring"])
        
        # Генерируем базовый рецепт
        recipe = {
            "id": f"ai_gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "name": f"AI {base_spirit} {season.title()}",
            "name_en": f"AI {base_spirit} {season.title()}",
            "category": "ai_generated",
            "difficulty": difficulty,
            "base_spirit": base_spirit,
            "season": season,
            "target_audience": target_audience,
            "ingredients": {},
            "method": "",
            "glassware": "",
            "garnish": "",
            "description": "",
            "description_en": "",
            "history": "AI Generated Recipe",
            "flavor_profile": [flavor_profile.primary] + flavor_profile.secondary,
            "food_pairings": [food_pairing] if food_pairing else [],
            "seasonal_availability": [season],
            "prep_time": 0,
            "cost_estimate": 0.0,
            "profit_margin": 0.0,
            "iba_status": False,
            "source_book": "MIXTRIX AI",
            "author": "MIXTRIX AI",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "rating": 0.0,
            "popularity_score": 0
        }
        
        # Добавляем базовый спирт
        recipe["ingredients"][base_spirit] = {
            "amount": self._get_spirit_amount(base_spirit, difficulty),
            "unit": "ml",
            "technique": "base"
        }
        
        # Добавляем сезонные ингредиенты
        seasonal_ingredients = self._select_seasonal_ingredients(seasonal_data, flavor_profile)
        for ingredient in seasonal_ingredients:
            recipe["ingredients"][ingredient["name"]] = {
                "amount": ingredient["amount"],
                "unit": ingredient["unit"],
                "technique": ingredient["technique"]
            }
        
        # Определяем технику приготовления
        technique = self._select_technique(seasonal_data, recipe["ingredients"])
        recipe["method"] = self._generate_method(technique, recipe["ingredients"])
        
        # Определяем бокал
        recipe["glassware"] = self._select_glassware(technique, difficulty)
        
        # Генерируем гарнир
        recipe["garnish"] = self._generate_garnish(seasonal_data, flavor_profile)
        
        # Генерируем описание через AI
        recipe["description"] = await self._generate_description(recipe)
        recipe["description_en"] = await self._generate_description_en(recipe)
        
        # Добавляем фудпейринг
        if food_pairing:
            recipe["food_pairings"] = await self._suggest_food_pairings(recipe)
        
        # Рассчитываем время и стоимость
        recipe["prep_time"] = self._calculate_prep_time(technique, len(recipe["ingredients"]))
        recipe["cost_estimate"] = self._calculate_cost(recipe["ingredients"])
        recipe["profit_margin"] = self._calculate_profit_margin(difficulty)
        
        return recipe
    
    def _get_spirit_amount(self, spirit: str, difficulty: str) -> int:
        """Определение количества базового спирта"""
        amounts = {
            "beginner": 40,
            "intermediate": 50,
            "advanced": 60,
            "expert": 70
        }
        return amounts.get(difficulty, 50)
    
    def _select_seasonal_ingredients(self, seasonal_data: Dict, flavor_profile: FlavorProfile) -> List[Dict]:
        """Выбор сезонных ингредиентов"""
        ingredients = []
        
        # Добавляем цитрусовый сок
        if flavor_profile.acidity != "low":
            ingredients.append({
                "name": "сок лайма",
                "amount": 20,
                "unit": "ml",
                "technique": "shake"
            })
        
        # Добавляем сироп
        if flavor_profile.sweetness != "dry":
            ingredients.append({
                "name": "сахарный сироп",
                "amount": 15,
                "unit": "ml",
                "technique": "shake"
            })
        
        # Добавляем сезонный ингредиент
        seasonal_ingredient = random.choice(seasonal_data["ingredients"])
        ingredients.append({
            "name": seasonal_ingredient,
            "amount": 25,
            "unit": "ml",
            "technique": "seasonal"
        })
        
        return ingredients
    
    def _select_technique(self, seasonal_data: Dict, ingredients: Dict) -> str:
        """Выбор техники приготовления"""
        techniques = seasonal_data["techniques"]
        
        # Если есть соки или сиропы - встряхивание
        if any("сок" in ing or "сироп" in ing for ing in ingredients.keys()):
            return "shake"
        
        # Если только спиртные напитки - перемешивание
        if len(ingredients) <= 2:
            return "stir"
        
        # По умолчанию - построение
        return "build"
    
    def _generate_method(self, technique: str, ingredients: Dict) -> str:
        """Генерация метода приготовления"""
        technique_info = self.technique_database.get(technique, {})
        
        if technique == "shake":
            return f"Встряхнуть все ингредиенты со льдом в шейкере {technique_info.get('time', '10-15 секунд')}, процедить в охлажденный бокал"
        elif technique == "stir":
            return f"Перемешать все ингредиенты со льдом в стакане для смешивания {technique_info.get('time', '30-45 секунд')}, процедить в охлажденный бокал"
        elif technique == "build":
            return f"Наполнить стакан льдом, добавить ингредиенты в указанном порядке, аккуратно перемешать"
        else:
            return f"Приготовить коктейль методом {technique}"
    
    def _select_glassware(self, technique: str, difficulty: str) -> str:
        """Выбор бокала"""
        glassware_map = {
            "shake": "коктейльный бокал",
            "stir": "коктейльный бокал",
            "build": "хайбол",
            "muddle": "хайбол",
            "blend": "кубок для коктейля"
        }
        return glassware_map.get(technique, "коктейльный бокал")
    
    def _generate_garnish(self, seasonal_data: Dict, flavor_profile: FlavorProfile) -> str:
        """Генерация гарнира"""
        garnishes = []
        
        # Сезонные гарниры
        if "травы" in seasonal_data["ingredients"]:
            garnishes.append("листья мяты")
        
        if "цитрусы" in seasonal_data["ingredients"]:
            garnishes.append("долька лайма")
        
        # По умолчанию
        if not garnishes:
            garnishes = ["долька лимона", "вишня", "оливка"]
        
        return random.choice(garnishes)
    
    async def _generate_description(self, recipe: Dict) -> str:
        """Генерация описания через AI"""
        prompt = f"""
        Создай профессиональное описание коктейля:
        Название: {recipe['name']}
        База: {recipe['base_spirit']}
        Сезон: {recipe['season']}
        Сложность: {recipe['difficulty']}
        Вкусовой профиль: {', '.join(recipe['flavor_profile'])}
        
        Описание должно быть:
        - Профессиональным и привлекательным
        - Упоминать сезонность
        - Подходить для барной карты
        - 2-3 предложения
        """
        
        try:
            description = await self.yandex_service.generate_response(prompt)
            return description
        except Exception as e:
            return f"Сезонный коктейль с {recipe['base_spirit']} и {recipe['season']} ингредиентами."
    
    async def _generate_description_en(self, recipe: Dict) -> str:
        """Генерация описания на английском"""
        prompt = f"""
        Create professional description for cocktail:
        Name: {recipe['name_en']}
        Base: {recipe['base_spirit']}
        Season: {recipe['season']}
        Difficulty: {recipe['difficulty']}
        Flavor profile: {', '.join(recipe['flavor_profile'])}
        
        Description should be:
        - Professional and appealing
        - Mention seasonality
        - Suitable for bar menu
        - 2-3 sentences
        """
        
        try:
            description = await self.yandex_service.generate_response(prompt)
            return description
        except Exception as e:
            return f"Seasonal cocktail with {recipe['base_spirit']} and {recipe['season']} ingredients."
    
    async def _suggest_food_pairings(self, recipe: Dict) -> List[str]:
        """Предложения фудпейринга"""
        pairings = []
        
        # Анализируем вкусовой профиль
        for flavor in recipe["flavor_profile"]:
            if flavor in self.flavor_pairing_rules["complementary"]:
                rule = self.flavor_pairing_rules["complementary"][flavor]
                pairings.extend(rule["foods"])
        
        # Убираем дубликаты и возвращаем топ-3
        unique_pairings = list(set(pairings))
        return unique_pairings[:3]
    
    def _calculate_prep_time(self, technique: str, ingredient_count: int) -> int:
        """Расчет времени приготовления"""
        base_times = {
            "shake": 120,
            "stir": 90,
            "build": 60,
            "muddle": 150,
            "blend": 180
        }
        
        base_time = base_times.get(technique, 120)
        return base_time + (ingredient_count * 10)
    
    def _calculate_cost(self, ingredients: Dict) -> float:
        """Расчет стоимости коктейля"""
        # Упрощенный расчет
        base_cost = 50.0  # Базовая стоимость
        ingredient_cost = len(ingredients) * 15.0
        return base_cost + ingredient_cost
    
    def _calculate_profit_margin(self, difficulty: str) -> float:
        """Расчет маржи прибыли"""
        margins = {
            "beginner": 0.6,
            "intermediate": 0.7,
            "advanced": 0.8,
            "expert": 0.85
        }
        return margins.get(difficulty, 0.7)
    
    async def analyze_cocktail_compatibility(self, cocktail1: Dict, cocktail2: Dict) -> Dict:
        """Анализ совместимости коктейлей для меню"""
        compatibility_score = 0.0
        reasons = []
        
        # Проверяем вкусовые профили
        flavors1 = set(cocktail1.get("flavor_profile", []))
        flavors2 = set(cocktail2.get("flavor_profile", []))
        
        if flavors1.intersection(flavors2):
            compatibility_score += 0.3
            reasons.append("Схожие вкусовые профили")
        
        # Проверяем сезонность
        seasons1 = set(cocktail1.get("seasonal_availability", []))
        seasons2 = set(cocktail2.get("seasonal_availability", []))
        
        if seasons1.intersection(seasons2):
            compatibility_score += 0.2
            reasons.append("Совпадающая сезонность")
        
        # Проверяем сложность
        if cocktail1.get("difficulty") == cocktail2.get("difficulty"):
            compatibility_score += 0.2
            reasons.append("Одинаковая сложность")
        
        # Проверяем базовые спирты
        if cocktail1.get("base_spirit") != cocktail2.get("base_spirit"):
            compatibility_score += 0.3
            reasons.append("Разные базовые спирты")
        
        return {
            "score": compatibility_score,
            "reasons": reasons,
            "recommendation": "Рекомендуется" if compatibility_score > 0.6 else "Не рекомендуется"
        }

# Тестирование AI модуля
async def test_mixtrix_ai():
    """Тестирование MIXTRIX AI"""
    ai = MIXTRIXAI()
    
    print("🤖 Тестирование MIXTRIX AI...")
    print("=" * 50)
    
    # Тест генерации рецепта
    flavor_profile = FlavorProfile(
        primary="citrus",
        secondary=["herbal", "fresh"],
        intensity="medium",
        acidity="high",
        sweetness="medium",
        bitterness="light"
    )
    
    recipe = await ai.generate_cocktail_recipe(
        base_spirit="джин лондонский",
        flavor_profile=flavor_profile,
        difficulty="intermediate",
        season="spring",
        food_pairing="устрицы",
        target_audience="молодые профессионалы"
    )
    
    print("🍸 Сгенерированный рецепт:")
    print(f"Название: {recipe['name']}")
    print(f"База: {recipe['base_spirit']}")
    print(f"Сезон: {recipe['season']}")
    print(f"Ингредиенты: {len(recipe['ingredients'])}")
    print(f"Метод: {recipe['method'][:50]}...")
    print(f"Описание: {recipe['description'][:100]}...")
    print(f"Фудпейринг: {recipe['food_pairings']}")
    
    print("\n✅ MIXTRIX AI работает!")

if __name__ == "__main__":
    asyncio.run(test_mixtrix_ai())












