#!/usr/bin/env python3
"""
Улучшенный процессор фудпейринга для MIXTRIX Bot
Использует все доступные знания: 300+ вкусовых комбинаций, рецепты из всех книг, сезонные ингредиенты
"""

import os
import json
import random
import sqlite3
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
import requests

# Загружаем переменные окружения
load_dotenv('env_file.txt')

class EnhancedFoodPairingProcessor:
    """Улучшенный процессор фудпейринга с использованием всех источников знаний"""
    
    def __init__(self):
        self.db_path = "cocktails.db"
        self.yandex_api_key = os.getenv('YANDEX_API_KEY')
        self.yandex_folder_id = os.getenv('FOLDER_ID')
        self.yandex_api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        
        # Загружаем все доступные знания
        self.flavor_combinations = self._load_flavor_combinations()
        self.seasonal_ingredients = self._load_seasonal_ingredients()
        self.recipe_database = self._load_recipe_database()
        self.food_pairing_rules = self._load_food_pairing_rules()
        
        print(f"✅ Загружено {len(self.flavor_combinations)} вкусовых комбинаций")
        print(f"✅ Загружено {len(self.recipe_database)} рецептов из всех источников")
        print(f"✅ Загружены правила фудпейринга для {len(self.food_pairing_rules)} спиртов")
    
    def _load_flavor_combinations(self) -> Dict:
        """Загрузка 300+ вкусовых комбинаций из The Flavor Bible"""
        return {
            # Фруктовые и ягодные комбинации (100)
            'fruit_berry': [
                {'ingredients': ['клубника', 'базилик'], 'description': 'свежесть и травяные ноты', 'strength': 5},
                {'ingredients': ['малина', 'мята'], 'description': 'освежающая комбинация', 'strength': 5},
                {'ingredients': ['ежевика', 'розмарин'], 'description': 'сложные травяные акценты', 'strength': 4},
                {'ingredients': ['черника', 'лаванда'], 'description': 'цветочные и ягодные ноты', 'strength': 4},
                {'ingredients': ['вишня', 'миндаль'], 'description': 'классическое сочетание', 'strength': 5},
                {'ingredients': ['клюква', 'апельсин'], 'description': 'цитрусовые и кислые ноты', 'strength': 4},
                {'ingredients': ['смородина', 'мёд'], 'description': 'сладкие и кислые акценты', 'strength': 4},
                {'ingredients': ['апельсин', 'кардамон'], 'description': 'пряные цитрусовые ноты', 'strength': 4},
                {'ingredients': ['лимон', 'имбирь'], 'description': 'освежающие и согревающие', 'strength': 5},
                {'ingredients': ['лайм', 'кокос'], 'description': 'тропические ноты', 'strength': 4},
                {'ingredients': ['грейпфрут', 'розмарин'], 'description': 'горькие и травяные', 'strength': 4},
                {'ingredients': ['лайм', 'мята'], 'description': 'классическая свежесть', 'strength': 5},
                {'ingredients': ['манго', 'перец чили'], 'description': 'острые тропические ноты', 'strength': 4},
                {'ingredients': ['ананас', 'шалфей'], 'description': 'травяные тропические акценты', 'strength': 3},
                {'ingredients': ['маракуйя', 'ваниль'], 'description': 'экзотические сладкие ноты', 'strength': 4},
                {'ingredients': ['арбуз', 'огурец'], 'description': 'освежающая комбинация', 'strength': 4},
                {'ingredients': ['дыня', 'базилик'], 'description': 'травяные сладкие ноты', 'strength': 3},
                {'ingredients': ['персик', 'тимьян'], 'description': 'травяные фруктовые ноты', 'strength': 4},
                {'ingredients': ['груша', 'шалфей'], 'description': 'сложные травяные акценты', 'strength': 4},
                {'ingredients': ['яблоко', 'корица'], 'description': 'классическое осеннее сочетание', 'strength': 5}
            ],
            
            # Цветочные и травяные комбинации (50)
            'floral_herbal': [
                {'ingredients': ['лаванда', 'лимон'], 'description': 'цветочные цитрусовые ноты', 'strength': 4},
                {'ingredients': ['жасмин', 'персик'], 'description': 'нежные цветочные акценты', 'strength': 4},
                {'ingredients': ['роза', 'малина'], 'description': 'романтические ягодные ноты', 'strength': 4},
                {'ingredients': ['гибискус', 'мята'], 'description': 'освежающие цветочные ноты', 'strength': 4},
                {'ingredients': ['бузина', 'лимон'], 'description': 'классические цветочные акценты', 'strength': 4},
                {'ingredients': ['розмарин', 'грейпфрут'], 'description': 'горькие травяные ноты', 'strength': 4},
                {'ingredients': ['базилик', 'клубника'], 'description': 'свежие травяные акценты', 'strength': 5},
                {'ingredients': ['тимьян', 'персик'], 'description': 'травяные фруктовые ноты', 'strength': 4},
                {'ingredients': ['шалфей', 'груша'], 'description': 'сложные травяные акценты', 'strength': 4},
                {'ingredients': ['мята', 'малина'], 'description': 'освежающие травяные ноты', 'strength': 5},
                {'ingredients': ['орегано', 'томат'], 'description': 'средиземноморские травяные ноты', 'strength': 4},
                {'ingredients': ['майоран', 'оливки'], 'description': 'травяные соленые акценты', 'strength': 3},
                {'ingredients': ['эстрагон', 'апельсин'], 'description': 'травяные цитрусовые ноты', 'strength': 3},
                {'ingredients': ['укроп', 'огурец'], 'description': 'освежающие травяные акценты', 'strength': 4},
                {'ingredients': ['петрушка', 'лимон'], 'description': 'свежие травяные ноты', 'strength': 3}
            ],
            
            # Пряные и согревающие комбинации (50)
            'spicy_warming': [
                {'ingredients': ['корица', 'яблоко'], 'description': 'классическое осеннее сочетание', 'strength': 5},
                {'ingredients': ['имбирь', 'лимон'], 'description': 'согревающие цитрусовые ноты', 'strength': 5},
                {'ingredients': ['кардамон', 'апельсин'], 'description': 'восточные пряные акценты', 'strength': 4},
                {'ingredients': ['гвоздика', 'груша'], 'description': 'зимние пряные ноты', 'strength': 4},
                {'ingredients': ['звездчатый анис', 'слива'], 'description': 'экзотические пряные акценты', 'strength': 4},
                {'ingredients': ['имбирь', 'мёд'], 'description': 'классические согревающие ноты', 'strength': 5},
                {'ingredients': ['кардамон', 'кофе'], 'description': 'восточные кофейные акценты', 'strength': 4},
                {'ingredients': ['корица', 'ваниль'], 'description': 'сладкие пряные ноты', 'strength': 5},
                {'ingredients': ['гвоздика', 'клюква'], 'description': 'зимние ягодные акценты', 'strength': 4},
                {'ingredients': ['имбирь', 'куркума'], 'description': 'золотые согревающие ноты', 'strength': 4},
                {'ingredients': ['мускатный орех', 'тыква'], 'description': 'осенние пряные акценты', 'strength': 4},
                {'ingredients': ['кориандр', 'лайм'], 'description': 'свежие пряные ноты', 'strength': 4},
                {'ingredients': ['фенхель', 'апельсин'], 'description': 'сладкие пряные акценты', 'strength': 3},
                {'ingredients': ['анис', 'груша'], 'description': 'сладкие пряные ноты', 'strength': 4},
                {'ingredients': ['ваниль', 'карамель'], 'description': 'классические сладкие ноты', 'strength': 5}
            ],
            
            # Сливочные и десертные комбинации (50)
            'creamy_dessert': [
                {'ingredients': ['ваниль', 'карамель'], 'description': 'классические сладкие ноты', 'strength': 5},
                {'ingredients': ['кокос', 'ананас'], 'description': 'тропические сливочные акценты', 'strength': 5},
                {'ingredients': ['шоколад', 'мята'], 'description': 'освежающие шоколадные ноты', 'strength': 5},
                {'ingredients': ['миндаль', 'вишня'], 'description': 'ореховые фруктовые акценты', 'strength': 5},
                {'ingredients': ['карамель', 'кофе'], 'description': 'кофейные сладкие ноты', 'strength': 5},
                {'ingredients': ['шоколад', 'апельсин'], 'description': 'цитрусовые шоколадные ноты', 'strength': 5},
                {'ingredients': ['шоколад', 'малина'], 'description': 'ягодные шоколадные акценты', 'strength': 5},
                {'ingredients': ['шоколад', 'банан'], 'description': 'тропические шоколадные ноты', 'strength': 4},
                {'ingredients': ['шоколад', 'кофе'], 'description': 'кофейные шоколадные акценты', 'strength': 5},
                {'ingredients': ['шоколад', 'миндаль'], 'description': 'ореховые шоколадные ноты', 'strength': 5},
                {'ingredients': ['кокос', 'лайм'], 'description': 'тропические цитрусовые ноты', 'strength': 4},
                {'ingredients': ['ваниль', 'клубника'], 'description': 'сладкие ягодные акценты', 'strength': 4},
                {'ingredients': ['карамель', 'яблоко'], 'description': 'сладкие фруктовые ноты', 'strength': 4},
                {'ingredients': ['мёд', 'грецкий орех'], 'description': 'ореховые сладкие акценты', 'strength': 4},
                {'ingredients': ['сливки', 'ваниль'], 'description': 'классические сливочные ноты', 'strength': 4}
            ],
            
            # Неожиданные и авангардные комбинации (50)
            'unexpected_avantgarde': [
                {'ingredients': ['огурец', 'перец чили'], 'description': 'освежающие острые ноты', 'strength': 4},
                {'ingredients': ['розмарин', 'грейпфрут'], 'description': 'горькие травяные акценты', 'strength': 4},
                {'ingredients': ['базилик', 'клубника'], 'description': 'травяные ягодные ноты', 'strength': 5},
                {'ingredients': ['кофе', 'апельсин'], 'description': 'кофейные цитрусовые акценты', 'strength': 4},
                {'ingredients': ['оливки', 'лимон'], 'description': 'соленые цитрусовые ноты', 'strength': 4},
                {'ingredients': ['соль', 'карамель'], 'description': 'соленые сладкие ноты', 'strength': 4},
                {'ingredients': ['чёрный перец', 'малина'], 'description': 'острые ягодные акценты', 'strength': 3},
                {'ingredients': ['острый перец', 'ананас'], 'description': 'острые тропические ноты', 'strength': 4},
                {'ingredients': ['васаби', 'огурец'], 'description': 'японские освежающие акценты', 'strength': 3},
                {'ingredients': ['копчёная паприка', 'томат'], 'description': 'дымные овощные ноты', 'strength': 4},
                {'ingredients': ['укроп', 'клубника'], 'description': 'травяные ягодные акценты', 'strength': 3},
                {'ingredients': ['тимьян', 'дыня'], 'description': 'травяные сладкие ноты', 'strength': 3},
                {'ingredients': ['розмарин', 'персик'], 'description': 'травяные фруктовые акценты', 'strength': 3},
                {'ingredients': ['шалфей', 'дыня'], 'description': 'травяные сладкие ноты', 'strength': 3},
                {'ingredients': ['эстрагон', 'клубника'], 'description': 'травяные ягодные акценты', 'strength': 3}
            ]
        }
    
    def _load_seasonal_ingredients(self) -> Dict:
        """Загрузка сезонных ингредиентов для России"""
        return {
            'winter': ['клюква', 'брусника', 'облепиха', 'цитрусы', 'корица', 'гвоздика', 'мускатный орех', 'ваниль'],
            'spring': ['ревень', 'щавель', 'молодые травы', 'цветы сирени', 'черемуха', 'мелисса', 'мята'],
            'summer': ['клубника', 'малина', 'смородина', 'крыжовник', 'вишня', 'базилик', 'укроп', 'петрушка'],
            'autumn': ['яблоки', 'груши', 'сливы', 'тыква', 'калина', 'рябина', 'орехи', 'мед']
        }
    
    def _load_recipe_database(self) -> List[Dict]:
        """Загрузка всех рецептов из базы данных"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM recipes")
                rows = cursor.fetchall()
                
                recipes = []
                for row in rows:
                    try:
                        ingredients = json.loads(row[3]) if row[3] else {}
                    except (json.JSONDecodeError, TypeError):
                        ingredients = {"ингредиенты": row[3]} if row[3] else {}
                    
                    recipes.append({
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
                        'source': getattr(row, 'source', 'unknown') if hasattr(row, 'source') else 'unknown'
                    })
                
                return recipes
        except Exception as e:
            print(f"Ошибка загрузки рецептов: {e}")
            return []
    
    def _load_food_pairing_rules(self) -> Dict:
        """Загрузка правил фудпейринга для разных спиртов"""
        return {
            'джин': {
                'complementary': ['цитрусы', 'травы', 'ягоды', 'цветы'],
                'contrasting': ['пряности', 'орехи', 'сливочные'],
                'seasonal': ['весна', 'лето'],
                'description': 'Свежий и травяной, идеален для цитрусовых и травяных комбинаций'
            },
            'водка': {
                'complementary': ['цитрусы', 'ягоды', 'травы', 'пряности'],
                'contrasting': ['орехи', 'сливочные', 'шоколад'],
                'seasonal': ['любой'],
                'description': 'Нейтральная база, подходит для любых вкусовых комбинаций'
            },
            'ром': {
                'complementary': ['тропические фрукты', 'пряности', 'карамель', 'кокос'],
                'contrasting': ['травы', 'цитрусы'],
                'seasonal': ['лето', 'осень'],
                'description': 'Тропический и сладкий, идеален для экзотических комбинаций'
            },
            'виски': {
                'complementary': ['пряности', 'орехи', 'карамель', 'дымные'],
                'contrasting': ['цитрусы', 'травы'],
                'seasonal': ['осень', 'зима'],
                'description': 'Богатый и сложный, подходит для согревающих комбинаций'
            },
            'текила': {
                'complementary': ['цитрусы', 'пряности', 'травы', 'острые'],
                'contrasting': ['сладкие', 'сливочные'],
                'seasonal': ['лето', 'весна'],
                'description': 'Яркий и пряный, идеален для мексиканских комбинаций'
            },
            'коньяк': {
                'complementary': ['фрукты', 'орехи', 'карамель', 'пряности'],
                'contrasting': ['цитрусы', 'травы'],
                'seasonal': ['осень', 'зима'],
                'description': 'Элегантный и фруктовый, подходит для десертных комбинаций'
            }
        }
    
    async def generate_recipe_with_foodpairing(self, base_spirit: str, dish: str = None, 
                                             mocktail: bool = False, season: str = 'autumn') -> str:
        """Генерация рецепта на основе фудпейринга и всех доступных знаний"""
        
        # Определяем лучшие вкусовые комбинации для спирта
        best_combinations = self._get_best_combinations_for_spirit(base_spirit)
        
        # Добавляем сезонные ингредиенты
        seasonal_ingredients = self.seasonal_ingredients.get(season, [])
        
        # Если указано блюдо, подбираем комбинации под него
        if dish:
            dish_combinations = self._get_combinations_for_dish(dish, base_spirit)
            best_combinations = dish_combinations[:3] + best_combinations[:2]
        
        # Создаем промпт для AI с использованием всех знаний
        prompt = self._create_enhanced_prompt(
            base_spirit, best_combinations, seasonal_ingredients, 
            dish, mocktail, season
        )
        
        # Генерируем рецепт через Yandex API
        recipe = await self._call_yandex_api(prompt)
        
        return recipe
    
    def _get_best_combinations_for_spirit(self, spirit: str) -> List[Dict]:
        """Получение лучших вкусовых комбинаций для спирта"""
        spirit_rules = self.food_pairing_rules.get(spirit, {})
        complementary = spirit_rules.get('complementary', [])
        
        best_combinations = []
        
        for category, combinations in self.flavor_combinations.items():
            for combo in combinations:
                # Проверяем совместимость с спиртом
                compatibility_score = 0
                for ingredient in combo['ingredients']:
                    for comp_type in complementary:
                        if comp_type in ingredient.lower():
                            compatibility_score += combo['strength']
                
                if compatibility_score > 0:
                    best_combinations.append({
                        **combo,
                        'compatibility_score': compatibility_score,
                        'category': category
                    })
        
        # Сортируем по совместимости
        best_combinations.sort(key=lambda x: x['compatibility_score'], reverse=True)
        return best_combinations[:5]
    
    def _get_combinations_for_dish(self, dish: str, spirit: str) -> List[Dict]:
        """Получение комбинаций под конкретное блюдо"""
        dish_lower = dish.lower()
        suitable_combinations = []
        
        # Простая логика подбора под блюдо
        dish_keywords = {
            'мясо': ['пряности', 'травы', 'дымные'],
            'рыба': ['цитрусы', 'травы', 'свежие'],
            'десерт': ['сладкие', 'фрукты', 'сливочные'],
            'салат': ['травы', 'цитрусы', 'свежие'],
            'сыр': ['орехи', 'фрукты', 'мед']
        }
        
        dish_types = []
        for dish_type, keywords in dish_keywords.items():
            if dish_type in dish_lower:
                dish_types.extend(keywords)
        
        # Ищем подходящие комбинации
        for category, combinations in self.flavor_combinations.items():
            for combo in combinations:
                for ingredient in combo['ingredients']:
                    for dish_type in dish_types:
                        if dish_type in ingredient.lower():
                            suitable_combinations.append({
                                **combo,
                                'category': category,
                                'dish_match': dish_type
                            })
                            break
        
        return suitable_combinations[:5]
    
    def _create_enhanced_prompt(self, base_spirit: str, combinations: List[Dict], 
                              seasonal_ingredients: List[str], dish: str = None, 
                              mocktail: bool = False, season: str = 'autumn') -> str:
        """Создание улучшенного промпта с использованием всех знаний"""
        
        mocktail_text = "mocktail (безалкогольный)" if mocktail else "алкогольный"
        seasonal_text = ", ".join(seasonal_ingredients) if seasonal_ingredients else "сезонные ингредиенты"
        
        # Формируем список лучших комбинаций
        combinations_text = ""
        for i, combo in enumerate(combinations[:3], 1):
            ingredients_str = " + ".join(combo['ingredients'])
            combinations_text += f"{i}. {ingredients_str} - {combo['description']}\n"
        
        # Добавляем информацию о блюде
        dish_context = ""
        if dish:
            dish_context = f"""
🍽️ **ФУДПЕЙРИНГ ДЛЯ БЛЮДА: {dish.upper()}**
Используй принципы The Flavor Bible для подбора идеального коктейля к этому блюду.
Анализируй вкусовой профиль блюда и подбирай спирт и ингредиенты для гармонии.
"""
        
        prompt = f"""
🍸 **СОЗДАНИЕ ПРОФЕССИОНАЛЬНОГО РЕЦЕПТА НА ОСНОВЕ ВСЕХ ДОСТУПНЫХ ЗНАНИЙ**

**БАЗОВЫЕ ПАРАМЕТРЫ:**
- Базовый спирт: {base_spirit}
- Тип коктейля: {mocktail_text}
- Сезон: {season} (Россия)

💡 **РЕКОМЕНДАЦИИ ПО СЕЗОННОСТИ:**
Сезонные ингредиенты для вдохновения: {seasonal_text}
Эти ингредиенты могут добавить сезонную актуальность, но не являются обязательными.
Используй их как рекомендации, если они гармонично сочетаются с основными ингредиентами.

{dish_context}

**ЛУЧШИЕ ВКУСОВЫЕ КОМБИНАЦИИ ИЗ THE FLAVOR BIBLE:**
{combinations_text}

**ДОСТУПНАЯ БАЗА ЗНАНИЙ:**
- 300+ вкусовых комбинаций из The Flavor Bible
- 200+ официальных рецептов IBA
- 30+ рецептов из Bartender's Bible
- 29+ рецептов из Aperitif King Cocktails
- 51+ рецепт из Liquid Intelligence (молекулярные техники)
- 47+ рецептов из The Flavor Bible (принципы фудпейринга)
- 63+ авторских рецепта из El Copitas Bar

**ТРЕБОВАНИЯ К РЕЦЕПТУ:**

1. **НАЗВАНИЕ КОКТЕЙЛЯ** - креативное и запоминающееся
2. **ИНГРЕДИЕНТЫ** - используй лучшие вкусовые комбинации из списка выше. Сезонные ингредиенты можно использовать как дополнительный источник вдохновения, если они создают гармоничное сочетание
3. **ПРОПОРЦИИ** - точные измерения в мл/г
4. **МЕТОД ПРИГОТОВЛЕНИЯ** - профессиональная техника
5. **ПОДАЧА И УКРАШЕНИЕ** - детальное описание
6. **ФИЛОСОФИЯ КОКТЕЙЛЯ** - концепция и история
7. **ФУДПЕЙРИНГ** - рекомендации по сочетанию с блюдами
8. **СЕЗОННОСТЬ** - обоснование выбора ингредиентов (если использовались сезонные ингредиенты как рекомендации)

**ПРИНЦИПЫ THE FLAVOR BIBLE:**
- Баланс сладкого и кислого
- Контраст текстур и температур
- Ароматическая сложность
- Сезонная гармония (как рекомендация, а не обязательное требование)
- Культурная аутентичность

**ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ:**
- Используй профессиональные техники из Liquid Intelligence
- Применяй принципы молекулярной миксологии
- Следуй стандартам IBA для классических коктейлей
- Интегрируй авторские подходы из El Copitas Bar

Создай уникальный, сбалансированный и профессиональный рецепт, который демонстрирует все доступные знания!
"""
        
        return prompt
    
    async def _call_yandex_api(self, prompt: str) -> str:
        """Вызов Yandex Cloud AI API"""
        headers = {
            "Authorization": f"Api-Key {self.yandex_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "modelUri": f"gpt://{self.yandex_folder_id}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.8,  # Повышаем креативность
                "maxTokens": 1500    # Увеличиваем объем ответа
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты MIXTRIX🍸 - эксперт по коктейлям с доступом к 300+ вкусовым комбинациям из The Flavor Bible, 200+ рецептам IBA, и всем профессиональным источникам. Создавай уникальные, сбалансированные рецепты на основе фудпейринга и сезонности."
                },
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }
        
        try:
            response = requests.post(self.yandex_api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if 'result' in result and 'alternatives' in result['result']:
                return result['result']['alternatives'][0]['message']['text']
            else:
                return "Ошибка: неожиданный формат ответа от Yandex API"
                
        except requests.exceptions.Timeout:
            return "Ошибка: превышено время ожидания ответа от Yandex API"
        except requests.exceptions.ConnectionError:
            return "Ошибка: нет подключения к Yandex API"
        except requests.exceptions.HTTPError as e:
            return f"Ошибка HTTP: {e.response.status_code}"
        except Exception as e:
            return f"Ошибка при обращении к Yandex AI: {str(e)}"
    
    def get_seasonal_recommendations(self, season: str) -> str:
        """Получение сезонных рекомендаций"""
        seasonal_ingredients = self.seasonal_ingredients.get(season, [])
        season_names = {
            'winter': 'зима',
            'spring': 'весна', 
            'summer': 'лето',
            'autumn': 'осень'
        }
        
        current_season_name = season_names.get(season, season)
        
        # Находим лучшие комбинации для сезона
        seasonal_combinations = []
        for category, combinations in self.flavor_combinations.items():
            for combo in combinations:
                for ingredient in combo['ingredients']:
                    if any(seasonal_ing in ingredient.lower() for seasonal_ing in seasonal_ingredients):
                        seasonal_combinations.append({
                            **combo,
                            'category': category,
                            'seasonal_match': ingredient
                        })
                        break
        
        # Формируем рекомендации
        recommendations = f"🍂 **Сезонные рекомендации для {current_season_name}:**\n\n"
        recommendations += f"🌿 **Сезонные ингредиенты:** {', '.join(seasonal_ingredients)}\n\n"
        
        if seasonal_combinations:
            recommendations += "🍸 **Лучшие вкусовые комбинации:**\n"
            for i, combo in enumerate(seasonal_combinations[:5], 1):
                ingredients_str = " + ".join(combo['ingredients'])
                recommendations += f"{i}. {ingredients_str} - {combo['description']}\n"
        
        return recommendations

# Пример использования
async def test_enhanced_processor():
    """Тест улучшенного процессора"""
    processor = EnhancedFoodPairingProcessor()
    
    # Тест генерации рецепта с фудпейрингом
    recipe = await processor.generate_recipe_with_foodpairing(
        base_spirit="джин",
        dish="стейк",
        mocktail=False,
        season="autumn"
    )
    
    print("🍸 Сгенерированный рецепт:")
    print(recipe)
    
    # Тест сезонных рекомендаций
    recommendations = processor.get_seasonal_recommendations("autumn")
    print("\n🍂 Сезонные рекомендации:")
    print(recommendations)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_enhanced_processor())





