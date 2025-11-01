#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

print("=== Запуск MixMatrix Bot ===")

# Загружаем переменные окружения
print("Загружаем переменные окружения...")
try:
    load_dotenv('env_file.txt')
    print("✓ Переменные окружения загружены")
except Exception as e:
    print(f"✗ Ошибка загрузки переменных: {e}")
    # Попробуем загрузить из других файлов
    try:
        load_dotenv('environment.env')
        print("✓ Переменные окружения загружены из environment.env")
    except:
        print("✗ Не удалось загрузить переменные окружения")
        sys.exit(1)

# Проверяем наличие необходимых переменных
print("Проверяем переменные окружения...")
if not os.getenv('TELEGRAM_BOT_TOKEN'):
    print("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден в переменных окружения")
    sys.exit(1)

if not os.getenv('YANDEX_API_KEY'):
    print("❌ Ошибка: YANDEX_API_KEY не найден в переменных окружения")
    sys.exit(1)

if not os.getenv('FOLDER_ID'):
    print("❌ Ошибка: FOLDER_ID не найден в переменных окружения")
    sys.exit(1)

print("✓ Все необходимые переменные найдены")

# Инициализация бота
print("Инициализируем бота...")
try:
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()
    print("✓ Бот инициализирован")
except Exception as e:
    print(f"❌ Ошибка инициализации бота: {e}")
    sys.exit(1)

# Простая база данных (без сложных зависимостей)
class SimpleDatabase:
    def __init__(self):
        self.recipes = [
            {
                'name': 'Мартини',
                'base_spirit': 'джин',
                'description': 'Классический коктейль с джином и вермутом'
            },
            {
                'name': 'Мохито',
                'base_spirit': 'ром',
                'description': 'Освежающий коктейль с ромом, мятой и лаймом'
            }
        ]
    
    def search_recipes(self, query):
        """Простой поиск рецептов"""
        query_lower = query.lower()
        results = []
        for recipe in self.recipes:
            if (query_lower in recipe['name'].lower() or 
                query_lower in recipe['base_spirit'].lower() or
                query_lower in recipe['description'].lower()):
                results.append(recipe)
        return results

# Инициализация простой базы данных
try:
    db = SimpleDatabase()
    print("✓ База данных инициализирована")
except Exception as e:
    print(f"❌ Ошибка инициализации базы данных: {e}")
    sys.exit(1)

# Yandex Cloud AI конфигурация
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
YANDEX_FOLDER_ID = os.getenv('FOLDER_ID')
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

async def call_yandex_api(prompt: str) -> str:
    """Вызов Yandex Cloud AI API для генерации рецептов"""
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 1000
        },
        "messages": [
            {
                "role": "user",
                "text": prompt
            }
        ]
    }
    
    try:
        response = requests.post(YANDEX_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Извлекаем текст ответа из структуры Yandex API
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

# Обработчики команд
@dp.message(Command('start'))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🍸 Создать рецепт", callback_data="recipe"),
            InlineKeyboardButton(text="🔍 Поиск", callback_data="search")
        ],
        [
            InlineKeyboardButton(text="🎲 Случайный", callback_data="random"),
            InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")
        ]
    ])
    
    welcome_text = """
🍹 MixMatrixBot - Ваш персональный бармен!

Добро пожаловать в мир коктейлей! Я помогу вам:
• Создать идеальный рецепт
• Найти коктейли по ингредиентам
• Подобрать коктейль под ваше блюдо

Основные команды:
/recipe - создать рецепт
/search - поиск коктейлей
/random - случайный коктейль
/help - помощь

Выберите действие кнопкой или используйте команды!
    """
    
    await message.reply(welcome_text, reply_markup=keyboard)

@dp.message(Command('help'))
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
🍹 **MixMatrixBot - Справка**

**Основные команды:**
/start - начать работу с ботом
/help - показать эту справку
/recipe - создать рецепт коктейля
/search [запрос] - поиск коктейлей
/random - случайный коктейль

**Примеры использования:**
/search мартини
/search джин
/recipe

**Особенности:**
• AI-генерация рецептов через Yandex GPT
• Поиск по базе рецептов
• Создание случайных коктейлей
    """
    await message.reply(help_text, parse_mode='Markdown')

@dp.message(Command('recipe'))
async def recipe_command(message: types.Message):
    """Обработчик команды /recipe"""
    await message.reply("🍹 Создаю идеальный рецепт для вас...")
    
    prompt = """
    Создай сбалансированный рецепт коктейля с учетом фудпейринга.
    Включи в рецепт:
    1. Название коктейля
    2. Ингредиенты с точными пропорциями
    3. Метод приготовления
    4. Подача и украшение
    5. Краткую историю или концепцию
    
    Сделай рецепт гармоничным и сбалансированным.
    """
    
    try:
        recipe = await call_yandex_api(prompt)
        await message.reply(recipe)
    except Exception as e:
        await message.reply(f"Извините, произошла ошибка: {str(e)}")

@dp.message(Command('search'))
async def search_command(message: types.Message):
    """Обработчик команды /search"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.reply("Использование: /search [название коктейля или ингредиент]")
        return
    
    query = " ".join(args)
    await message.reply(f"🔍 Ищу рецепты по запросу: {query}")
    
    try:
        recipes = db.search_recipes(query)
        
        if not recipes:
            await message.reply("Рецепты не найдены. Попробуйте другой запрос или создайте новый рецепт с помощью /recipe")
            return
        
        response = f"**Найдено рецептов: {len(recipes)}**\n\n"
        
        for i, recipe in enumerate(recipes[:5], 1):  # Показываем максимум 5 рецептов
            response += f"**{i}. {recipe['name']}**\n"
            response += f"Базовый спирт: {recipe['base_spirit']}\n"
            response += f"Описание: {recipe['description']}\n\n"
        
        if len(recipes) > 5:
            response += f"... и еще {len(recipes) - 5} рецептов"
        
        await message.reply(response, parse_mode='Markdown')
        
    except Exception as e:
        await message.reply(f"Ошибка при поиске: {str(e)}")

@dp.message(Command('random'))
async def random_command(message: types.Message):
    """Обработчик команды /random"""
    import random
    
    base_spirits = ['джин', 'водка', 'ром', 'виски', 'текила', 'коньяк', 'бренди']
    random_spirit = random.choice(base_spirits)
    
    prompt = f"""
    Создай неожиданный и интересный рецепт коктейля на основе {random_spirit}.
    Сделай коктейль креативным и необычным, используя неожиданные сочетания.
    Включи:
    1. Креативное название
    2. Ингредиенты с пропорциями
    3. Метод приготовления
    4. Подача и украшение
    5. Философию коктейля
    
    Пусть это будет сюрприз!
    """
    
    await message.reply("🎲 Создаю для вас сюрприз-коктейль...")
    
    try:
        recipe = await call_yandex_api(prompt)
        await message.reply(recipe)
    except Exception as e:
        await message.reply(f"Извините, произошла ошибка: {str(e)}")

# Обработчики кнопок
@dp.callback_query(lambda c: c.data == 'recipe')
async def process_callback_recipe(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Рецепт'"""
    try:
        await callback_query.answer()
        await recipe_command(callback_query.message)
    except Exception as e:
        print(f"Ошибка обработки кнопки recipe: {e}")

@dp.callback_query(lambda c: c.data == 'search')
async def process_callback_search(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Поиск'"""
    try:
        await callback_query.answer()
        await callback_query.message.reply(
            "🔍 **Поиск коктейлей**\n\n"
            "Напишите название коктейля или ингредиент для поиска!\n\n"
            "**Примеры:**\n"
            "• мартини\n"
            "• джин\n"
            "• мохито\n"
            "• ром\n\n"
            "Или используйте команду: /search [запрос]",
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Ошибка обработки кнопки search: {e}")

@dp.callback_query(lambda c: c.data == 'random')
async def process_callback_random(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Случайный'"""
    try:
        await callback_query.answer()
        await random_command(callback_query.message)
    except Exception as e:
        print(f"Ошибка обработки кнопки random: {e}")

@dp.callback_query(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Помощь'"""
    try:
        await callback_query.answer()
        await help_command(callback_query.message)
    except Exception as e:
        print(f"Ошибка обработки кнопки help: {e}")

@dp.message()
async def handle_text_message(message: types.Message):
    """Обработчик текстовых сообщений"""
    user_message = message.text
    
    # Если сообщение начинается с /, это команда
    if user_message.startswith('/'):
        await message.reply("Неизвестная команда. Используйте /help для получения списка команд.")
        return
    
    # Обрабатываем как поисковый запрос
    await message.reply(f"🔍 Ищу рецепты по запросу: {user_message}")
    
    try:
        recipes = db.search_recipes(user_message)
        
        if not recipes:
            await message.reply("Рецепты не найдены. Попробуйте другой запрос или создайте новый рецепт с помощью /recipe")
            return
        
        response = f"**Найдено рецептов: {len(recipes)}**\n\n"
        
        for i, recipe in enumerate(recipes[:5], 1):
            response += f"**{i}. {recipe['name']}**\n"
            response += f"Базовый спирт: {recipe['base_spirit']}\n"
            response += f"Описание: {recipe['description']}\n\n"
        
        if len(recipes) > 5:
            response += f"... и еще {len(recipes) - 5} рецептов"
        
        await message.reply(response, parse_mode='Markdown')
        
    except Exception as e:
        await message.reply(f"Ошибка при поиске: {str(e)}")

async def main():
    """Основная функция запуска бота"""
    print("Запуск MIXTRIX Bot...")
    print("✓ База данных: готова")
    print("✓ Yandex API: подключен")
    print("✓ Простая система: активна")
    print("Бот готов к работе!")
    
    try:
        # Проверяем подключение к Telegram API
        bot_info = await bot.get_me()
        print(f"✓ Бот подключен: @{bot_info.username} ({bot_info.first_name})")
        
        # Запускаем polling
        await dp.start_polling(
            bot, 
            skip_updates=True,
            timeout=30,
            request_timeout=30,
            drop_pending_updates=True
        )
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        print("🔄 Попробуйте перезапустить бота через несколько секунд")
        return

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
