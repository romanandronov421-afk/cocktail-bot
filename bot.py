import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
from database import CocktailDatabase

# Загружаем переменные окружения
load_dotenv()

# Инициализация бота
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher(bot)

# Инициализация базы данных
db = CocktailDatabase()

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

# XAI API конфигурация
XAI_API_KEY = os.getenv('XAI_API_KEY')
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

async def call_xai_api(prompt: str) -> str:
    """Вызов XAI API для генерации рецептов"""
    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "grok-beta",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(XAI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка при обращении к AI: {str(e)}"

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🍸 Создать рецепт", callback_data="recipe"),
        InlineKeyboardButton("🔍 Поиск", callback_data="search"),
        InlineKeyboardButton("🎲 Случайный", callback_data="random"),
        InlineKeyboardButton("📋 Меню", callback_data="menu"),
        InlineKeyboardButton("🍂 Сезонные", callback_data="seasonal"),
        InlineKeyboardButton("🍽️ Фудпейринг", callback_data="pairing"),
        InlineKeyboardButton("📈 Тренды", callback_data="trends"),
        InlineKeyboardButton("📰 Новости", callback_data="news"),
        InlineKeyboardButton("➕ Создать рецепт", callback_data="create_recipe"),
        InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
    )
    
    welcome_text = """
🍹 **MixMatrixBot** - Ваш персональный бармен!

Добро пожаловать в мир коктейлей! Я помогу вам:
• Создать идеальный рецепт на основе фудпейринга
• Найти коктейли по ингредиентам и сезону
• Подобрать коктейль под ваше блюдо
• Узнать о трендах и новостях индустрии

**Основные команды:**
/recipe - создать рецепт
/search - поиск коктейлей
/random - случайный коктейль
/seasonal - сезонные коктейли
/pairing - подбор под блюдо
/create_recipe - создать новый рецепт

Выберите действие кнопкой или используйте команды!
    """
    
    await message.reply(welcome_text, reply_markup=keyboard, parse_mode='Markdown')

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
🍹 **MixMatrixBot - Справка**

**Основные команды:**
/start - начать работу с ботом
/help - показать эту справку

**Создание и поиск:**
/recipe [спирт] [mocktail=yes/no] - создать рецепт
/search [запрос] - поиск коктейлей
/random - случайный коктейль
/create_recipe - создать новый рецепт с AI

**Сезонные и специальные:**
/seasonal - сезонные коктейли для России
/pairing [блюдо] - подбор коктейля под блюдо
/menu [тип] [количество] - генерация меню

**Информация:**
/trends - тренды коктейлей 2025
/news - новости из мира HoReCa
/history [коктейль] - история коктейля

**Доступные спирты:**
джин, водка, ром, виски, текила, коньяк, бренди

**Сезонность (Россия):**
• Зима: клюква, брусника, цитрусы, корица
• Весна: ревень, щавель, молодые травы
• Лето: ягоды, базилик, укроп
• Осень: яблоки, груши, тыква, мед

**Особенности:**
• Фудпейринг на основе The Flavor Bible
• Сезонные ингредиенты для России
• AI-генерация рецептов
• Концептуальные меню с матрицей вдохновения
    """
    await message.reply(help_text, parse_mode='Markdown')

@dp.message_handler(commands=['recipe'])
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
    seasonal_ingredients = ", ".join(SEASONAL_INGREDIENTS['october'])
    
    prompt = f"""
Создай сбалансированный рецепт коктейля на основе {base_spirit} с учетом фудпейринга из The Flavor Bible.
Сезон: октябрь 2025 (используй сезонные ингредиенты: {seasonal_ingredients}).
Тип: {mocktail_text} коктейль.

Включи в рецепт:
1. Название коктейля
2. Ингредиенты с точными пропорциями
3. Метод приготовления
4. Подача и украшение
5. Краткую историю или концепцию
6. Советы по фудпейрингу

Сделай рецепт гармоничным и сбалансированным, используя принципы The Flavor Bible.
    """
    
    await message.reply("🍹 Создаю идеальный рецепт для вас...")
    
    try:
        recipe = await call_xai_api(prompt)
        await message.reply(recipe)
    except Exception as e:
        await message.reply(f"Извините, произошла ошибка: {str(e)}")

@dp.message_handler(commands=['menu'])
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
    seasonal_ingredients = ", ".join(SEASONAL_INGREDIENTS['october'])
    
    prompt = f"""
Создай сезонное меню из {count} коктейлей для октября 2025.
Используй сезонные ингредиенты: {seasonal_ingredients}.
Включи разные базовые спирты: джин, виски, ром, текила.

Для каждого коктейля укажи:
1. Название
2. Базовый спирт
3. Основные ингредиенты
4. Краткое описание вкуса
5. Сезонную особенность

Сделай меню разнообразным и сбалансированным.
    """
    
    try:
        menu = await call_xai_api(prompt)
        await message.reply(menu)
    except Exception as e:
        await message.reply(f"Ошибка при создании меню: {str(e)}")

async def generate_conceptual_menu(message: types.Message, count: int):
    """Генерация концептуального меню"""
    prompt = f"""
Создай концептуальное меню из {count} коктейлей, используя матрицу вдохновения:

**Источники вдохновения:**
- Сюрреализм (неожиданные сочетания)
- Модернизм (чистые линии, минимализм)
- Барокко (богатство, сложность)
- Авангард (эксперименты, инновации)

**Способы воплощения:**
- Аромат (духи, эфирные масла)
- Текстура (пена, желе, эмульсии)
- Температура (горячие, холодные, контрасты)
- Презентация (необычная подача)

Для каждого коктейля укажи:
1. Название и концепцию
2. Источник вдохновения
3. Способ воплощения
4. Ингредиенты и метод
5. Философию коктейля

Сделай меню креативным и концептуальным.
    """
    
    try:
        menu = await call_xai_api(prompt)
        await message.reply(menu)
    except Exception as e:
        await message.reply(f"Ошибка при создании меню: {str(e)}")

@dp.message_handler(commands=['trends'])
async def trends_command(message: types.Message):
    """Обработчик команды /trends"""
    trends_text = """
📈 **Тренды коктейлей 2025**

**Zero-Proof Revolution:**
• Сложные безалкогольные коктейли
• Использование ферментированных ингредиентов
• Квас, комбуча, кефир в качестве базы

**Fat-Washing:**
• Настаивание спирта на жирах (масло, бекон)
• Создание кремовой текстуры
• Новые вкусовые профили

**Сезонные ингредиенты:**
• Локальные и сезонные продукты
• Ферментированные овощи и фрукты
• Дикие травы и цветы

**Техники приготовления:**
• Sous-vide для настоев
• Криогенные методы
• Молекулярная гастрономия

**Подача:**
• Интерактивные элементы
• Дым, пар, световые эффекты
• Необычная посуда и сервировка

**Популярные вкусы:**
• Умами (грибы, соевый соус)
• Кислые и ферментированные
• Цветочные и травяные
• Пряные и острые
    """
    await message.reply(trends_text, parse_mode='Markdown')

@dp.message_handler(commands=['news'])
async def news_command(message: types.Message):
    """Обработчик команды /news"""
    news_text = """
📰 **Новости из мира HoReCa**

**Последние обновления:**
• Новые рецепты в IBA Official Cocktails 2025
• Тренды в миксологии от ведущих барменов
• Сезонные ингредиенты и их применение

**Рекомендуемые источники:**
• Difford's Guide - ежедневные обновления
• Imbibe Magazine - тренды и инновации
• Punch - история и культура коктейлей

**Следите за обновлениями:**
• Новые техники приготовления
• Сезонные меню ведущих баров
• Инновации в подаче коктейлей
    """
    await message.reply(news_text, parse_mode='Markdown')

@dp.message_handler(commands=['random'])
async def random_command(message: types.Message):
    """Обработчик команды /random"""
    import random
    
    # Получаем случайный спирт
    random_spirit = random.choice(BASE_SPIRITS)
    
    # Получаем случайные сезонные ингредиенты
    seasonal_ingredients = SEASONAL_INGREDIENTS[CURRENT_SEASON]
    random_ingredients = random.sample(seasonal_ingredients, min(3, len(seasonal_ingredients)))
    
    # Создаем промпт для случайного коктейля
    mocktail = random.choice([True, False])
    mocktail_text = "mocktail (безалкогольный)" if mocktail else "алкогольный"
    
    prompt = f"""
Создай неожиданный и интересный рецепт коктейля на основе:
- Базовый спирт: {random_spirit}
- Сезонные ингредиенты: {', '.join(random_ingredients)}
- Тип: {mocktail_text}
- Сезон: {CURRENT_SEASON} (Россия)

Сделай коктейль креативным и необычным, используя неожиданные сочетания.
Включи:
1. Креативное название
2. Ингредиенты с пропорциями
3. Метод приготовления
4. Подача и украшение
5. Философию коктейля
6. Советы по фудпейрингу

Пусть это будет сюрприз!
    """
    
    await message.reply("🎲 Создаю для вас сюрприз-коктейль...")
    
    try:
        recipe = await call_xai_api(prompt)
        await message.reply(recipe)
    except Exception as e:
        await message.reply(f"Извините, произошла ошибка: {str(e)}")

@dp.message_handler(commands=['seasonal'])
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
Создай 3 сезонных коктейля для {current_season_name} в России.
Используй сезонные ингредиенты: {', '.join(seasonal_ingredients)}.

Для каждого коктейля:
1. Название с сезонной тематикой
2. Базовый спирт (разные для каждого)
3. Сезонные ингредиенты
4. Метод приготовления
5. Подача и украшение
6. Сезонная философия

Сделай коктейли теплыми и уютными для {current_season_name}.
    """
    
    await message.reply(f"🍂 Создаю сезонные коктейли для {current_season_name}...")
    
    try:
        recipes = await call_xai_api(prompt)
        await message.reply(recipes)
    except Exception as e:
        await message.reply(f"Ошибка при создании сезонных коктейлей: {str(e)}")

@dp.message_handler(commands=['pairing'])
async def pairing_command(message: types.Message):
    """Обработчик команды /pairing"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.reply("Использование: /pairing [название блюда]\nПример: /pairing стейк")
        return
    
    dish = " ".join(args)
    
    prompt = f"""
Подбери идеальный коктейль для блюда: {dish}

Используй принципы фудпейринга из The Flavor Bible:
1. Анализируй вкусовой профиль блюда
2. Подбери спирт, который дополняет вкус
3. Выбери ингредиенты для гармонии
4. Учти сезонность (текущий сезон: {CURRENT_SEASON})

Включи:
1. Название коктейля
2. Обоснование выбора (почему именно этот коктейль)
3. Ингредиенты и пропорции
4. Метод приготовления
5. Подача и температура
6. Дополнительные советы по сочетанию

Сделай подборку профессиональной и обоснованной.
    """
    
    await message.reply(f"🍽️ Подбираю коктейль для {dish}...")
    
    try:
        pairing = await call_xai_api(prompt)
        await message.reply(pairing)
    except Exception as e:
        await message.reply(f"Ошибка при подборе коктейля: {str(e)}")

@dp.message_handler(commands=['create_recipe'])
async def create_recipe_command(message: types.Message):
    """Обработчик команды /create_recipe"""
    await message.reply("""
➕ **Создание нового рецепта**

Для создания рецепта с помощью AI, используйте команду:
/recipe [спирт] [mocktail=yes/no]

Или опишите ваш рецепт в свободной форме, и я помогу его доработать!

**Примеры:**
- "Хочу коктейль с джином и мятой"
- "Создай что-то с текилой и лаймом"
- "Нужен безалкогольный коктейль с ягодами"

Просто напишите ваши пожелания, и я создам рецепт!
    """, parse_mode='Markdown')

@dp.message_handler(commands=['search'])
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
            response += f"Описание: {recipe['description'][:100]}...\n\n"
        
        if len(recipes) > 5:
            response += f"... и еще {len(recipes) - 5} рецептов"
        
        await message.reply(response, parse_mode='Markdown')
        
    except Exception as e:
        await message.reply(f"Ошибка при поиске: {str(e)}")

@dp.message_handler(commands=['history'])
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
        await message.reply(f"**История коктейля {cocktail_name}:**\n\n{recipe['history']}", parse_mode='Markdown')
        return
    
    # Если не найдено в БД, используем AI
    await message.reply(f"📚 Ищу историю коктейля {cocktail_name}...")
    
    prompt = f"""
Расскажи подробную историю коктейля "{cocktail_name}".
Включи:
1. Происхождение и создателя
2. Исторический контекст
3. Эволюцию рецепта
4. Интересные факты
5. Влияние на коктейльную культуру

Если это известный коктейль, используй достоверные исторические данные.
    """
    
    try:
        history = await call_xai_api(prompt)
        await message.reply(f"**История коктейля {cocktail_name}:**\n\n{history}", parse_mode='Markdown')
    except Exception as e:
        await message.reply(f"Ошибка при получении истории: {str(e)}")

@dp.callback_query_handler(lambda c: c.data == 'recipe')
async def process_callback_recipe(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Рецепт'"""
    await callback_query.answer()
    await recipe_command(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'menu')
async def process_callback_menu(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Меню'"""
    await callback_query.answer()
    await menu_command(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'trends')
async def process_callback_trends(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Тренды'"""
    await callback_query.answer()
    await trends_command(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'news')
async def process_callback_news(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Новости'"""
    await callback_query.answer()
    await news_command(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Помощь'"""
    await callback_query.answer()
    await help_command(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'random')
async def process_callback_random(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Случайный'"""
    await callback_query.answer()
    await random_command(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'seasonal')
async def process_callback_seasonal(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Сезонные'"""
    await callback_query.answer()
    await seasonal_command(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'pairing')
async def process_callback_pairing(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Фудпейринг'"""
    await callback_query.answer()
    await callback_query.message.reply(
        "🍽️ **Фудпейринг**\n\n"
        "Напишите название блюда, и я подберу идеальный коктейль!\n\n"
        "**Примеры:**\n"
        "• стейк\n"
        "• паста карбонара\n"
        "• суши\n"
        "• шоколадный десерт\n"
        "• сырная тарелка\n\n"
        "Или используйте команду: /pairing [блюдо]",
        parse_mode='Markdown'
    )

@dp.callback_query_handler(lambda c: c.data == 'create_recipe')
async def process_callback_create_recipe(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Создать рецепт'"""
    await callback_query.answer()
    await create_recipe_command(callback_query.message)

@dp.message_handler()
async def handle_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    text = message.text.lower()
    
    # Проверяем, не является ли это запросом на создание рецепта
    recipe_keywords = ['коктейль', 'рецепт', 'создай', 'хочу', 'нужен', 'сделай', 'приготовь']
    if any(keyword in text for keyword in recipe_keywords):
        await message.reply("🍹 Создаю рецепт по вашему запросу...")
        
        prompt = f"""
Пользователь просит создать коктейль: "{message.text}"

Создай рецепт на основе запроса пользователя, учитывая:
1. Сезонность (текущий сезон: {CURRENT_SEASON})
2. Принципы фудпейринга
3. Баланс вкусов
4. Практичность приготовления

Включи:
1. Название коктейля
2. Ингредиенты с пропорциями
3. Метод приготовления
4. Подача и украшение
5. Описание вкуса
6. Советы по приготовлению

Сделай рецепт понятным и воспроизводимым.
        """
        
        try:
            recipe = await call_xai_api(prompt)
            await message.reply(recipe)
        except Exception as e:
            await message.reply(f"Ошибка при создании рецепта: {str(e)}")
        return
    
    # Проверяем, не является ли это запросом на фудпейринг
    pairing_keywords = ['блюдо', 'еда', 'подойдет', 'сочетается', 'к еде', 'к блюду']
    if any(keyword in text for keyword in pairing_keywords):
        await message.reply("🍽️ Подбираю коктейль под ваше блюдо...")
        
        prompt = f"""
Пользователь просит подобрать коктейль к блюду: "{message.text}"

Используй принципы фудпейринга из The Flavor Bible:
1. Анализируй вкусовой профиль блюда
2. Подбери спирт, который дополняет вкус
3. Выбери ингредиенты для гармонии
4. Учти сезонность (текущий сезон: {CURRENT_SEASON})

Включи:
1. Название коктейля
2. Обоснование выбора
3. Ингредиенты и пропорции
4. Метод приготовления
5. Подача и температура
6. Дополнительные советы по сочетанию
        """
        
        try:
            pairing = await call_xai_api(prompt)
            await message.reply(pairing)
        except Exception as e:
            await message.reply(f"Ошибка при подборе коктейля: {str(e)}")
        return
    
    # Обычное сообщение
    await message.reply(
        "Не понимаю эту команду. Используйте /help для получения справки или выберите действие из меню выше.\n\n"
        "💡 **Совет:** Вы можете просто написать, что хотите, например:\n"
        "• 'Хочу коктейль с джином'\n"
        "• 'Подбери коктейль к стейку'\n"
        "• 'Создай что-то с ягодами'",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
        ),
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    print("🍹 MixMatrixBot запускается...")
    print("Нажмите Ctrl+C для остановки")
    executor.start_polling(dp, skip_updates=True)
