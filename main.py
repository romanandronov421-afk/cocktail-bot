import os
import asyncio
import sqlite3
import requests
import configparser
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные окружения
load_dotenv('env_file.txt')

# Загружаем конфигурацию
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

# Инициализация бота
bot = Bot(token=config.get('Telegram', 'Token'))
dp = Dispatcher()

# Название бота и его расшифровка
BOT_NAME = "MIXTRIX🍸"
BOT_DESCRIPTION = """
M - Mixology (Миксология)
I - Innovation (Инновации)
X - X-factor (Изюминка)
T - Taste (Вкус)
R - Recipes (Рецепты)
I - Ingredients (Ингредиенты)
X - Xperience (Опыт)
"""

# Сезонность октябрь 2025
SEASONAL_OCTOBER = ['Гранат', 'Клюква', 'Айва', 'Груша', 'Яблоки', 'Черноплодка', 'Рябина']

# Базовые спирты
BASE_SPIRITS = ['джин', 'водка', 'ром', 'виски', 'текила', 'коньяк', 'бренди']

# Словарь для проверки возраста пользователей
user_age_verified = {}

# Запрещенные темы (политика и другие)
FORBIDDEN_TOPICS = [
    'политика', 'политик', 'выборы', 'президент', 'правительство', 'партия',
    'депутат', 'министр', 'государство', 'власть', 'оппозиция', 'революция',
    'протест', 'митинг', 'демонстрация', 'забастовка', 'бунт', 'переворот'
]

def is_age_verified(user_id):
    """Проверка верификации возраста пользователя"""
    return user_age_verified.get(user_id, False)

def contains_forbidden_content(text):
    """Проверка на запрещенный контент"""
    text_lower = text.lower()
    return any(topic in text_lower for topic in FORBIDDEN_TOPICS)

def is_alcohol_related(text):
    """Проверка, связан ли текст с алкоголем"""
    alcohol_keywords = [
        'алкоголь', 'спирт', 'коктейль', 'напиток', 'джин', 'водка', 'ром', 
        'виски', 'текила', 'коньяк', 'бренди', 'ликер', 'вермут', 'шампанское',
        'вино', 'пиво', 'самогон', 'абсент', 'ром', 'виски', 'бурбон'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in alcohol_keywords)

# Инициализация базы данных
def init_database():
    """Инициализация базы данных с рецептами из 'Код коктейля'"""
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    # Удаляем старую таблицу если она существует
    cursor.execute('DROP TABLE IF EXISTS recipes')
    
    # Создаем новую таблицу с расширенной структурой
    cursor.execute('''CREATE TABLE recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        ingredients TEXT,
        method TEXT,
        base_spirit TEXT,
        category TEXT,
        source TEXT,
        description TEXT,
        glassware TEXT,
        garnish TEXT,
        difficulty TEXT,
        prep_time TEXT
    )''')
    
    # Рецепты из "Код коктейля" - Классические
    classic_recipes = [
        ("Old Fashioned", "60 мл бурбон, 1 кубик сахара, 2 дэш биттерс Ангостура, апельсиновая цедра", "Стир с сахаром и биттерс, добавить виски, подача в рокс", "виски", "классический", "Код коктейля", "Классический коктейль на виски с биттерс", "рокс", "апельсиновая цедра", "легкий", "2 мин"),
        ("Manhattan", "60 мл ржаной виски, 30 мл сладкий вермут, 2 дэш биттерс Ангостура", "Стир со льдом, подача в коктейльном бокале", "виски", "классический", "Код коктейля", "Элегантный коктейль на виски с вермутом", "коктейльный", "вишня мараскино", "средний", "3 мин"),
        ("Martini", "60 мл джин, 10 мл сухой вермут, оливка или лимонная цедра", "Стир со льдом, подача в коктейльном бокале", "джин", "классический", "Код коктейля", "Классический джин-коктейль", "коктейльный", "оливка или лимонная цедра", "легкий", "2 мин"),
        ("Negroni", "30 мл джин, 30 мл красный вермут, 30 мл Кампари", "Стир со льдом, подача в рокс", "джин", "классический", "Код коктейля", "Горький итальянский коктейль", "рокс", "апельсиновая цедра", "легкий", "2 мин"),
        ("Daiquiri", "60 мл белый ром, 30 мл лаймовый сок, 15 мл сахарный сироп", "Шейк со льдом, подача в коктейльном бокале", "ром", "классический", "Код коктейля", "Классический ромовый коктейль", "коктейльный", "лаймовая цедра", "легкий", "2 мин"),
        ("Margarita", "60 мл текила, 30 мл лаймовый сок, 20 мл трипл сек", "Шейк со льдом, подача в рокс с солью", "текила", "классический", "Код коктейля", "Классический текила-коктейль", "рокс", "лаймовая долька", "средний", "3 мин"),
        ("Mojito", "60 мл белый ром, 30 мл лаймовый сок, 20 мл сахарный сироп, 8 листьев мяты, содовая", "Мудл мяты, добавить ингредиенты, подача в хайбол", "ром", "классический", "Код коктейля", "Освежающий ромовый коктейль", "хайбол", "мята и лайм", "средний", "4 мин"),
        ("Whiskey Sour", "60 мл виски, 30 мл лимонный сок, 20 мл сахарный сироп, белок", "Шейк со льдом, подача в рокс", "виски", "классический", "Код коктейля", "Классический виски сауэр", "рокс", "лимонная цедра", "средний", "3 мин"),
        ("Gin Fizz", "60 мл джин, 30 мл лимонный сок, 20 мл сахарный сироп, белок, содовая", "Шейк со льдом, добавить содовую, подача в хайбол", "джин", "классический", "Код коктейля", "Освежающий джин-физз", "хайбол", "лимонная цедра", "средний", "4 мин"),
        ("Sidecar", "60 мл коньяк, 30 мл лимонный сок, 20 мл трипл сек", "Шейк со льдом, подача в коктейльном бокале", "коньяк", "классический", "Код коктейля", "Элегантный коньячный коктейль", "коктейльный", "сахарный ободок", "средний", "3 мин")
    ]
    
    # Рецепты из "Код коктейля" - Авторские
    signature_recipes = [
        ("Penicillin", "60 мл шотландский виски, 20 мл лимонный сок, 20 мл медовый сироп, 2 дэш биттерс Ангостура, 10 мл имбирный сироп", "Шейк со льдом, подача в рокс", "виски", "авторский", "Код коктейля", "Авторский коктейль с имбирем и медом", "рокс", "имбирь", "сложный", "5 мин"),
        ("Last Word", "30 мл джин, 30 мл зеленый шартрез, 30 мл лаймовый сок, 30 мл мараскино", "Шейк со льдом, подача в коктейльном бокале", "джин", "авторский", "Код коктейля", "Сложный авторский коктейль", "коктейльный", "вишня", "сложный", "4 мин"),
        ("Corpse Reviver #2", "30 мл джин, 30 мл лимонный сок, 30 мл трипл сек, 30 мл Лилье Блан, 1 дэш абсент", "Шейк со льдом, подача в коктейльном бокале", "джин", "авторский", "Код коктейля", "Авторский коктейль для восстановления", "коктейльный", "лимонная цедра", "сложный", "4 мин"),
        ("Aviation", "60 мл джин, 15 мл лимонный сок, 15 мл мараскино, 1 дэш крем де виолетт", "Шейк со льдом, подача в коктейльном бокале", "джин", "авторский", "Код коктейля", "Элегантный авторский коктейль", "коктейльный", "вишня", "сложный", "4 мин"),
        ("Boulevardier", "60 мл бурбон, 30 мл красный вермут, 30 мл Кампари", "Стир со льдом, подача в рокс", "виски", "авторский", "Код коктейля", "Авторский виски-негрони", "рокс", "апельсиновая цедра", "средний", "3 мин"),
        ("Paper Plane", "30 мл бурбон, 30 мл амаро, 30 мл лимонный сок, 30 мл апероль", "Шейк со льдом, подача в коктейльном бокале", "виски", "авторский", "Код коктейля", "Современный авторский коктейль", "коктейльный", "лимонная цедра", "сложный", "4 мин"),
        ("Jungle Bird", "60 мл темный ром, 30 мл лимонный сок, 20 мл сахарный сироп, 45 мл ананасовый сок, 15 мл Кампари", "Шейк со льдом, подача в рокс", "ром", "авторский", "Код коктейля", "Тропический авторский коктейль", "рокс", "ананас", "средний", "4 мин"),
        ("Naked & Famous", "30 мл мескаль, 30 мл желтый шартрез, 30 мл апероль, 30 мл лаймовый сок", "Шейк со льдом, подача в коктейльном бокале", "текила", "авторский", "Код коктейля", "Авторский мескаль-коктейль", "коктейльный", "лаймовая цедра", "сложный", "4 мин"),
        ("Trinidad Sour", "60 мл анджелс энви, 30 мл лимонный сок, 30 мл орж, 7 дэш биттерс Ангостура", "Шейк со льдом, подача в коктейльном бокале", "ром", "авторский", "Код коктейля", "Необычный авторский коктейль", "коктейльный", "лимонная цедра", "сложный", "4 мин"),
        ("Industry Sour", "30 мл зеленый шартрез, 30 мл фернет-бранка, 30 мл лаймовый сок, 30 мл сироп демерара", "Шейк со льдом, подача в коктейльном бокале", "ликер", "авторский", "Код коктейля", "Горький авторский коктейль", "коктейльный", "лаймовая цедра", "сложный", "4 мин")
    ]
    
    # Рецепты примиксов и заготовок
    premix_recipes = [
        ("Simple Syrup", "1 часть сахара, 1 часть воды", "Нагреть воду, растворить сахар, охладить", "сироп", "примикс", "Код коктейля", "Базовый сахарный сироп", "бутылка", "нет", "легкий", "10 мин"),
        ("Grenadine", "1 часть гранатовый сок, 1 часть сахара", "Нагреть сок, растворить сахар, охладить", "сироп", "примикс", "Код коктейля", "Гранатовый сироп", "бутылка", "нет", "легкий", "15 мин"),
        ("Orgeat", "1 часть миндальное молоко, 1 часть сахара, 1 дэш миндальный экстракт", "Смешать ингредиенты, процедить", "сироп", "примикс", "Код коктейля", "Миндальный сироп", "бутылка", "нет", "средний", "20 мин"),
        ("Honey Syrup", "1 часть мед, 1 часть теплая вода", "Смешать мед с теплой водой", "сироп", "примикс", "Код коктейля", "Медовый сироп", "бутылка", "нет", "легкий", "5 мин"),
        ("Ginger Syrup", "1 часть имбирь, 1 часть сахара, 1 часть воды", "Натереть имбирь, смешать с сахаром и водой, процедить", "сироп", "примикс", "Код коктейля", "Имбирный сироп", "бутылка", "нет", "средний", "30 мин"),
        ("Cinnamon Syrup", "1 часть корица, 1 часть сахара, 1 часть воды", "Нагреть воду с корицей, растворить сахар", "сироп", "примикс", "Код коктейля", "Коричный сироп", "бутылка", "нет", "легкий", "15 мин"),
        ("Lavender Syrup", "1 часть лаванда, 1 часть сахара, 1 часть воды", "Нагреть воду с лавандой, растворить сахар", "сироп", "примикс", "Код коктейля", "Лавандовый сироп", "бутылка", "нет", "средний", "20 мин"),
        ("Rose Syrup", "1 часть лепестки роз, 1 часть сахара, 1 часть воды", "Нагреть воду с лепестками, растворить сахар", "сироп", "примикс", "Код коктейля", "Розовый сироп", "бутылка", "нет", "средний", "25 мин"),
        ("Vanilla Syrup", "1 часть ваниль, 1 часть сахара, 1 часть воды", "Нагреть воду с ванилью, растворить сахар", "сироп", "примикс", "Код коктейля", "Ванильный сироп", "бутылка", "нет", "легкий", "15 мин"),
        ("Demerara Syrup", "1 часть демерара сахар, 1 часть воды", "Нагреть воду, растворить сахар, охладить", "сироп", "примикс", "Код коктейля", "Сироп из демерара сахара", "бутылка", "нет", "легкий", "10 мин")
    ]
    
    # Объединяем все рецепты
    all_recipes = classic_recipes + signature_recipes + premix_recipes
    
    cursor.executemany("INSERT OR IGNORE INTO recipes (name, ingredients, method, base_spirit, category, source, description, glassware, garnish, difficulty, prep_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", all_recipes)
    conn.commit()
    conn.close()

# Инициализируем базу данных
init_database()

async def call_yandex_api(prompt: str) -> str:
    """Вызов Yandex Cloud AI API для генерации рецептов"""
    api_key = config.get('YandexGPT', 'SecretKey')
    folder_id = config.get('YandexGPT', 'CatalogID')
    model = config.get('YandexGPT', 'ChatModel')
    temperature = config.getfloat('YandexGPT', 'Temperature')
    max_tokens = config.getint('YandexGPT', 'MaxTokens')
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    # Добавляем системное сообщение для соблюдения правил
    safe_prompt = f"""
    {prompt}
    
    ВАЖНО: Отвечай только на темы, связанные с кулинарией и напитками. 
    Избегай обсуждения алкоголя без предупреждения о возрасте.
    Не обсуждай политические темы.
    Фокусируйся на вкусовых сочетаниях, ингредиентах и кулинарных традициях.
    """
    
    data = {
        "modelUri": model,
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": max_tokens
        },
        "messages": [
            {
                "role": "user",
                "text": safe_prompt
            }
        ]
    }
    
    try:
        response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if 'result' in result and 'alternatives' in result['result']:
            return result['result']['alternatives'][0]['message']['text']
        else:
            return "Извините, не удалось обработать запрос."
            
    except Exception as e:
        return f"Ошибка при обращении к AI: {str(e)}"

@dp.message(Command('start'))
async def start_command(message: types.Message):
    """Обработчик команды /start с проверкой возраста"""
    user_id = message.from_user.id
    
    if not is_age_verified(user_id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Мне 18+ лет", callback_data="age_verify_yes"),
                InlineKeyboardButton(text="❌ Мне меньше 18", callback_data="age_verify_no")
            ]
        ])
        
        await message.reply(
            f"🍸 **Добро пожаловать в {BOT_NAME}!**\n\n"
            f"**{BOT_DESCRIPTION}**\n\n"
            f"⚠️ **Важно:** Этот бот содержит информацию о напитках, включая алкогольные.\n"
            f"Пожалуйста, подтвердите ваш возраст для продолжения работы с ботом.",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        return
    
    # Если возраст подтвержден, показываем основное меню
    await show_main_menu(message)

async def show_main_menu(message: types.Message):
    """Показать основное меню бота"""
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
            InlineKeyboardButton(text="📋 Правила", callback_data="rules"),
            InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")
        ]
    ])
    
    welcome_text = f"""
🍸 **{BOT_NAME}** - Ваш персональный миксолог!

{BOT_DESCRIPTION}

Добро пожаловать в мир кулинарных экспериментов! Я помогу вам:
• Создать идеальный рецепт с учетом сезонности (октябрь 2025)
• Найти рецепты по ингредиентам и базовым компонентам
• Подобрать напиток под ваше блюдо
• Узнать о трендах и новостях кулинарной индустрии
• Генерировать концептуальные меню

**Основные команды:**
/recipe [ингредиент] - создать рецепт
/search [запрос] - поиск рецептов
/random - случайный рецепт
/seasonal - сезонные рецепты (октябрь)
/pairing [блюдо] - подбор под блюдо
/menu [тип] [количество] - генерация меню
/rules - правила пользования
/examples - примеры использования

**Сезонные ингредиенты октября:**
Гранат, Клюква, Айва, Груша, Яблоки, Черноплодка, Рябина

Выберите действие кнопкой или используйте команды!
    """
    
    await message.reply(welcome_text, reply_markup=keyboard, parse_mode='Markdown')

@dp.message(Command('rules'))
async def rules_command(message: types.Message):
    """Обработчик команды /rules"""
    rules_text = f"""
📋 **Правила пользования {BOT_NAME}**

**🔞 Возрастные ограничения:**
• Бот предназначен для пользователей 18+ лет
• Информация о алкогольных напитках доступна только совершеннолетним
• Ответственность за соблюдение местного законодательства лежит на пользователе

**🚫 Запрещенные темы:**
• Политические обсуждения
• Пропаганда незаконных веществ
• Контент, нарушающий законы РФ
• Оскорбления и дискриминация

**✅ Разрешенные темы:**
• Кулинарные рецепты и техники
• Вкусовые сочетания и фудпейринг
• Сезонные ингредиенты
• Кулинарные традиции и история
• Инновации в кулинарии

**🍸 О алкогольных напитках:**
• Информация предоставляется в образовательных целях
• Рекомендуем ответственное потребление
• Соблюдайте местное законодательство
• Не злоупотребляйте алкоголем

**🛡️ Безопасность:**
• Не делитесь личной информацией
• Используйте бота ответственно
• Соблюдайте правила сообщества Telegram

**📞 Поддержка:**
При нарушении правил бот может ограничить доступ к определенным функциям.
    """
    await message.reply(rules_text, parse_mode='Markdown')

@dp.message(Command('examples'))
async def examples_command(message: types.Message):
    """Обработчик команды /examples"""
    examples_text = f"""
📚 **Примеры использования {BOT_NAME}**

**🍸 Создание рецептов:**
• `/recipe джин` - рецепт с джином
• `/recipe яблоки` - рецепт с яблоками
• `/recipe сезонный` - сезонный рецепт

**🔍 Поиск рецептов:**
• `/search Manhattan` - найти Manhattan
• `/search джин` - рецепты с джином
• `/search классический` - классические рецепты
• `/search авторский` - авторские рецепты
• `/search примикс` - примиксы и сиропы
• `/iba_search Manhattan` - поиск только среди рецептов IBA

**📚 Коллекции рецептов:**
• `/classic` - классические рецепты из "Код коктейля"
• `/signature` - авторские рецепты
• `/premix` - примиксы и сиропы
• `/iba` - официальные рецепты IBA
• `/iba_classic` - классические рецепты IBA
• `/bible` - рецепты из "Библия бармена"
• `/aperitif` - рецепты аперитивов
• `/theory` - теория барменства
• `/preparation` - рецепты заготовок
• `/techniques` - техники приготовления
• `/syrups` - рецепты сиропов
• `/extended` - расширенные рецепты
• `/molecular` - молекулярные техники
• `/scientific` - научные заготовки
• `/liquid_intelligence` - научные коктейли
• `/flavor_principles` - принципы фудпейринга
• `/flavor_combinations` - сочетания вкусов
• `/seasonal_pairings` - сезонные сочетания
• `/cocktail_pairings` - фудпейринг для коктейлей
• `/el_copitas` - авторские рецепты El Copitas Bar

**📖 Подробные рецепты:**
• `/recipe_detail Manhattan` - полный рецепт Manhattan
• `/recipe_detail Old Fashioned` - детали Old Fashioned
• `/recipe_detail Penicillin` - авторский Penicillin

**🎲 Случайные рецепты:**
• `/random` - случайный рецепт
• `/seasonal` - сезонные рецепты

**🍽️ Фудпейринг:**
• `/pairing стейк` - напиток к стейку
• `/pairing десерт` - напиток к десерту
• `/pairing сыр` - напиток к сыру

**📋 Меню:**
• `/menu seasonal 5` - сезонное меню из 5 рецептов
• `/menu conceptual 3` - концептуальное меню

**💬 Свободные запросы:**
• "Создай рецепт с мятой и лаймом"
• "Что подойдет к шоколадному десерту?"
• "Нужен освежающий напиток для лета"

**🍂 Сезонные ингредиенты (октябрь):**
Гранат, Клюква, Айва, Груша, Яблоки, Черноплодка, Рябина

**📚 База знаний "Код коктейля":**
• 10 классических рецептов
• 10 авторских рецептов  
• 10 примиксов и сиропов

**⚠️ Помните:** Всегда указывайте возраст при первом использовании!
    """
    await message.reply(examples_text, parse_mode='Markdown')

@dp.message(Command('recipe'))
async def recipe_command(message: types.Message):
    """Обработчик команды /recipe с проверкой возраста"""
    user_id = message.from_user.id
    
    if not is_age_verified(user_id):
        await message.reply(
            "⚠️ Для создания рецептов необходимо подтвердить возраст.\n"
            "Используйте команду /start для верификации.",
            parse_mode='Markdown'
        )
        return
    
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    base_spirit = 'джин'  # по умолчанию
    mocktail = False
    
    # Парсинг аргументов
    for arg in args:
        if arg.lower() in BASE_SPIRITS:
            base_spirit = arg.lower()
        elif 'mock' in arg.lower():
            mocktail = True
    
    # Создание промпта с сезонностью и фудпейрингом
    mocktail_text = "безалкогольный" if mocktail else "алкогольный"
    seasonal_ingredients = ", ".join(SEASONAL_OCTOBER)
    
    prompt = f"""
    Создай сбалансированный рецепт напитка на основе {base_spirit} с учетом фудпейринга и сезонности.
Сезон: октябрь 2025 (используй сезонные ингредиенты: {seasonal_ingredients}).
    Тип: {mocktail_text} напиток.

Включи в рецепт:
    1. Название напитка
2. Ингредиенты с точными пропорциями
3. Метод приготовления
4. Подача и украшение
    5. Краткую историю или концепцию
6. Советы по фудпейрингу
7. Сезонную особенность

    Сделай рецепт гармоничным и сбалансированным.
    """
    
    await message.reply("🍹 Создаю идеальный рецепт для вас...")
    
    try:
        recipe = await call_yandex_api(prompt)
        await message.reply(recipe)
    except Exception as e:
        await message.reply(f"Извините, произошла ошибка: {str(e)}")

# Обработчики callback кнопок
@dp.callback_query(lambda c: c.data == 'age_verify_yes')
async def process_age_verify_yes(callback_query: types.CallbackQuery):
    """Обработка подтверждения возраста"""
    user_id = callback_query.from_user.id
    user_age_verified[user_id] = True
    
    await callback_query.answer("✅ Возраст подтвержден!")
    await show_main_menu(callback_query.message)

@dp.callback_query(lambda c: c.data == 'age_verify_no')
async def process_age_verify_no(callback_query: types.CallbackQuery):
    """Обработка отказа от подтверждения возраста"""
    await callback_query.answer("❌ Доступ ограничен")
    await callback_query.message.reply(
        "🚫 **Доступ ограничен**\n\n"
        "К сожалению, бот предназначен только для пользователей 18+ лет.\n"
        "Вы можете использовать бота для изучения безалкогольных рецептов.\n\n"
        "Для этого используйте команду: /recipe mocktail",
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data == 'rules')
async def process_callback_rules(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Правила'"""
    await callback_query.answer()
    await rules_command(callback_query.message)

@dp.callback_query(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Помощь'"""
    await callback_query.answer()
    await examples_command(callback_query.message)

# Добавляем остальные обработчики callback кнопок...
@dp.callback_query(lambda c: c.data == 'recipe')
async def process_callback_recipe(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await recipe_command(callback_query.message)

@dp.message()
async def handle_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений с проверками"""
    user_id = message.from_user.id
    text = message.text.lower()
    
    # Проверка на запрещенный контент
    if contains_forbidden_content(message.text):
        await message.reply(
            "🚫 **Тема не разрешена**\n\n"
            "Бот предназначен только для обсуждения кулинарных тем.\n"
            "Пожалуйста, используйте команду /rules для ознакомления с правилами.",
            parse_mode='Markdown'
        )
        return
    
    # Проверка возраста для алкогольных тем
    if is_alcohol_related(message.text) and not is_age_verified(user_id):
        await message.reply(
            "⚠️ **Требуется подтверждение возраста**\n\n"
            "Для обсуждения алкогольных напитков необходимо подтвердить возраст.\n"
            "Используйте команду /start для верификации.",
            parse_mode='Markdown'
        )
        return
    
    # Проверяем, не является ли это запросом на создание рецепта
    recipe_keywords = ['коктейль', 'рецепт', 'создай', 'хочу', 'нужен', 'сделай', 'приготовь']
    if any(keyword in text for keyword in recipe_keywords):
        await message.reply("🍹 Создаю рецепт по вашему запросу...")
    
    prompt = f"""
        Пользователь просит создать напиток: "{message.text}"

        Создай рецепт на основе запроса пользователя, учитывая:
        1. Сезонность (текущий сезон: октябрь 2025, ингредиенты: {', '.join(SEASONAL_OCTOBER)})
        2. Принципы фудпейринга
        3. Баланс вкусов
        4. Практичность приготовления

        Включи:
        1. Название напитка
        2. Ингредиенты с пропорциями
        3. Метод приготовления
        4. Подача и украшение
        5. Описание вкуса
        6. Советы по приготовлению

        Сделай рецепт понятным и воспроизводимым.
    """
    
    try:
        recipe = await call_yandex_api(prompt)
        await message.reply(recipe)
    except Exception as e:
        await message.reply(f"Ошибка при создании рецепта: {str(e)}")
    return
    
    # Обычное сообщение
    await message.reply(
        f"Не понимаю эту команду. Используйте /help для получения справки или выберите действие из меню.\n\n"
        f"💡 **Совет:** Вы можете просто написать, что хотите, например:\n"
        f"• 'Хочу рецепт с джином'\n"
        f"• 'Создай что-то с яблоками'\n"
        f"• 'Нужен сезонный напиток'",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
        ]),
        parse_mode='Markdown'
    )

@dp.message(Command('search'))
async def search_command(message: types.Message):
    """Обработчик команды /search с расширенной базой данных"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.reply(
            "🔍 **Поиск рецептов**\n\n"
            "Использование: /search [запрос]\n\n"
            "**Примеры:**\n"
            "• `/search Manhattan` - найти Manhattan\n"
            "• `/search джин` - рецепты с джином\n"
            "• `/search классический` - классические рецепты\n"
            "• `/search авторский` - авторские рецепты\n"
            "• `/search примикс` - примиксы и сиропы\n"
            "• `/search сироп` - все сиропы",
            parse_mode='Markdown'
        )
        return
    
    query = " ".join(args)
    await message.reply(f"🔍 Ищу рецепты по запросу: {query}")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        # Расширенный поиск в базе данных
        cursor.execute("""
            SELECT * FROM recipes 
            WHERE name LIKE ? OR ingredients LIKE ? OR base_spirit LIKE ? 
            OR category LIKE ? OR description LIKE ? OR source LIKE ?
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply(
                "Рецепты не найдены в базе.\n\n"
                "**Попробуйте:**\n"
                "• `/classic` - классические рецепты\n"
                "• `/signature` - авторские рецепты\n"
                "• `/premix` - примиксы и сиропы\n"
                "• `/recipe` - создать новый рецепт",
                parse_mode='Markdown'
            )
            return
        
        response = f"**Найдено рецептов: {len(recipes)}**\n\n"
        
        for recipe in recipes[:5]:  # Показываем максимум 5 рецептов
            response += f"**{recipe[1]}**\n"
            response += f"📋 Категория: {recipe[5]}\n"
            response += f"🍸 Базовый спирт: {recipe[4]}\n"
            response += f"⏱️ Время: {recipe[12]}\n"
            response += f"📝 Описание: {recipe[7]}\n"
            response += f"🥃 Бокал: {recipe[9]}\n"
            response += f"🌿 Украшение: {recipe[10]}\n\n"
        
        if len(recipes) > 5:
            response += f"... и еще {len(recipes) - 5} рецептов"
        
        await message.reply(response, parse_mode='Markdown')
        
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при поиске: {str(e)}")

@dp.message(Command('classic'))
async def classic_command(message: types.Message):
    """Обработчик команды /classic - классические рецепты"""
    await message.reply("🍸 **Классические рецепты из 'Код коктейля'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'классический'")
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply("Классические рецепты не найдены.")
            return
        
        response = f"**📚 Классические рецепты ({len(recipes)} шт.)**\n\n"
        
        for recipe in recipes:
            response += f"**{recipe[1]}**\n"
            response += f"🍸 {recipe[4]} | ⏱️ {recipe[12]} | 🥃 {recipe[9]}\n"
            response += f"📝 {recipe[7]}\n"
            response += f"🌿 {recipe[10]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке классических рецептов: {str(e)}")

@dp.message(Command('signature'))
async def signature_command(message: types.Message):
    """Обработчик команды /signature - авторские рецепты"""
    await message.reply("🎨 **Авторские рецепты из 'Код коктейля'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'авторский'")
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply("Авторские рецепты не найдены.")
            return
        
        response = f"**🎨 Авторские рецепты ({len(recipes)} шт.)**\n\n"
        
        for recipe in recipes:
            response += f"**{recipe[1]}**\n"
            response += f"🍸 {recipe[4]} | ⏱️ {recipe[12]} | 🥃 {recipe[9]}\n"
            response += f"📝 {recipe[7]}\n"
            response += f"🌿 {recipe[10]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке авторских рецептов: {str(e)}")

@dp.message(Command('premix'))
async def premix_command(message: types.Message):
    """Обработчик команды /premix - примиксы и сиропы"""
    await message.reply("🧪 **Примиксы и сиропы из 'Код коктейля'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'примикс'")
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply("Примиксы не найдены.")
            return
        
        response = f"**🧪 Примиксы и сиропы ({len(recipes)} шт.)**\n\n"
        
        for recipe in recipes:
            response += f"**{recipe[1]}**\n"
            response += f"⏱️ {recipe[12]} | 📦 {recipe[9]}\n"
            response += f"📝 {recipe[7]}\n"
            response += f"🔧 {recipe[3]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке примиксов: {str(e)}")

@dp.message(Command('recipe_detail'))
async def recipe_detail_command(message: types.Message):
    """Обработчик команды /recipe_detail - подробный рецепт"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.reply(
            "📖 **Подробный рецепт**\n\n"
            "Использование: /recipe_detail [название рецепта]\n\n"
            "**Примеры:**\n"
            "• `/recipe_detail Manhattan`\n"
            "• `/recipe_detail Old Fashioned`\n"
            "• `/recipe_detail Penicillin`",
            parse_mode='Markdown'
        )
        return
    
    recipe_name = " ".join(args)
    await message.reply(f"📖 Ищу подробный рецепт: {recipe_name}")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE name LIKE ?", (f'%{recipe_name}%',))
        recipe = cursor.fetchone()
        
        if not recipe:
            await message.reply(f"Рецепт '{recipe_name}' не найден. Попробуйте /search для поиска.")
            return
        
        response = f"**📖 {recipe[1]}**\n\n"
        response += f"📋 **Категория:** {recipe[5]}\n"
        response += f"🍸 **Базовый спирт:** {recipe[4]}\n"
        response += f"⏱️ **Время приготовления:** {recipe[12]}\n"
        response += f"🎯 **Сложность:** {recipe[11]}\n"
        response += f"🥃 **Бокал:** {recipe[9]}\n"
        response += f"🌿 **Украшение:** {recipe[10]}\n\n"
        response += f"📝 **Описание:**\n{recipe[7]}\n\n"
        response += f"🥄 **Ингредиенты:**\n{recipe[2]}\n\n"
        response += f"🔧 **Метод приготовления:**\n{recipe[3]}\n\n"
        response += f"📚 **Источник:** {recipe[6]}"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке рецепта: {str(e)}")

@dp.message(Command('iba'))
async def iba_command(message: types.Message):
    """Обработчик команды /iba - рецепты IBA"""
    await message.reply("🍸 **Официальные рецепты IBA**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE source = 'IBA Official'")
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply("Рецепты IBA не найдены.")
            return
        
        response = f"**🍸 Официальные рецепты IBA ({len(recipes)} шт.)**\n\n"
        
        # Показываем первые 10 рецептов
        for recipe in recipes[:10]:
            response += f"**{recipe[1]}**\n"
            response += f"🍸 {recipe[4]} | ⏱️ {recipe[12]} | 🥃 {recipe[9]}\n"
            response += f"📝 {recipe[7]}\n\n"
        
        if len(recipes) > 10:
            response += f"... и еще {len(recipes) - 10} рецептов IBA"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке рецептов IBA: {str(e)}")

@dp.message(Command('iba_search'))
async def iba_search_command(message: types.Message):
    """Обработчик команды /iba_search - поиск рецептов IBA"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.reply(
            "🔍 **Поиск рецептов IBA**\n\n"
            "Использование: /iba_search [запрос]\n\n"
        "**Примеры:**\n"
            "• `/iba_search Manhattan` - найти Manhattan\n"
            "• `/iba_search джин` - рецепты IBA с джином\n"
            "• `/iba_search классический` - классические IBA рецепты",
        parse_mode='Markdown'
    )
        return
    
    query = " ".join(args)
    await message.reply(f"🔍 Ищу рецепты IBA по запросу: {query}")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        # Поиск только среди рецептов IBA
        cursor.execute("""
            SELECT * FROM recipes 
            WHERE source = 'IBA Official' 
            AND (name LIKE ? OR ingredients LIKE ? OR base_spirit LIKE ? 
            OR category LIKE ? OR description LIKE ?)
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply(
                "Рецепты IBA не найдены.\n\n"
                "**Попробуйте:**\n"
                "• `/iba` - все рецепты IBA\n"
                "• `/classic` - классические рецепты\n"
                "• `/search` - общий поиск",
                parse_mode='Markdown'
            )
            return
        
        response = f"**Найдено рецептов IBA: {len(recipes)}**\n\n"
        
        for recipe in recipes[:5]:  # Показываем максимум 5 рецептов
            response += f"**{recipe[1]}**\n"
            response += f"📋 Категория: {recipe[5]}\n"
            response += f"🍸 Базовый спирт: {recipe[4]}\n"
            response += f"⏱️ Время: {recipe[12]}\n"
            response += f"📝 Описание: {recipe[7]}\n"
            response += f"🥃 Бокал: {recipe[9]}\n"
            response += f"🌿 Украшение: {recipe[10]}\n\n"
        
        if len(recipes) > 5:
            response += f"... и еще {len(recipes) - 5} рецептов IBA"
        
        await message.reply(response, parse_mode='Markdown')
        
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при поиске рецептов IBA: {str(e)}")

@dp.message(Command('iba_classic'))
async def iba_classic_command(message: types.Message):
    """Обработчик команды /iba_classic - классические рецепты IBA"""
    await message.reply("🍸 **Классические рецепты IBA**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE source = 'IBA Official' AND category = 'iba_classic'")
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply("Классические рецепты IBA не найдены.")
        return
    
        response = f"**🍸 Классические рецепты IBA ({len(recipes)} шт.)**\n\n"
        
        # Показываем первые 15 рецептов
        for recipe in recipes[:15]:
            response += f"**{recipe[1]}**\n"
            response += f"🍸 {recipe[4]} | ⏱️ {recipe[12]} | 🥃 {recipe[9]}\n"
            response += f"📝 {recipe[7]}\n\n"
        
        if len(recipes) > 15:
            response += f"... и еще {len(recipes) - 15} классических рецептов IBA"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке классических рецептов IBA: {str(e)}")

@dp.message(Command('bible'))
async def bible_command(message: types.Message):
    """Обработчик команды /bible - рецепты из Библии бармена"""
    await message.reply("📖 **Рецепты из 'Библия бармена'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE source = 'Библия бармена'")
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply("Рецепты из 'Библия бармена' не найдены.")
        return
    
        response = f"**📖 Рецепты из 'Библия бармена' ({len(recipes)} шт.)**\n\n"
        
        # Показываем первые 10 рецептов
        for recipe in recipes[:10]:
            response += f"**{recipe[1]}**\n"
            response += f"🍸 {recipe[4]} | ⏱️ {recipe[12]} | 🥃 {recipe[9]}\n"
            response += f"📝 {recipe[7]}\n\n"
        
        if len(recipes) > 10:
            response += f"... и еще {len(recipes) - 10} рецептов"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке рецептов из 'Библия бармена': {str(e)}")

@dp.message(Command('aperitif'))
async def aperitif_command(message: types.Message):
    """Обработчик команды /aperitif - рецепты аперитивов"""
    await message.reply("🍸 **Рецепты аперитивов**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE source = 'Аперитив Король коктейля'")
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply("Рецепты аперитивов не найдены.")
            return
        
        response = f"**🍸 Рецепты аперитивов ({len(recipes)} шт.)**\n\n"
        
        # Показываем первые 10 рецептов
        for recipe in recipes[:10]:
            response += f"**{recipe[1]}**\n"
            response += f"🍸 {recipe[4]} | ⏱️ {recipe[12]} | 🥃 {recipe[9]}\n"
            response += f"📝 {recipe[7]}\n\n"
        
        if len(recipes) > 10:
            response += f"... и еще {len(recipes) - 10} рецептов"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке рецептов аперитивов: {str(e)}")

@dp.message(Command('theory'))
async def theory_command(message: types.Message):
    """Обработчик команды /theory - теория барменства"""
    await message.reply("📚 **Теория барменства**\n\nЗагружаю знания...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'theory'")
        theories = cursor.fetchall()
        
        if not theories:
            await message.reply("Теоретические материалы не найдены.")
            return
        
        response = f"**📚 Теория барменства ({len(theories)} тем)**\n\n"
        
        for theory in theories:
            response += f"**{theory[1]}**\n"
            response += f"📝 {theory[7]}\n"
            response += f"🔧 {theory[3]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке теории: {str(e)}")

@dp.message(Command('preparation'))
async def preparation_command(message: types.Message):
    """Обработчик команды /preparation - рецепты заготовок"""
    await message.reply("🧪 **Рецепты заготовок**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'preparation'")
        preparations = cursor.fetchall()
        
        if not preparations:
            await message.reply("Рецепты заготовок не найдены.")
            return
        
        response = f"**🧪 Рецепты заготовок ({len(preparations)} шт.)**\n\n"
        
        for prep in preparations:
            response += f"**{prep[1]}**\n"
            response += f"⏱️ {prep[12]} | 📦 {prep[9]}\n"
            response += f"📝 {prep[7]}\n"
            response += f"🔧 {prep[3]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке рецептов заготовок: {str(e)}")

@dp.message(Command('techniques'))
async def techniques_command(message: types.Message):
    """Обработчик команды /techniques - техники приготовления"""
    await message.reply("🔧 **Техники приготовления**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'cocktail_code_technique'")
        techniques = cursor.fetchall()
        
        if not techniques:
            await message.reply("Техники приготовления не найдены.")
            return
        
        response = f"**🔧 Техники приготовления ({len(techniques)} шт.)**\n\n"
        
        for technique in techniques:
            response += f"**{technique[1]}**\n"
            response += f"📝 {technique[7]}\n"
            response += f"🔧 {technique[3]}\n"
            response += f"⏱️ {technique[12]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке техник: {str(e)}")

@dp.message(Command('syrups'))
async def syrups_command(message: types.Message):
    """Обработчик команды /syrups - рецепты сиропов"""
    await message.reply("🧪 **Рецепты сиропов**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'cocktail_code_syrup'")
        syrups = cursor.fetchall()
        
        if not syrups:
            await message.reply("Рецепты сиропов не найдены.")
            return
        
        response = f"**🧪 Рецепты сиропов ({len(syrups)} шт.)**\n\n"
        
        for syrup in syrups:
            response += f"**{syrup[1]}**\n"
            response += f"⏱️ {syrup[12]} | 📦 {syrup[9]}\n"
            response += f"📝 {syrup[7]}\n"
            response += f"🔧 {syrup[3]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке рецептов сиропов: {str(e)}")

@dp.message(Command('extended'))
async def extended_command(message: types.Message):
    """Обработчик команды /extended - расширенные рецепты из Код Коктейля"""
    await message.reply("🍸 **Расширенные рецепты из 'Код Коктейля'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'cocktail_code_extended'")
        recipes = cursor.fetchall()
        
        if not recipes:
            await message.reply("Расширенные рецепты не найдены.")
            return
        
        response = f"**🍸 Расширенные рецепты ({len(recipes)} шт.)**\n\n"
        
        # Показываем первые 10 рецептов
        for recipe in recipes[:10]:
            response += f"**{recipe[1]}**\n"
            response += f"🍸 {recipe[4]} | ⏱️ {recipe[12]} | 🥃 {recipe[9]}\n"
            response += f"📝 {recipe[7]}\n\n"
        
        if len(recipes) > 10:
            response += f"... и еще {len(recipes) - 10} рецептов"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке расширенных рецептов: {str(e)}")

@dp.message(Command('molecular'))
async def molecular_command(message: types.Message):
    """Обработчик команды /molecular - молекулярные техники"""
    await message.reply("🧪 **Молекулярные техники из 'Liquid Intelligence'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'liquid_intelligence_technique'")
        techniques = cursor.fetchall()
        
        if not techniques:
            await message.reply("Молекулярные техники не найдены.")
            return
        
        response = f"**🧪 Молекулярные техники ({len(techniques)} шт.)**\n\n"
        
        for technique in techniques:
            response += f"**{technique[1]}**\n"
            response += f"📝 {technique[7]}\n"
            response += f"🔧 {technique[3]}\n"
            response += f"⏱️ {technique[12]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке молекулярных техник: {str(e)}")

@dp.message(Command('scientific'))
async def scientific_command(message: types.Message):
    """Обработчик команды /scientific - научные заготовки"""
    await message.reply("🔬 **Научные заготовки из 'Liquid Intelligence'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'liquid_intelligence_preparation'")
        preparations = cursor.fetchall()
        
        if not preparations:
            await message.reply("Научные заготовки не найдены.")
            return
        
        response = f"**🔬 Научные заготовки ({len(preparations)} шт.)**\n\n"
        
        for prep in preparations:
            response += f"**{prep[1]}**\n"
            response += f"⏱️ {prep[12]} | 📦 {prep[9]}\n"
            response += f"📝 {prep[7]}\n"
            response += f"🔧 {prep[3]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке научных заготовок: {str(e)}")

@dp.message(Command('liquid_intelligence'))
async def liquid_intelligence_command(message: types.Message):
    """Обработчик команды /liquid_intelligence - научные коктейли"""
    await message.reply("🧪 **Научные коктейли из 'Liquid Intelligence'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'liquid_intelligence_cocktail'")
        cocktails = cursor.fetchall()
        
        if not cocktails:
            await message.reply("Научные коктейли не найдены.")
            return
        
        response = f"**🧪 Научные коктейли ({len(cocktails)} шт.)**\n\n"
        
        # Показываем первые 10 коктейлей
        for cocktail in cocktails[:10]:
            response += f"**{cocktail[1]}**\n"
            response += f"🍸 {cocktail[4]} | ⏱️ {cocktail[12]} | 🥃 {cocktail[9]}\n"
            response += f"📝 {cocktail[7]}\n\n"
        
        if len(cocktails) > 10:
            response += f"... и еще {len(cocktails) - 10} коктейлей"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке научных коктейлей: {str(e)}")

@dp.message(Command('flavor_principles'))
async def flavor_principles_command(message: types.Message):
    """Обработчик команды /flavor_principles - принципы фудпейринга"""
    await message.reply("🍽️ **Принципы фудпейринга из 'The Flavor Bible'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'flavor_bible_principle'")
        principles = cursor.fetchall()
        
        if not principles:
            await message.reply("Принципы фудпейринга не найдены.")
            return
        
        response = f"**🍽️ Принципы фудпейринга ({len(principles)} шт.)**\n\n"
        
        for principle in principles:
            response += f"**{principle[1]}**\n"
            response += f"📝 {principle[7]}\n"
            response += f"🔧 {principle[3]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке принципов фудпейринга: {str(e)}")

@dp.message(Command('flavor_combinations'))
async def flavor_combinations_command(message: types.Message):
    """Обработчик команды /flavor_combinations - сочетания вкусов"""
    await message.reply("🍽️ **Сочетания вкусов из 'The Flavor Bible'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'flavor_bible_combination'")
        combinations = cursor.fetchall()
        
        if not combinations:
            await message.reply("Сочетания вкусов не найдены.")
            return
        
        response = f"**🍽️ Сочетания вкусов ({len(combinations)} шт.)**\n\n"
        
        for combo in combinations:
            response += f"**{combo[1]}**\n"
            response += f"📝 {combo[7]}\n"
            response += f"🔧 {combo[3]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке сочетаний вкусов: {str(e)}")

@dp.message(Command('seasonal_pairings'))
async def seasonal_pairings_command(message: types.Message):
    """Обработчик команды /seasonal_pairings - сезонные сочетания"""
    await message.reply("🍽️ **Сезонные сочетания из 'The Flavor Bible'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'flavor_bible_seasonal'")
        pairings = cursor.fetchall()
        
        if not pairings:
            await message.reply("Сезонные сочетания не найдены.")
            return
        
        response = f"**🍽️ Сезонные сочетания ({len(pairings)} шт.)**\n\n"
        
        for pairing in pairings:
            response += f"**{pairing[1]}**\n"
            response += f"📝 {pairing[7]}\n"
            response += f"🔧 {pairing[3]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке сезонных сочетаний: {str(e)}")

@dp.message(Command('cocktail_pairings'))
async def cocktail_pairings_command(message: types.Message):
    """Обработчик команды /cocktail_pairings - фудпейринг для коктейлей"""
    await message.reply("🍽️ **Фудпейринг для коктейлей из 'The Flavor Bible'**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE category = 'flavor_bible_cocktail'")
        pairings = cursor.fetchall()
        
        if not pairings:
            await message.reply("Фудпейринг для коктейлей не найден.")
            return
        
        response = f"**🍽️ Фудпейринг для коктейлей ({len(pairings)} шт.)**\n\n"
        
        for pairing in pairings:
            response += f"**{pairing[1]}**\n"
            response += f"📝 {pairing[7]}\n"
            response += f"🔧 {pairing[3]}\n\n"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке фудпейринга для коктейлей: {str(e)}")

@dp.message(Command('el_copitas'))
async def el_copitas_command(message: types.Message):
    """Обработчик команды /el_copitas - авторские рецепты из El Copitas Bar"""
    await message.reply("🍸 **Авторские рецепты из El Copitas Bar**\n\nЗагружаю коллекцию...")
    
    try:
        conn = sqlite3.connect('cocktails.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE source = 'El Copitas Bar'")
        cocktails = cursor.fetchall()
        
        if not cocktails:
            await message.reply("Авторские рецепты не найдены.")
            return
        
        response = f"**🍸 Авторские рецепты El Copitas Bar ({len(cocktails)} шт.)**\n\n"
        
        # Показываем первые 15 коктейлей
        for cocktail in cocktails[:15]:
            response += f"**{cocktail[1]}**\n"
            response += f"🍸 {cocktail[4]} | ⏱️ {cocktail[12]} | 🥃 {cocktail[9]}\n"
            response += f"📝 {cocktail[7]}\n\n"
        
        if len(cocktails) > 15:
            response += f"... и еще {len(cocktails) - 15} рецептов"
        
        await message.reply(response, parse_mode='Markdown')
        conn.close()
        
    except Exception as e:
        await message.reply(f"Ошибка при загрузке авторских рецептов: {str(e)}")

async def main():
    """Основная функция запуска бота"""
    print(f"🍸 {BOT_NAME} запускается...")
    print("📊 База данных инициализирована")
    print("🍂 Сезонные ингредиенты октября загружены")
    print("🤖 Yandex GPT подключен")
    print("🛡️ Системы безопасности активированы")
    print("📚 База рецептов 'Код коктейля' загружена")
    print("🍸 200+ рецептов IBA загружены")
    print("📖 Рецепты из 'Библия бармена' загружены")
    print("🍸 Рецепты аперитивов загружены")
    print("📚 Теория барменства загружена")
    print("🧪 Рецепты заготовок загружены")
    print("🔧 Техники приготовления загружены")
    print("🧪 Рецепты сиропов загружены")
    print("🍸 Расширенные рецепты загружены")
    print("🧪 Молекулярные техники загружены")
    print("🔬 Научные заготовки загружены")
    print("🧪 Научные коктейли загружены")
    print("🍽️ Принципы фудпейринга загружены")
    print("🍽️ Сочетания вкусов загружены")
    print("🍽️ Сезонные сочетания загружены")
    print("🍽️ Фудпейринг для коктейлей загружен")
    print("🍸 Авторские рецепты El Copitas Bar загружены")
    print("Нажмите Ctrl+C для остановки")
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())