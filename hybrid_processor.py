#!/usr/bin/env python3
"""
Гибридная система обработки запросов для MixMatrixBot
Комбинирует локальную БД для рецептов и Yandex API для описаний
"""

import os
import re
import json
import requests
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from database import CocktailDatabase

# Загружаем переменные окружения
load_dotenv('env_file.txt')

class HybridCocktailProcessor:
    """Гибридный процессор запросов о коктейлях"""
    
    def __init__(self):
        self.db = CocktailDatabase()
        self.yandex_api_key = os.getenv('YANDEX_API_KEY')
        self.yandex_folder_id = os.getenv('FOLDER_ID')
        self.yandex_api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        
        # Ключевые слова для определения типа запроса
        self.alcohol_keywords = [
            'алкоголь', 'спирт', 'джин', 'водка', 'ром', 'виски', 'текила', 
            'коньяк', 'бренди', 'ликер', 'вермут', 'шампанское', 'вино',
            'коктейль', 'мартини', 'джин-тоник', 'мохито', 'космополитен',
            'кровавая мэри', 'пина колада', 'май тай', 'лонг айленд'
        ]
        
        self.educational_keywords = [
            'что такое', 'расскажи о', 'история', 'как делают', 'техника',
            'миксология', 'бармен', 'искусство', 'культура', 'традиция',
            'происхождение', 'этимология', 'значение', 'символика'
        ]
        
        self.non_alcohol_keywords = [
            'безалкогольный', 'моктейль', 'детский', 'без спирта',
            'лимонад', 'морс', 'компот', 'сок', 'вода'
        ]
    
    def analyze_request(self, user_message: str) -> Dict[str, any]:
        """Анализ пользовательского запроса"""
        message_lower = user_message.lower()
        
        analysis = {
            'is_alcohol_related': False,
            'is_educational': False,
            'is_recipe_request': False,
            'is_non_alcohol': False,
            'spirit_type': None,
            'cocktail_name': None,
            'confidence': 0.0
        }
        
        # Проверяем на алкогольные запросы
        alcohol_matches = sum(1 for keyword in self.alcohol_keywords if keyword in message_lower)
        if alcohol_matches > 0:
            analysis['is_alcohol_related'] = True
            analysis['confidence'] += alcohol_matches * 0.3
        
        # Проверяем на образовательные запросы
        educational_matches = sum(1 for keyword in self.educational_keywords if keyword in message_lower)
        if educational_matches > 0:
            analysis['is_educational'] = True
            analysis['confidence'] += educational_matches * 0.2
        
        # Проверяем на запросы рецептов
        recipe_patterns = [
            r'рецепт\s+(\w+)',
            r'как\s+сделать\s+(\w+)',
            r'приготовить\s+(\w+)',
            r'создать\s+(\w+)'
        ]
        
        for pattern in recipe_patterns:
            match = re.search(pattern, message_lower)
            if match:
                analysis['is_recipe_request'] = True
                analysis['cocktail_name'] = match.group(1)
                analysis['confidence'] += 0.4
                break
        
        # Проверяем на безалкогольные запросы
        non_alcohol_matches = sum(1 for keyword in self.non_alcohol_keywords if keyword in message_lower)
        if non_alcohol_matches > 0:
            analysis['is_non_alcohol'] = True
            analysis['confidence'] += non_alcohol_matches * 0.3
        
        # Определяем тип спирта
        for spirit in ['джин', 'водка', 'ром', 'виски', 'текила', 'коньяк', 'бренди']:
            if spirit in message_lower:
                analysis['spirit_type'] = spirit
                break
        
        return analysis
    
    async def call_yandex_api(self, prompt: str, system_prompt: str = "") -> str:
        """Вызов Yandex API для образовательного контента"""
        headers = {
            "Authorization": f"Api-Key {self.yandex_api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "text": system_prompt})
        messages.append({"role": "user", "text": prompt})
        
        data = {
            "modelUri": f"gpt://{self.yandex_folder_id}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 500
            },
            "messages": messages
        }
        
        try:
            response = requests.post(self.yandex_api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('result', {}).get('alternatives', [{}])[0].get('message', {}).get('text', 'Ошибка получения ответа')
            else:
                return f"Ошибка API: {response.status_code}"
                
        except Exception as e:
            return f"Ошибка при обращении к API: {e}"
    
    def search_cocktail_in_db(self, cocktail_name: str) -> Optional[Dict]:
        """Поиск коктейля в базе данных"""
        try:
            recipes = self.db.get_all_recipes()
            cocktail_name_lower = cocktail_name.lower()
            
            for recipe in recipes:
                if cocktail_name_lower in recipe['name'].lower():
                    return recipe
            
            # Поиск по частичному совпадению
            for recipe in recipes:
                if any(word in recipe['name'].lower() for word in cocktail_name_lower.split()):
                    return recipe
            
            return None
        except Exception as e:
            print(f"Ошибка поиска в БД: {e}")
            return None
    
    def format_cocktail_recipe(self, recipe: Dict) -> str:
        """Форматирование рецепта коктейля"""
        ingredients = json.loads(recipe['ingredients']) if isinstance(recipe['ingredients'], str) else recipe['ingredients']
        
        formatted_recipe = f"🍸 **{recipe['name']}**\n\n"
        
        if recipe.get('description'):
            formatted_recipe += f"📝 {recipe['description']}\n\n"
        
        formatted_recipe += "🥃 **Ингредиенты:**\n"
        for ingredient, amount in ingredients.items():
            formatted_recipe += f"• {ingredient}: {amount}\n"
        
        formatted_recipe += f"\n🔧 **Способ приготовления:**\n{recipe['method']}\n"
        
        if recipe.get('garnish'):
            formatted_recipe += f"\n🍒 **Гарнир:** {recipe['garnish']}\n"
        
        if recipe.get('glass_type'):
            formatted_recipe += f"\n🥛 **Посуда:** {recipe['glass_type']}\n"
        
        if recipe.get('history'):
            formatted_recipe += f"\n📚 **История:** {recipe['history']}\n"
        
        return formatted_recipe
    
    async def process_request(self, user_message: str) -> str:
        """Основной метод обработки запроса"""
        analysis = self.analyze_request(user_message)
        
        # Если запрос не связан с алкоголем или это безалкогольный запрос
        if analysis['is_non_alcohol'] or not analysis['is_alcohol_related']:
            if analysis['is_educational']:
                # Образовательный контент через API
                system_prompt = "Ты эксперт по напиткам и кулинарии. Рассказывай об истории, традициях и культуре напитков."
                response = await self.call_yandex_api(user_message, system_prompt)
                return f"📚 **Образовательный контент:**\n\n{response}"
            else:
                # Обычный запрос через API
                response = await self.call_yandex_api(user_message)
                return response
        
        # Если это запрос рецепта алкогольного коктейля
        if analysis['is_recipe_request'] and analysis['is_alcohol_related']:
            cocktail_name = analysis['cocktail_name']
            
            # Ищем в базе данных
            recipe = self.search_cocktail_in_db(cocktail_name)
            if recipe:
                return self.format_cocktail_recipe(recipe)
            else:
                # Если не найден в БД, используем API для описания
                system_prompt = "Ты эксперт-бармен. Расскажи об этом коктейле, его истории и особенностях, но не давай точный рецепт с алкоголем."
                response = await self.call_yandex_api(f"Расскажи о коктейле {cocktail_name}", system_prompt)
                return f"🍸 **Информация о коктейле {cocktail_name.title()}:**\n\n{response}\n\n💡 *Для точного рецепта обратитесь к профессиональному бармену*"
        
        # Если это образовательный запрос об алкоголе
        if analysis['is_educational'] and analysis['is_alcohol_related']:
            system_prompt = "Ты эксперт по истории и культуре напитков. Рассказывай об истории, традициях, производстве и культурном значении напитков."
            response = await self.call_yandex_api(user_message, system_prompt)
            return f"📚 **Образовательный контент:**\n\n{response}"
        
        # Если это общий запрос об алкоголе
        if analysis['is_alcohol_related']:
            system_prompt = "Ты эксперт по напиткам. Расскажи об этом напитке, его истории, особенностях и культурном значении."
            response = await self.call_yandex_api(user_message, system_prompt)
            return f"🍸 **Информация о напитке:**\n\n{response}"
        
        # По умолчанию используем API
        response = await self.call_yandex_api(user_message)
        return response

# Пример использования
async def test_hybrid_processor():
    """Тест гибридного процессора"""
    processor = HybridCocktailProcessor()
    
    test_requests = [
        "Расскажи рецепт мартини",
        "Что такое миксология?",
        "История джина",
        "Как приготовить лимонад?",
        "Расскажи о коктейле космополитен",
        "Что такое джин-тоник?"
    ]
    
    for request in test_requests:
        print(f"\n📝 Запрос: {request}")
        print("-" * 50)
        response = await processor.process_request(request)
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_hybrid_processor())












