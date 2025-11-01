#!/usr/bin/env python3
"""
Расширенный процессор для функций приложения "Коктейльная вечеринка"
"""

import re
import json
from typing import Dict, List, Optional
from cocktail_party_db import CocktailPartyDatabase
from yandex_ai_gateway import YandexAIService

class CocktailPartyProcessor:
    """Процессор для функций MIXTRIX"""
    
    def __init__(self):
        self.db = CocktailPartyDatabase()
        self.yandex_service = YandexAIService()
    
    async def process_request(self, user_message: str, user_id: int = 1) -> str:
        """Обработка запроса пользователя"""
        
        # Определяем тип запроса
        request_type = self._identify_request_type(user_message)
        
        if request_type == "add_ingredient":
            return await self._handle_add_ingredient(user_message, user_id)
        elif request_type == "show_my_bar":
            return await self._handle_show_bar(user_id)
        elif request_type == "find_cocktails":
            return await self._handle_find_cocktails(user_id)
        elif request_type == "rate_cocktail":
            return await self._handle_rate_cocktail(user_message, user_id)
        elif request_type == "add_favorite":
            return await self._handle_add_favorite(user_message, user_id)
        elif request_type == "show_favorites":
            return await self._handle_show_favorites(user_id)
        elif request_type == "create_recipe":
            return await self._handle_create_recipe(user_message, user_id)
        elif request_type == "show_custom_recipes":
            return await self._handle_show_custom_recipes(user_id)
        elif request_type == "create_collection":
            return await self._handle_create_collection(user_message, user_id)
        elif request_type == "show_collections":
            return await self._handle_show_collections(user_id)
        elif request_type == "advanced_search":
            return await self._handle_advanced_search(user_message)
        elif request_type == "show_catalog":
            return await self._handle_show_catalog(user_message)
        elif request_type == "help":
            return await self._handle_help()
        else:
            # Обычный поиск коктейля
            return await self._handle_cocktail_search(user_message)
    
    def _identify_request_type(self, message: str) -> str:
        """Определение типа запроса"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["добавь", "есть", "купил", "приобрёл"]):
            return "add_ingredient"
        elif any(word in message_lower for word in ["мой бар", "что есть", "ингредиенты"]):
            return "show_my_bar"
        elif any(word in message_lower for word in ["что приготовить", "можно сделать", "доступные"]):
            return "find_cocktails"
        elif any(word in message_lower for word in ["оцени", "рейтинг", "звезд"]):
            return "rate_cocktail"
        elif any(word in message_lower for word in ["избранное", "сохрани", "понравился"]):
            return "add_favorite"
        elif any(word in message_lower for word in ["мои избранные", "любимые"]):
            return "show_favorites"
        elif any(word in message_lower for word in ["создай рецепт", "мой рецепт", "добавь рецепт"]):
            return "create_recipe"
        elif any(word in message_lower for word in ["мои рецепты", "созданные"]):
            return "show_custom_recipes"
        elif any(word in message_lower for word in ["подборка", "коллекция", "создай подборку"]):
            return "create_collection"
        elif any(word in message_lower for word in ["мои подборки", "коллекции"]):
            return "show_collections"
        elif any(word in message_lower for word in ["поиск", "фильтр", "найди по"]):
            return "advanced_search"
        elif any(word in message_lower for word in ["каталог", "ингредиенты", "список"]):
            return "show_catalog"
        elif any(word in message_lower for word in ["помощь", "команды", "что умеешь"]):
            return "help"
        else:
            return "cocktail_search"
    
    async def _handle_add_ingredient(self, message: str, user_id: int) -> str:
        """Добавление ингредиента в бар"""
        # Извлекаем название ингредиента
        ingredient_match = re.search(r'(?:добавь|есть|купил|приобрёл)\s+(.+)', message.lower())
        if not ingredient_match:
            return "❌ Не удалось определить название ингредиента. Попробуйте: 'Добавь водку' или 'Есть джин'"
        
        ingredient_name = ingredient_match.group(1).strip()
        
        # Определяем категорию
        category = self._determine_ingredient_category(ingredient_name)
        
        # Добавляем в базу
        success = self.db.add_user_ingredient(user_id, ingredient_name, category)
        
        if success:
            return f"✅ Добавлен ингредиент: *{ingredient_name.title()}*\n📂 Категория: {category}\n\nТеперь вы можете найти коктейли, которые можно приготовить из ваших ингредиентов!"
        else:
            return "❌ Ошибка добавления ингредиента"
    
    async def _handle_show_bar(self, user_id: int) -> str:
        """Показ ингредиентов в баре пользователя"""
        ingredients = self.db.get_user_ingredients(user_id)
        
        if not ingredients:
            return "🍹 *Ваш бар пуст*\n\nДобавьте ингредиенты командой:\n• 'Добавь водку'\n• 'Есть джин'\n• 'Купил текилу'"
        
        # Группируем по категориям
        categories = {}
        for ing in ingredients:
            cat = ing['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ing)
        
        response = "🍹 *Ваш бар:*\n\n"
        
        for category, items in categories.items():
            response += f"📂 *{category.replace('_', ' ').title()}:*\n"
            for item in items:
                amount_info = f" ({item['amount']} {item['unit']})" if item['amount'] else ""
                response += f"• {item['name'].title()}{amount_info}\n"
            response += "\n"
        
        response += "💡 *Команды:*\n• 'Что приготовить?' - найти доступные коктейли\n• 'Добавь [ингредиент]' - добавить новый ингредиент"
        
        return response
    
    async def _handle_find_cocktails(self, user_id: int) -> str:
        """Поиск коктейлей по имеющимся ингредиентам"""
        cocktails = self.db.find_cocktails_by_ingredients(user_id)
        
        if not cocktails:
            return "❌ *Не найдено коктейлей*\n\nДобавьте ингредиенты в ваш бар командой 'Добавь [ингредиент]'"
        
        # Показываем топ-5 наиболее доступных
        top_cocktails = cocktails[:5]
        
        response = "🍹 *Коктейли из ваших ингредиентов:*\n\n"
        
        for cocktail in top_cocktails:
            availability = cocktail['availability_percentage']
            missing = cocktail['missing_ingredients']
            
            response += f"🥃 *{cocktail['name']}*\n"
            response += f"📊 Доступность: {availability:.0f}%\n"
            
            if missing:
                response += f"❌ Нужно: {', '.join(missing[:3])}\n"
            
            if cocktail.get('description'):
                response += f"📝 {cocktail['description'][:100]}...\n"
            
            response += "\n"
        
        if len(cocktails) > 5:
            response += f"... и ещё {len(cocktails) - 5} коктейлей\n"
        
        response += "💡 *Команды:*\n• 'Оцени [коктейль] 5 звёзд' - поставить оценку\n• 'Сохрани [коктейль]' - добавить в избранное"
        
        return response
    
    async def _handle_rate_cocktail(self, message: str, user_id: int) -> str:
        """Оценка коктейля"""
        # Извлекаем название коктейля и оценку
        rating_match = re.search(r'оцени\s+(.+?)\s+(\d+)\s*звезд', message.lower())
        if not rating_match:
            return "❌ Формат: 'Оцени Мартини 5 звёзд'"
        
        cocktail_name = rating_match.group(1).strip()
        rating = int(rating_match.group(2))
        
        if not 1 <= rating <= 5:
            return "❌ Оценка должна быть от 1 до 5 звёзд"
        
        # Находим коктейль в базе
        cocktails = self.db.advanced_search({'name': cocktail_name})
        if not cocktails:
            return f"❌ Коктейль '{cocktail_name}' не найден"
        
        cocktail = cocktails[0]
        success = self.db.rate_cocktail(user_id, cocktail['id'], rating)
        
        if success:
            return f"⭐ Оценка сохранена!\n\n🥃 *{cocktail['name']}*\n⭐ {rating}/5 звёзд\n\nСпасибо за оценку!"
        else:
            return "❌ Ошибка сохранения оценки"
    
    async def _handle_add_favorite(self, message: str, user_id: int) -> str:
        """Добавление в избранное"""
        cocktail_match = re.search(r'(?:сохрани|добавь в избранное)\s+(.+)', message.lower())
        if not cocktail_match:
            return "❌ Формат: 'Сохрани Мартини' или 'Добавь в избранное Негрони'"
        
        cocktail_name = cocktail_match.group(1).strip()
        
        # Находим коктейль
        cocktails = self.db.advanced_search({'name': cocktail_name})
        if not cocktails:
            return f"❌ Коктейль '{cocktail_name}' не найден"
        
        cocktail = cocktails[0]
        success = self.db.add_to_favorites(user_id, cocktail['id'])
        
        if success:
            return f"❤️ *{cocktail['name']}* добавлен в избранное!\n\n💡 Посмотреть избранное: 'Мои избранные'"
        else:
            return "❌ Ошибка добавления в избранное"
    
    async def _handle_show_favorites(self, user_id: int) -> str:
        """Показ избранных коктейлей"""
        favorites = self.db.get_favorites(user_id)
        
        if not favorites:
            return "❤️ *Избранное пусто*\n\nДобавьте коктейли командой:\n• 'Сохрани Мартини'\n• 'Добавь в избранное Негрони'"
        
        response = "❤️ *Ваши избранные коктейли:*\n\n"
        
        for cocktail in favorites[:10]:  # Показываем первые 10
            response += f"🥃 *{cocktail['name']}*\n"
            if cocktail.get('description'):
                response += f"📝 {cocktail['description'][:80]}...\n"
            response += f"🍸 База: {cocktail['base_spirit']}\n\n"
        
        if len(favorites) > 10:
            response += f"... и ещё {len(favorites) - 10} коктейлей\n"
        
        return response
    
    async def _handle_create_recipe(self, message: str, user_id: int) -> str:
        """Создание пользовательского рецепта"""
        return "🍹 *Создание рецепта*\n\nДля создания рецепта используйте формат:\n\n```\nСоздай рецепт:\nНазвание: Мой коктейль\nИнгредиенты:\n- Водка 50мл\n- Лайм 20мл\n- Сахарный сироп 15мл\nМетод: Встряхнуть\nОписание: Освежающий коктейль\n```"
    
    async def _handle_show_custom_recipes(self, user_id: int) -> str:
        """Показ пользовательских рецептов"""
        recipes = self.db.get_custom_recipes(user_id)
        
        if not recipes:
            return "👨‍🍳 *У вас нет собственных рецептов*\n\nСоздайте рецепт командой 'Создай рецепт'"
        
        response = "👨‍🍳 *Ваши рецепты:*\n\n"
        
        for recipe in recipes:
            response += f"🥃 *{recipe['name']}*\n"
            response += f"📝 {recipe['description'][:80]}...\n"
            response += f"⏱️ Время: {recipe['prep_time']}\n\n"
        
        return response
    
    async def _handle_create_collection(self, message: str, user_id: int) -> str:
        """Создание подборки коктейлей"""
        return "📚 *Создание подборки*\n\nДля создания подборки используйте формат:\n\n```\nСоздай подборку:\nНазвание: Классические коктейли\nОписание: Лучшие классические рецепты\nКоктейли: Мартини, Негрони, Манхеттен\n```"
    
    async def _handle_show_collections(self, user_id: int) -> str:
        """Показ подборок"""
        collections = self.db.get_collections(user_id)
        
        if not collections:
            return "📚 *У вас нет подборок*\n\nСоздайте подборку командой 'Создай подборку'"
        
        response = "📚 *Ваши подборки:*\n\n"
        
        for collection in collections:
            response += f"📖 *{collection['name']}*\n"
            response += f"📝 {collection['description'][:80]}...\n"
            response += f"🍹 Коктейлей: {len(collection['cocktail_ids'])}\n\n"
        
        return response
    
    async def _handle_advanced_search(self, message: str) -> str:
        """Продвинутый поиск"""
        filters = {}
        
        # Извлекаем фильтры
        if "джин" in message.lower():
            filters['base_spirit'] = "джин"
        elif "водка" in message.lower():
            filters['base_spirit'] = "водка"
        elif "ром" in message.lower():
            filters['base_spirit'] = "ром"
        elif "текила" in message.lower():
            filters['base_spirit'] = "текила"
        elif "виски" in message.lower():
            filters['base_spirit'] = "виски"
        
        if "легкий" in message.lower() or "простой" in message.lower():
            filters['difficulty'] = "easy"
        elif "сложный" in message.lower():
            filters['difficulty'] = "hard"
        
        cocktails = self.db.advanced_search(filters)
        
        if not cocktails:
            return "❌ *Коктейли не найдены*\n\nПопробуйте изменить критерии поиска"
        
        response = f"🔍 *Найдено {len(cocktails)} коктейлей:*\n\n"
        
        for cocktail in cocktails[:5]:
            response += f"🥃 *{cocktail['name']}*\n"
            response += f"🍸 База: {cocktail['base_spirit']}\n"
            if cocktail.get('difficulty'):
                response += f"⚡ Сложность: {cocktail['difficulty']}\n"
            response += "\n"
        
        if len(cocktails) > 5:
            response += f"... и ещё {len(cocktails) - 5} коктейлей\n"
        
        return response
    
    async def _handle_show_catalog(self, message: str) -> str:
        """Показ каталога ингредиентов"""
        category = None
        
        if "базовые" in message.lower():
            category = "base_spirits"
        elif "ликёры" in message.lower():
            category = "liqueurs"
        elif "миксеры" in message.lower():
            category = "mixers"
        elif "добавки" in message.lower():
            category = "additives"
        
        ingredients = self.db.get_ingredient_catalog(category)
        
        if not ingredients:
            return "❌ *Ингредиенты не найдены*"
        
        # Группируем по категориям
        categories = {}
        for ing in ingredients:
            cat = ing['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ing)
        
        response = "📦 *Каталог ингредиентов:*\n\n"
        
        for cat, items in categories.items():
            response += f"📂 *{cat.replace('_', ' ').title()}:*\n"
            for item in items[:5]:  # Показываем первые 5 в категории
                response += f"• {item['name'].title()}"
                if item['substitutes']:
                    response += f" (замена: {', '.join(item['substitutes'][:2])})"
                response += "\n"
            if len(items) > 5:
                response += f"... и ещё {len(items) - 5}\n"
            response += "\n"
        
        return response
    
    async def _handle_help(self) -> str:
        """Помощь по командам"""
        return """🍹 *MIXTRIX Bot*

*🏠 Управление баром:*
• 'Добавь водку' - добавить ингредиент
• 'Мой бар' - показать ингредиенты
• 'Что приготовить?' - найти доступные коктейли

*⭐ Оценки и избранное:*
• 'Оцени Мартини 5 звёзд' - поставить оценку
• 'Сохрани Негрони' - добавить в избранное
• 'Мои избранные' - показать избранное

*👨‍🍳 Собственные рецепты:*
• 'Создай рецепт' - создать свой рецепт
• 'Мои рецепты' - показать свои рецепты

*📚 Подборки:*
• 'Создай подборку' - создать коллекцию
• 'Мои подборки' - показать подборки

*🔍 Поиск:*
• 'Поиск джин' - найти коктейли с джином
• 'Каталог ингредиентов' - показать все ингредиенты
• 'Помощь' - эта справка

*💡 Просто спросите о любом коктейле!*"""
    
    async def _handle_cocktail_search(self, message: str) -> str:
        """Обычный поиск коктейля"""
        # Используем Yandex API для поиска
        try:
            response = await self.yandex_service.generate_response(message)
            return response
        except Exception as e:
            return f"❌ Ошибка поиска: {str(e)}"
    
    def _determine_ingredient_category(self, ingredient_name: str) -> str:
        """Определение категории ингредиента"""
        name_lower = ingredient_name.lower()
        
        base_spirits = ["водка", "джин", "ром", "виски", "текила", "коньяк", "бренди"]
        liqueurs = ["кампари", "апероль", "вермут", "трипл сек", "куантро", "крем де какао"]
        mixers = ["сок", "содовая", "тоник", "кола", "спрайт"]
        additives = ["сироп", "мед", "соль", "перец", "биттерс", "мята", "лайм", "лимон"]
        
        if any(spirit in name_lower for spirit in base_spirits):
            return "base_spirits"
        elif any(liqueur in name_lower for liqueur in liqueurs):
            return "liqueurs"
        elif any(mixer in name_lower for mixer in mixers):
            return "mixers"
        elif any(additive in name_lower for additive in additives):
            return "additives"
        else:
            return "other"
