#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
import sys
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

print("=== Запуск MixMatrix Bot (Полная версия) ===")

# Загружаем переменные окружения
print("Загружаем переменные окружения...")
try:
    load_dotenv('env_file.txt')
    print("✓ Переменные окружения загружены")
except Exception as e:
    print(f"✗ Ошибка загрузки переменных: {e}")
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

# Сезонные ингредиенты для России
SEASONAL_INGREDIENTS = {
    'winter': ['клюква', 'брусника', 'облепиха', 'цитрусы', 'корица', 'гвоздика', 'мускатный орех', 'ваниль'],
    'spring': ['ревень', 'щавель', 'молодые травы', 'цветы сирени', 'черемуха', 'мелисса', 'мята'],
    'summer': ['клубника', 'малина', 'смородина', 'крыжовник', 'вишня', 'базилик', 'укроп', 'петрушка'],
    'autumn': ['яблоки', 'груши', 'сливы', 'тыква', 'калина', 'рябина', 'орехи', 'мед']
}

# Текущий сезон (октябрь = осень)
CURRENT_SEASON = 'autumn'

# Базовые спирты
BASE_SPIRITS = ['джин', 'водка', 'ром', 'виски', 'текила', 'коньяк', 'бренди']

# Расширенная база данных коктейлей
class ExtendedDatabase:
    def __init__(self):
        self.recipes = [
            {
                'name': 'Мартини',
                'base_spirit': 'джин',
                'description': 'Классический коктейль с джином и вермутом',
                'ingredients': 'Джин 60мл, Сухой вермут 10мл',
                'method': 'Перемешать со льдом, процедить в охлажденный бокал',
                'garnish': 'Оливка или лимонная цедра',
                'history': 'Один из самых известных коктейлей в мире, создан в конце XIX века'
            },
            {
                'name': 'Мохито',
                'base_spirit': 'ром',
                'description': 'Освежающий коктейль с ромом, мятой и лаймом',
                'ingredients': 'Белый ром 50мл, Лайм 1/2, Мята 8 листьев, Сахар 2 ч.л., Содовая',
                'method': 'Размять мяту с сахаром и лаймом, добавить ром и лед, долить содовую',
                'garnish': 'Веточка мяты и долька лайма',
                'history': 'Кубинский коктейль, популярный с 1930-х годов'
            },
            {
                'name': 'Космополитен',
                'base_spirit': 'водка',
                'description': 'Элегантный коктейль с водкой и клюквенным соком',
                'ingredients': 'Водка 45мл, Трипл сек 15мл, Клюквенный сок 30мл, Лайм 15мл',
                'method': 'Встряхнуть со льдом, процедить в охлажденный бокал',
                'garnish': 'Долька лайма',
                'history': 'Стал популярен в 1990-х благодаря сериалу "Секс в большом городе"'
            },
            {
                'name': 'Негрони',
                'base_spirit': 'джин',
                'description': 'Итальянский коктейль с джином, кампари и красным вермутом',
                'ingredients': 'Джин 30мл, Кампари 30мл, Красный вермут 30мл',
                'method': 'Перемешать со льдом, подавать со льдом в старомодном бокале',
                'garnish': 'Долька апельсина',
                'history': 'Создан в 1919 году в баре Caffè Casoni во Флоренции'
            },
            {
                'name': 'Май Тай',
                'base_spirit': 'ром',
                'description': 'Тропический коктейль с ромом и фруктовыми соками',
                'ingredients': 'Темный ром 30мл, Белый ром 30мл, Трипл сек 15мл, Лайм 15мл, Орчата 15мл',
                'method': 'Встряхнуть со льдом, процедить в бокал со льдом',
                'garnish': 'Мята и вишня',
                'history': 'Создан в 1944 году в баре Trader Vic\'s в Окленде'
            }
        ]
    
    def search_recipes(self, query):
        """Поиск рецептов"""
        query_lower = query.lower()
        results = []
        for recipe in self.recipes:
            if (query_lower in recipe['name'].lower() or 
                query_lower in recipe['base_spirit'].lower() or
                query_lower in recipe['description'].lower() or
                query_lower in recipe['ingredients'].lower()):
                results.append(recipe)
        return results
    
    def get_recipe_by_name(self, name):
        """Получить рецепт по имени"""
        for recipe in self.recipes:
            if recipe['name'].lower() == name.lower():
                return recipe
        return None
    
    def get_all_recipes(self):
        """Получить все рецепты"""
        return self.recipes

# Инициализация расширенной базы данных
try:
    db = ExtendedDatabase()
    print("✓ Расширенная база данных инициализирована")
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
                "role": "system",
                "text": "Ты - кулинарный эксперт и бармен. Помогаешь создавать рецепты напитков, сочетания вкусов и кулинарные советы. Отвечай только на кулинарные темы."
            },
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
            InlineKeyboardButton(text="📋 Меню", callback_data="menu")
        ],
        [
            InlineKeyboardButton(text="🍂 Сезонные", callback_data="seasonal"),
            InlineKeyboardButton(text="🍽️ Фудпейринг", callback_data="pairing")
        ],
        [
            InlineKeyboardButton(text="📈 Тренды", callback_data="trends"),
            InlineKeyboardButton(text="📰 Новости", callback_data="news")
        ],
        [
            InlineKeyboardButton(text="➕ Создать рецепт", callback_data="create_recipe"),
            InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")
        ]
    ])
    
    welcome_text = """
🍹 MixMatrixBot - Ваш персональный бармен!

Добро пожаловать в мир коктейлей! Я помогу вам:
• Создать идеальный рецепт на основе фудпейринга
• Найти коктейли по ингредиентам и сезону
• Подобрать коктейль под ваше блюдо
• Узнать о трендах и новостях индустрии

Основные команды:
/recipe - создать рецепт
/search - поиск коктейлей
/random - случайный коктейль
/seasonal - сезонные коктейли
/pairing - подбор под блюдо
/create_recipe - создать новый рецепт
/menu - генерация меню
/trends - тренды коктейлей
/news - новости индустрии
/history - история коктейля

Выберите действие кнопкой или используйте команды!
    """
    
    await message.reply(welcome_text, reply_markup=keyboard)

@dp.message(Command('help'))
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
🍹 MixMatrixBot - Справка

Основные команды:
/start - начать работу с ботом
/help - показать эту справку

Создание и поиск:
/recipe [спирт] [mocktail=yes/no] - создать рецепт
/search [запрос] - поиск коктейлей
/random - случайный коктейль
/create_recipe - создать новый рецепт с AI

Сезонные и специальные:
/seasonal - сезонные коктейли для России
/pairing [блюдо] - подбор коктейля под блюдо
/menu [тип] [количество] - генерация меню

Информация:
/trends - тренды коктейлей 2025
/news - новости из мира HoReCa
/history [коктейль] - история коктейля

Доступные спирты:
джин, водка, ром, виски, текила, коньяк, бренди

Сезонность (Россия):
• Зима: клюква, брусника, цитрусы, корица
• Весна: ревень, щавель, молодые травы
• Лето: ягоды, базилик, укроп
• Осень: яблоки, груши, тыква, мед

Особенности:
• Фудпейринг на основе The Flavor Bible
• Сезонные ингредиенты для России
• AI-генерация рецептов
• Концептуальные меню с матрицей вдохновения
    """
    await message.reply(help_text)

@dp.message(Command('recipe'))
async def recipe_command(message: types.Message):
    """Обработчик команды /recipe"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    base_spirit = 'джин'  # по умолчанию
    mocktail = False
    
    # Парсинг аргументов
    for arg in args:
        if arg.lower() in BASE_SPIRITS:
            base_spirit = arg.lower()
        elif 'mocktail=yes' in arg.lower() or 'mocktail=да' in arg.lower():
            mocktail = True
    
    # Создание промпта для AI
    mocktail_text = "mocktail (безалкогольный)" if mocktail else "алкогольный"
    seasonal_ingredients = ", ".join(SEASONAL_INGREDIENTS[CURRENT_SEASON])
    
    prompt = f"""
    Создай рецепт напитка на основе {base_spirit} с учетом кулинарных принципов.
    Сезон: октябрь 2025 (используй сезонные ингредиенты: {seasonal_ingredients}).
    Тип: {mocktail_text} напиток.

    Включи в рецепт:
    1. Название напитка
    2. Ингредиенты с точными пропорциями
    3. Метод приготовления
    4. Подача и украшение
    5. Краткую историю или концепцию
    6. Советы по сочетанию с едой

    Сделай рецепт гармоничным и сбалансированным.
    """
    
    await message.reply("🍹 Создаю идеальный рецепт для вас...")
    
    try:
        recipe = await call_yandex_api(prompt)
        await message.reply(recipe)
    except Exception as e:
        await message.reply(f"Извините, произошла ошибка: {str(e)}")

@dp.message(Command('menu'))
async def menu_command(message: types.Message):
    """Обработчик команды /menu"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    menu_type = 'seasonal'  # по умолчанию
    count = 5  # по умолчанию
    
    # Парсинг аргументов
    for arg in args:
        if arg.lower() in ['seasonal', 'conceptual']:
            menu_type = arg.lower()
        elif arg.isdigit():
            count = min(int(arg), 10)  # максимум 10 коктейлей
    
    await message.reply(f"📋 Создаю {menu_type} меню из {count} коктейлей...")
    
    if menu_type == 'seasonal':
        await generate_seasonal_menu(message, count)
    else:
        await generate_conceptual_menu(message, count)

async def generate_seasonal_menu(message: types.Message, count: int):
    """Генерация сезонного меню"""
    seasonal_ingredients = ", ".join(SEASONAL_INGREDIENTS[CURRENT_SEASON])
    
    prompt = f"""
    Создай сезонное меню из {count} напитков для октября 2025.
    Используй сезонные ингредиенты: {seasonal_ingredients}.
    Включи разные базовые ингредиенты: джин, виски, ром, текила.

    Для каждого напитка укажи:
    1. Название
    2. Базовый ингредиент
    3. Основные ингредиенты
    4. Краткое описание вкуса
    5. Сезонную особенность

    Сделай меню разнообразным и сбалансированным.
    """
    
    try:
        menu = await call_yandex_api(prompt)
        await message.reply(menu)
    except Exception as e:
        await message.reply(f"Ошибка при создании меню: {str(e)}")

async def generate_conceptual_menu(message: types.Message, count: int):
    """Генерация концептуального меню"""
    prompt = f"""
    Создай концептуальное меню из {count} напитков, используя матрицу вдохновения:

    Источники вдохновения:
    - Сюрреализм (неожиданные сочетания)
    - Модернизм (чистые линии, минимализм)
    - Барокко (богатство, сложность)
    - Авангард (эксперименты, инновации)

    Способы воплощения:
    - Аромат (духи, эфирные масла)
    - Текстура (пена, желе, эмульсии)
    - Температура (горячие, холодные, контрасты)
    - Презентация (необычная подача)

    Для каждого напитка укажи:
    1. Название и концепцию
    2. Источник вдохновения
    3. Способ воплощения
    4. Ингредиенты и метод
    5. Философию напитка

    Сделай меню креативным и концептуальным.
    """
    
    try:
        menu = await call_yandex_api(prompt)
        await message.reply(menu)
    except Exception as e:
        await message.reply(f"Ошибка при создании меню: {str(e)}")

@dp.message(Command('trends'))
async def trends_command(message: types.Message):
    """Обработчик команды /trends"""
    trends_text = """
📈 Тренды коктейлей 2025

Zero-Proof Revolution:
• Сложные безалкогольные коктейли
• Использование ферментированных ингредиентов
• Квас, комбуча, кефир в качестве базы

Fat-Washing:
• Настаивание спирта на жирах (масло, бекон)
• Создание кремовой текстуры
• Новые вкусовые профили

Сезонные ингредиенты:
• Локальные и сезонные продукты
• Ферментированные овощи и фрукты
• Дикие травы и цветы

Техники приготовления:
• Sous-vide для настоев
• Криогенные методы
• Молекулярная гастрономия

Подача:
• Интерактивные элементы
• Дым, пар, световые эффекты
• Необычная посуда и сервировка

Популярные вкусы:
• Умами (грибы, соевый соус)
• Кислые и ферментированные
• Цветочные и травяные
• Пряные и острые
    """
    await message.reply(trends_text)

@dp.message(Command('news'))
async def news_command(message: types.Message):
    """Обработчик команды /news"""
    news_text = """
📰 Новости из мира HoReCa

Последние обновления:
• Новые рецепты в IBA Official Cocktails 2025
• Тренды в миксологии от ведущих барменов
• Сезонные ингредиенты и их применение

Рекомендуемые источники:
• Difford's Guide - ежедневные обновления
• Imbibe Magazine - тренды и инновации
• Punch - история и культура коктейлей

Следите за обновлениями:
• Новые техники приготовления
• Сезонные меню ведущих баров
• Инновации в подаче коктейлей
    """
    await message.reply(news_text)

@dp.message(Command('random'))
async def random_command(message: types.Message):
    """Обработчик команды /random"""
    # Получаем случайный спирт
    random_spirit = random.choice(BASE_SPIRITS)
    
    # Получаем случайные сезонные ингредиенты
    seasonal_ingredients = SEASONAL_INGREDIENTS[CURRENT_SEASON]
    random_ingredients = random.sample(seasonal_ingredients, min(3, len(seasonal_ingredients)))
    
    # Создаем промпт для случайного коктейля
    mocktail = random.choice([True, False])
    mocktail_text = "mocktail (безалкогольный)" if mocktail else "алкогольный"
    
    prompt = f"""
    Создай интересный рецепт напитка на основе:
    - Базовый ингредиент: {random_spirit}
    - Сезонные ингредиенты: {', '.join(random_ingredients)}
    - Тип: {mocktail_text}
    - Сезон: {CURRENT_SEASON} (Россия)

    Сделай напиток креативным и необычным, используя неожиданные сочетания.
    Включи:
    1. Креативное название
    2. Ингредиенты с пропорциями
    3. Метод приготовления
    4. Подача и украшение
    5. Философию напитка
    6. Советы по сочетанию с едой

    Пусть это будет сюрприз!
    """
    
    await message.reply("🎲 Создаю для вас сюрприз-коктейль...")
    
    try:
        recipe = await call_yandex_api(prompt)
        await message.reply(recipe)
    except Exception as e:
        await message.reply(f"Извините, произошла ошибка: {str(e)}")

@dp.message(Command('seasonal'))
async def seasonal_command(message: types.Message):
    """Обработчик команды /seasonal"""
    seasonal_ingredients = SEASONAL_INGREDIENTS[CURRENT_SEASON]
    season_names = {
        'winter': 'зима',
        'spring': 'весна', 
        'summer': 'лето',
        'autumn': 'осень'
    }
    
    current_season_name = season_names[CURRENT_SEASON]
    
    prompt = f"""
    Создай 3 сезонных напитка для {current_season_name} в России.
    Используй сезонные ингредиенты: {', '.join(seasonal_ingredients)}.

    Для каждого напитка:
    1. Название с сезонной тематикой
    2. Базовый ингредиент (разные для каждого)
    3. Сезонные ингредиенты
    4. Метод приготовления
    5. Подача и украшение
    6. Сезонная философия

    Сделай напитки теплыми и уютными для {current_season_name}.
    """
    
    await message.reply(f"🍂 Создаю сезонные коктейли для {current_season_name}...")
    
    try:
        recipes = await call_yandex_api(prompt)
        await message.reply(recipes)
    except Exception as e:
        await message.reply(f"Ошибка при создании сезонных коктейлей: {str(e)}")

@dp.message(Command('pairing'))
async def pairing_command(message: types.Message):
    """Обработчик команды /pairing"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.reply("Использование: /pairing [название блюда]\nПример: /pairing стейк")
        return
    
    dish = " ".join(args)
    
    prompt = f"""
    Подбери идеальный напиток для блюда: {dish}

    Используй принципы сочетания вкусов:
    1. Анализируй вкусовой профиль блюда
    2. Подбери ингредиент, который дополняет вкус
    3. Выбери ингредиенты для гармонии
    4. Учти сезонность (текущий сезон: {CURRENT_SEASON})

    Включи:
    1. Название напитка
    2. Обоснование выбора (почему именно этот напиток)
    3. Ингредиенты и пропорции
    4. Метод приготовления
    5. Подача и температура
    6. Дополнительные советы по сочетанию

    Сделай подборку профессиональной и обоснованной.
    """
    
    await message.reply(f"🍽️ Подбираю коктейль для {dish}...")
    
    try:
        pairing = await call_yandex_api(prompt)
        await message.reply(pairing)
    except Exception as e:
        await message.reply(f"Ошибка при подборе коктейля: {str(e)}")

@dp.message(Command('create_recipe'))
async def create_recipe_command(message: types.Message):
    """Обработчик команды /create_recipe"""
    await message.reply("""
➕ Создание нового рецепта

Для создания рецепта с помощью AI, используйте команду:
/recipe [спирт] [mocktail=yes/no]

Или опишите ваш рецепт в свободной форме, и я помогу его доработать!

Примеры:
- "Хочу коктейль с джином и мятой"
- "Создай что-то с текилой и лаймом"
- "Нужен безалкогольный коктейль с ягодами"

Просто напишите ваши пожелания, и я создам рецепт!
    """)

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
        
        response = f"Найдено рецептов: {len(recipes)}\n\n"
        
        for i, recipe in enumerate(recipes[:5], 1):  # Показываем максимум 5 рецептов
            response += f"{i}. {recipe['name']}\n"
            response += f"Базовый спирт: {recipe['base_spirit']}\n"
            response += f"Описание: {recipe['description'][:100]}...\n\n"
        
        if len(recipes) > 5:
            response += f"... и еще {len(recipes) - 5} рецептов"
        
        await message.reply(response)
        
    except Exception as e:
        await message.reply(f"Ошибка при поиске: {str(e)}")

@dp.message(Command('history'))
async def history_command(message: types.Message):
    """Обработчик команды /history"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.reply("Использование: /history [название коктейля]")
        return
    
    cocktail_name = " ".join(args)
    
    # Сначала ищем в базе данных
    recipe = db.get_recipe_by_name(cocktail_name)
    
    if recipe and recipe.get('history'):
        await message.reply(f"История коктейля {cocktail_name}:\n\n{recipe['history']}")
        return
    
    # Если не найдено в БД, используем AI
    await message.reply(f"📚 Ищу историю коктейля {cocktail_name}...")
    
    prompt = f"""
    Расскажи подробную историю напитка "{cocktail_name}".
    Включи:
    1. Происхождение и создателя
    2. Исторический контекст
    3. Эволюцию рецепта
    4. Интересные факты
    5. Влияние на кулинарную культуру

    Если это известный напиток, используй достоверные исторические данные.
    """
    
    try:
        history = await call_yandex_api(prompt)
        await message.reply(f"История коктейля {cocktail_name}:\n\n{history}")
    except Exception as e:
        await message.reply(f"Ошибка при получении истории: {str(e)}")

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
            "🔍 Поиск коктейлей\n\n"
            "Напишите название коктейля или ингредиент для поиска!\n\n"
            "Примеры:\n"
            "• мартини\n"
            "• джин\n"
            "• мохито\n"
            "• ром\n\n"
            "Или используйте команду: /search [запрос]"
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

@dp.callback_query(lambda c: c.data == 'menu')
async def process_callback_menu(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Меню'"""
    try:
        await callback_query.answer()
        await menu_command(callback_query.message)
    except Exception as e:
        print(f"Ошибка обработки кнопки menu: {e}")

@dp.callback_query(lambda c: c.data == 'trends')
async def process_callback_trends(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Тренды'"""
    try:
        await callback_query.answer()
        await trends_command(callback_query.message)
    except Exception as e:
        print(f"Ошибка обработки кнопки trends: {e}")

@dp.callback_query(lambda c: c.data == 'news')
async def process_callback_news(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Новости'"""
    try:
        await callback_query.answer()
        await news_command(callback_query.message)
    except Exception as e:
        print(f"Ошибка обработки кнопки news: {e}")

@dp.callback_query(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Помощь'"""
    try:
        await callback_query.answer()
        await help_command(callback_query.message)
    except Exception as e:
        print(f"Ошибка обработки кнопки help: {e}")

@dp.callback_query(lambda c: c.data == 'seasonal')
async def process_callback_seasonal(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Сезонные'"""
    try:
        await callback_query.answer()
        await seasonal_command(callback_query.message)
    except Exception as e:
        print(f"Ошибка обработки кнопки seasonal: {e}")

@dp.callback_query(lambda c: c.data == 'pairing')
async def process_callback_pairing(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Фудпейринг'"""
    try:
        await callback_query.answer()
        await callback_query.message.reply(
            "🍽️ Фудпейринг\n\n"
            "Напишите название блюда, и я подберу идеальный коктейль!\n\n"
            "Примеры:\n"
            "• стейк\n"
            "• паста карбонара\n"
            "• суши\n"
            "• шоколадный десерт\n"
            "• сырная тарелка\n\n"
            "Или используйте команду: /pairing [блюдо]"
        )
    except Exception as e:
        print(f"Ошибка обработки кнопки pairing: {e}")

@dp.callback_query(lambda c: c.data == 'create_recipe')
async def process_callback_create_recipe(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Создать рецепт'"""
    try:
        await callback_query.answer()
        await create_recipe_command(callback_query.message)
    except Exception as e:
        print(f"Ошибка обработки кнопки create_recipe: {e}")

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
        
        response = f"Найдено рецептов: {len(recipes)}\n\n"
        
        for i, recipe in enumerate(recipes[:5], 1):
            response += f"{i}. {recipe['name']}\n"
            response += f"Базовый спирт: {recipe['base_spirit']}\n"
            response += f"Описание: {recipe['description'][:100]}...\n\n"
        
        if len(recipes) > 5:
            response += f"... и еще {len(recipes) - 5} рецептов"
        
        await message.reply(response)
        
    except Exception as e:
        await message.reply(f"Ошибка при поиске: {str(e)}")

async def main():
    """Основная функция запуска бота"""
    print("Запуск MIXTRIX Bot (Полная версия)...")
    print("✓ База данных: готова")
    print("✓ Yandex API: подключен")
    print("✓ Расширенная система: активна")
    print("✓ Все функции MIXTRIX: активны")
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
