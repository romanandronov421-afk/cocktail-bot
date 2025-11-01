#!/usr/bin/env python3
"""
MIXTRIX🍸 Professional Telegram Bot
Профессиональный Telegram бот для баров и ресторанов

M - Mixology
I - Innovation  
X - X-factor
T - Taste
R - Recipes
I - Ingredients
X - Xperience
"""

import asyncio
import logging
import os
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime
import json

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

from mixtrix_professional import MIXTRIXBot, UserRole, CocktailCategory, DifficultyLevel
from mixtrix_ai import MIXTRIXAI, FlavorProfile
from populate_mixtrix_db import MIXTRIXDatabasePopulator
from seasonal_ingredients_service import SeasonalIngredientsService

# Загружаем переменные окружения
load_dotenv('env_file.txt')

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MIXTRIX_BOT')

# Инициализация бота
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()

# Инициализация MIXTRIX системы
mixtrix_system = MIXTRIXBot()
mixtrix_ai = MIXTRIXAI()
seasonal_service = SeasonalIngredientsService()

# Кэш пользователей
user_cache = {}

class MIXTRIXTelegramBot:
    """Основной класс MIXTRIX Telegram бота"""
    
    def __init__(self):
        self.bot = bot
        self.dp = dp
        self.mixtrix = mixtrix_system
        self.ai = mixtrix_ai
        self.logger = logger
    
    async def initialize(self):
        """Инициализация системы"""
        await self.mixtrix.initialize()
        self.logger.info("🍸 MIXTRIX Professional System initialized")
    
    def get_user_role(self, user_id: int) -> UserRole:
        """Получение роли пользователя"""
        # В реальном приложении это будет из базы данных
        return UserRole.BARTENDER
    
    def get_main_menu_keyboard(self, user_role: UserRole) -> InlineKeyboardMarkup:
        """Главное меню в зависимости от роли пользователя"""
        builder = InlineKeyboardBuilder()
        
        if user_role in [UserRole.BARTENDER, UserRole.BARISTA]:
            builder.add(InlineKeyboardButton(
                text="🍸 Генерация рецептов",
                callback_data="generate_recipe"
            ))
            builder.add(InlineKeyboardButton(
                text="📋 Создание меню",
                callback_data="create_menu"
            ))
            builder.add(InlineKeyboardButton(
                text="🍽️ Фудпейринг",
                callback_data="food_pairing"
            ))
            builder.add(InlineKeyboardButton(
                text="🌿 Сезонные рекомендации",
                callback_data="seasonal"
            ))
        
        if user_role in [UserRole.MANAGER, UserRole.OWNER]:
            builder.add(InlineKeyboardButton(
                text="📊 Аналитика",
                callback_data="analytics"
            ))
            builder.add(InlineKeyboardButton(
                text="💰 Расчет стоимости",
                callback_data="cost_calculation"
            ))
            builder.add(InlineKeyboardButton(
                text="📈 Тренды индустрии",
                callback_data="industry_trends"
            ))
        
        # Общие функции
        builder.add(InlineKeyboardButton(
            text="📰 Новости HORECA",
            callback_data="horeca_news"
        ))
        builder.add(InlineKeyboardButton(
            text="❓ Помощь",
            callback_data="help"
        ))
        
        builder.adjust(2)
        return builder.as_markup()
    
    def get_difficulty_keyboard(self) -> InlineKeyboardMarkup:
        """Клавиатура выбора сложности"""
        builder = InlineKeyboardBuilder()
        
        difficulties = [
            ("🟢 Начинающий", "beginner"),
            ("🟡 Средний", "intermediate"),
            ("🟠 Продвинутый", "advanced"),
            ("🔴 Эксперт", "expert")
        ]
        
        for text, data in difficulties:
            builder.add(InlineKeyboardButton(
                text=text,
                callback_data=f"difficulty_{data}"
            ))
        
        builder.adjust(2)
        return builder.as_markup()
    
    def get_season_keyboard(self) -> InlineKeyboardMarkup:
        """Клавиатура выбора сезона"""
        builder = InlineKeyboardBuilder()
        
        seasons = [
            ("🌸 Весна", "spring"),
            ("☀️ Лето", "summer"),
            ("🍂 Осень", "autumn"),
            ("❄️ Зима", "winter")
        ]
        
        for text, data in seasons:
            builder.add(InlineKeyboardButton(
                text=text,
                callback_data=f"season_{data}"
            ))
        
        builder.adjust(2)
        return builder.as_markup()
    
    def get_base_spirit_keyboard(self) -> InlineKeyboardMarkup:
        """Клавиатура выбора базового спирта"""
        builder = InlineKeyboardBuilder()
        
        spirits = [
            ("🍸 Джин", "джин лондонский"),
            ("🥃 Водка", "водка премиум"),
            ("🍹 Ром", "ром белый"),
            ("🌵 Текила", "текила"),
            ("🥃 Виски", "виски ржаной"),
            ("🍷 Коньяк", "коньяк")
        ]
        
        for text, data in spirits:
            builder.add(InlineKeyboardButton(
                text=text,
                callback_data=f"spirit_{data}"
            ))
        
        builder.adjust(2)
        return builder.as_markup()

# Инициализация бота
mixtrix_bot = MIXTRIXTelegramBot()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    user_role = mixtrix_bot.get_user_role(user_id)
    
    welcome_text = f"""
🍸 *Добро пожаловать в MIXTRIX!*

*M* - Mixology | *I* - Innovation | *X* - X-factor
*T* - Taste | *R* - Recipes | *I* - Ingredients | *X* - Xperience

Профессиональная система для создания коктейлей и управления барными картами.

Ваша роль: *{user_role.value.title()}*

Выберите действие:
"""
    
    keyboard = mixtrix_bot.get_main_menu_keyboard(user_role)
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode='Markdown')

@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
🍸 *MIXTRIX Professional System*

*Основные функции:*

🍸 *Генерация рецептов*
• AI-создание коктейлей с фудпейрингом
• Сезонные рекомендации
• Адаптация под целевую аудиторию

📋 *Создание меню*
• Сезонные коктейльные карты
• Концептуальные меню
• Расчет стоимости и маржи

🍽️ *Фудпейринг*
• Сочетание коктейлей с блюдами
• Рекомендации на основе Flavor Bible
• Анализ вкусовых профилей

🌿 *Сезонность*
• Российские сезонные ингредиенты
• Адаптация под климат
• Локальные продукты

📰 *HORECA новости*
• Тренды индустрии
• Новости от Difford's Guide
• Обновления рынка

*Команды:*
/start - Главное меню
/help - Эта справка
/menu - Создание меню
/recipe - Генерация рецепта
/news - Новости индустрии
/seasonal - Сезонные ингредиенты
/ingredients - Поиск по ингредиентам
"""
    
    await message.answer(help_text, parse_mode='Markdown')

@dp.message(Command("seasonal"))
async def seasonal_command(message: types.Message):
    """Обработчик команды /seasonal - сезонные ингредиенты"""
    try:
        # Получаем все сезонные ингредиенты для текущего сезона
        seasonal_message = seasonal_service.format_all_seasonal_ingredients_message()
        
        # Создаем клавиатуру для выбора базового спирта
        keyboard = InlineKeyboardBuilder()
        base_spirits = ["джин лондонский", "водка премиум", "виски ржаной", "коньяк", "ром белый", "текила"]
        
        for spirit in base_spirits:
            keyboard.add(InlineKeyboardButton(
                text=spirit.title(),
                callback_data=f"seasonal_{spirit}"
            ))
        
        keyboard.adjust(2)  # 2 кнопки в ряду
        
        await message.answer(
            seasonal_message + "\n\n🍸 *Выберите базовый спирт для детального просмотра:*",
            reply_markup=keyboard.as_markup(),
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Ошибка в команде seasonal: {e}")
        await message.answer("❌ Произошла ошибка при получении сезонных ингредиентов.")

@dp.message(Command("ingredients"))
async def ingredients_command(message: types.Message):
    """Обработчик команды /ingredients - поиск по ингредиентам"""
    try:
        text = """
🍸 *Поиск коктейлей по ингредиентам*

Введите ингредиенты через запятую или пробел.
Например: "джин, лайм, мята" или "водка лимон сахар"

*Доступные команды:*
• Напишите ингредиенты для поиска коктейлей
• Используйте /seasonal для просмотра сезонных ингредиентов
        """
        
        await message.answer(text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Ошибка в команде ingredients: {e}")
        await message.answer("❌ Произошла ошибка при обработке команды.")

@dp.callback_query(lambda c: c.data.startswith("seasonal_"))
async def handle_seasonal_spirit(callback: CallbackQuery):
    """Обработчик выбора базового спирта для сезонных ингредиентов"""
    await callback.answer()
    
    try:
        base_spirit = callback.data.replace("seasonal_", "")
        
        # Получаем сезонные ингредиенты для выбранного спирта
        seasonal_message = seasonal_service.format_seasonal_ingredients_message(base_spirit)
        
        # Получаем предложения коктейлей
        suggestions = seasonal_service.get_seasonal_cocktail_suggestions(base_spirit)
        
        if suggestions:
            seasonal_message += "\n\n🍸 *Рекомендуемые коктейли:*\n"
            for cocktail in suggestions:
                seasonal_message += f"• *{cocktail['name']}* - {cocktail['description'][:60]}...\n"
        
        # Создаем клавиатуру для возврата
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(
            text="🔙 Назад к сезонным ингредиентам",
            callback_data="back_to_seasonal"
        ))
        
        await callback.message.edit_text(
            seasonal_message,
            reply_markup=keyboard.as_markup(),
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Ошибка в обработчике сезонных ингредиентов: {e}")
        await callback.message.edit_text("❌ Произошла ошибка при получении информации.")

@dp.callback_query(lambda c: c.data == "back_to_seasonal")
async def handle_back_to_seasonal(callback: CallbackQuery):
    """Обработчик возврата к сезонным ингредиентам"""
    await callback.answer()
    
    try:
        # Возвращаемся к общему списку сезонных ингредиентов
        seasonal_message = seasonal_service.format_all_seasonal_ingredients_message()
        
        # Создаем клавиатуру для выбора базового спирта
        keyboard = InlineKeyboardBuilder()
        base_spirits = ["джин лондонский", "водка премиум", "виски ржаной", "коньяк", "ром белый", "текила"]
        
        for spirit in base_spirits:
            keyboard.add(InlineKeyboardButton(
                text=spirit.title(),
                callback_data=f"seasonal_{spirit}"
            ))
        
        keyboard.adjust(2)
        
        await callback.message.edit_text(
            seasonal_message + "\n\n🍸 *Выберите базовый спирт для детального просмотра:*",
            reply_markup=keyboard.as_markup(),
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Ошибка при возврате к сезонным ингредиентам: {e}")
        await callback.message.edit_text("❌ Произошла ошибка при возврате.")

@dp.callback_query(lambda c: c.data == "generate_recipe")
async def handle_generate_recipe(callback: CallbackQuery):
    """Обработчик генерации рецепта"""
    await callback.answer()
    
    text = """
🍸 *Генерация рецепта коктейля*

Выберите базовый спирт:
"""
    
    keyboard = mixtrix_bot.get_base_spirit_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='Markdown')

@dp.callback_query(lambda c: c.data.startswith("spirit_"))
async def handle_spirit_selection(callback: CallbackQuery):
    """Обработчик выбора спирта"""
    await callback.answer()
    
    spirit = callback.data.replace("spirit_", "")
    
    # Сохраняем выбор пользователя
    user_cache[callback.from_user.id] = {"base_spirit": spirit}
    
    text = f"""
🍸 *Выбран базовый спирт: {spirit}*

Выберите сложность рецепта:
"""
    
    keyboard = mixtrix_bot.get_difficulty_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='Markdown')

@dp.callback_query(lambda c: c.data.startswith("difficulty_"))
async def handle_difficulty_selection(callback: CallbackQuery):
    """Обработчик выбора сложности"""
    await callback.answer()
    
    difficulty = callback.data.replace("difficulty_", "")
    
    # Сохраняем выбор пользователя
    if callback.from_user.id not in user_cache:
        user_cache[callback.from_user.id] = {}
    user_cache[callback.from_user.id]["difficulty"] = difficulty
    
    text = f"""
🍸 *Сложность: {difficulty}*

Выберите сезон:
"""
    
    keyboard = mixtrix_bot.get_season_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='Markdown')

@dp.callback_query(lambda c: c.data.startswith("season_"))
async def handle_season_selection(callback: CallbackQuery):
    """Обработчик выбора сезона и генерации рецепта"""
    await callback.answer()
    
    season = callback.data.replace("season_", "")
    
    # Получаем данные пользователя
    user_data = user_cache.get(callback.from_user.id, {})
    base_spirit = user_data.get("base_spirit", "джин лондонский")
    difficulty = user_data.get("difficulty", "intermediate")
    
    # Показываем загрузку
    await callback.message.edit_text("🤖 Генерирую рецепт...")
    
    try:
        # Создаем профиль вкуса
        flavor_profile = FlavorProfile(
            primary="citrus",
            secondary=["herbal", "fresh"],
            intensity="medium",
            acidity="high",
            sweetness="medium",
            bitterness="light"
        )
        
        # Генерируем рецепт
        recipe = await mixtrix_ai.generate_cocktail_recipe(
            base_spirit=base_spirit,
            flavor_profile=flavor_profile,
            difficulty=difficulty,
            season=season,
            food_pairing="устрицы",
            target_audience="профессионалы"
        )
        
        # Форматируем ответ
        response = f"""
🍸 *{recipe['name']}*

*База:* {recipe['base_spirit']}
*Сезон:* {recipe['season'].title()}
*Сложность:* {recipe['difficulty'].title()}

*Ингредиенты:*
"""
        
        for ingredient, details in recipe['ingredients'].items():
            response += f"• {ingredient}: {details['amount']} {details['unit']}\n"
        
        response += f"""
*Метод приготовления:*
{recipe['method']}

*Бокал:* {recipe['glassware']}
*Гарнир:* {recipe['garnish']}

*Описание:*
{recipe['description']}

*Фудпейринг:* {', '.join(recipe['food_pairings'])}

*Время приготовления:* {recipe['prep_time']} сек
*Стоимость:* {recipe['cost_estimate']:.0f} руб
*Маржа:* {recipe['profit_margin']*100:.0f}%
"""
        
        # Кнопка для сохранения
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="💾 Сохранить рецепт",
            callback_data=f"save_recipe_{recipe['id']}"
        ))
        builder.add(InlineKeyboardButton(
            text="🔄 Новый рецепт",
            callback_data="generate_recipe"
        ))
        
        await callback.message.edit_text(response, reply_markup=builder.as_markup(), parse_mode='Markdown')
        
    except Exception as e:
        error_text = f"❌ Ошибка генерации рецепта: {str(e)}"
        await callback.message.edit_text(error_text)

@dp.callback_query(lambda c: c.data == "horeca_news")
async def handle_horeca_news(callback: CallbackQuery):
    """Обработчик новостей HORECA"""
    await callback.answer()
    
    news_text = """
📰 *Новости HORECA индустрии*

*Последние тренды:*
• Рост популярности сезонных коктейлей
• Использование локальных ингредиентов
• Функциональные коктейли с добавками
• Экологически чистые барные практики

*Российский рынок:*
• Увеличение спроса на премиальные коктейли
• Развитие коктейльной культуры в регионах
• Популярность русских ингредиентов (облепиха, ревень)

*Источники:*
• Difford's Guide
• Imbibe Magazine
• Bar Magazine
• Cocktail Society

*Обновления каждые 24 часа*
"""
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🔄 Обновить",
        callback_data="horeca_news"
    ))
    builder.add(InlineKeyboardButton(
        text="📋 Главное меню",
        callback_data="main_menu"
    ))
    
    await callback.message.edit_text(news_text, reply_markup=builder.as_markup(), parse_mode='Markdown')

@dp.callback_query(lambda c: c.data == "main_menu")
async def handle_main_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    await callback.answer()
    
    user_id = callback.from_user.id
    user_role = mixtrix_bot.get_user_role(user_id)
    
    text = """
🍸 *MIXTRIX Professional System*

Выберите действие:
"""
    
    keyboard = mixtrix_bot.get_main_menu_keyboard(user_role)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='Markdown')

@dp.message()
async def handle_text_message(message: types.Message):
    """Обработчик текстовых сообщений"""
    user_id = message.from_user.id
    user_role = mixtrix_bot.get_user_role(user_id)
    
    # Проверяем, является ли сообщение поиском по ингредиентам
    if any(keyword in message.text.lower() for keyword in ['найди', 'поиск', 'что можно', 'ингредиенты']):
        try:
            # Извлекаем ингредиенты из сообщения
            ingredients_text = message.text.lower()
            
            # Убираем служебные слова
            for word in ['найди', 'поиск', 'что можно', 'ингредиенты', 'коктейли', 'с', 'из']:
                ingredients_text = ingredients_text.replace(word, '')
            
            # Разделяем ингредиенты
            ingredients = [ing.strip() for ing in ingredients_text.replace(',', ' ').split() if ing.strip()]
            
            if ingredients:
                # Ищем коктейли с этими ингредиентами
                conn = sqlite3.connect('mixtrix_professional.db')
                cursor = conn.cursor()
                
                found_cocktails = []
                for ingredient in ingredients:
                    cursor.execute("""
                        SELECT name, name_en, base_spirit, ingredients, description
                        FROM cocktails
                        WHERE ingredients LIKE ? OR name LIKE ? OR description LIKE ?
                        LIMIT 5
                    """, (f"%{ingredient}%", f"%{ingredient}%", f"%{ingredient}%"))
                    
                    for row in cursor.fetchall():
                        cocktail = {
                            "name": row[0],
                            "name_en": row[1],
                            "base_spirit": row[2],
                            "ingredients": json.loads(row[3]) if row[3] else {},
                            "description": row[4]
                        }
                        found_cocktails.append(cocktail)
                
                conn.close()
                
                if found_cocktails:
                    response = f"🍸 *Найдено коктейлей с ингредиентами: {', '.join(ingredients)}*\n\n"
                    for cocktail in found_cocktails[:5]:  # Показываем первые 5
                        response += f"• *{cocktail['name']}* ({cocktail['name_en']})\n"
                        response += f"  🥃 База: {cocktail['base_spirit']}\n"
                        response += f"  📝 {cocktail['description'][:80]}...\n\n"
                    
                    response += "💡 Используйте /seasonal для просмотра сезонных ингредиентов"
                else:
                    response = f"❌ Коктейли с ингредиентами '{', '.join(ingredients)}' не найдены.\n\n"
                    response += "💡 Попробуйте:\n"
                    response += "• Использовать /seasonal для просмотра доступных ингредиентов\n"
                    response += "• Проверить правильность написания ингредиентов\n"
                    response += "• Использовать синонимы (например, 'лимон' вместо 'лайм')"
                
                await message.reply(response, parse_mode='Markdown')
                return
            else:
                await message.reply("❌ Не удалось определить ингредиенты. Попробуйте написать их через запятую или пробел.")
                return
                
        except Exception as e:
            logger.error(f"Ошибка при поиске по ингредиентам: {e}")
            await message.reply("❌ Произошла ошибка при поиске коктейлей.")
            return
    
    # Обрабатываем через MIXTRIX систему
    response = await mixtrix_bot.mixtrix.process_user_request(
        user_id=user_id,
        message=message.text,
        user_role=user_role
    )
    
    await message.reply(response, parse_mode='Markdown')

async def main():
    """Основная функция запуска бота"""
    print("🍸 Запуск MIXTRIX Professional Telegram Bot...")
    print("M - Mixology | I - Innovation | X - X-factor")
    print("T - Taste | R - Recipes | I - Ingredients | X - Xperience")
    print("=" * 60)
    
    # Инициализация системы
    await mixtrix_bot.initialize()
    
    print("✅ MIXTRIX Professional System готов!")
    print("📱 Telegram Bot запущен")
    print("🌍 Международная поддержка активна")
    print("🤖 AI функции работают")
    print("📊 База данных загружена")
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
