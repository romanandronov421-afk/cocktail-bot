#!/usr/bin/env python3
"""
MIXTRIX Bot - Исправленная версия без эмодзи
"""

import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# Настройка логирования без эмодзи
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mixtrix.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv('env_file.txt')

# Проверка переменных окружения
if not os.getenv('TELEGRAM_BOT_TOKEN'):
    logger.error("TELEGRAM_BOT_TOKEN не найден в переменных окружения")
    exit(1)

if not os.getenv('YANDEX_API_KEY'):
    logger.error("YANDEX_API_KEY не найден в переменных окружения")
    exit(1)

if not os.getenv('FOLDER_ID'):
    logger.error("FOLDER_ID не найден в переменных окружения")
    exit(1)

logger.info("Переменные окружения загружены успешно")

# Инициализация компонентов
try:
    from database import CocktailDatabase
    from hybrid_processor import HybridCocktailProcessor
    from cocktail_party_processor import CocktailPartyProcessor
    
    db = CocktailDatabase()
    hybrid_processor = HybridCocktailProcessor()
    party_processor = CocktailPartyProcessor()
    
    logger.info("Все компоненты инициализированы успешно")
except Exception as e:
    logger.error(f"Ошибка инициализации компонентов: {e}")
    exit(1)

# Сезонные ингредиенты для России
SEASONAL_INGREDIENTS = {
    'winter': ['клюква', 'брусника', 'облепиха', 'цитрусы', 'корица', 'гвоздика', 'мускатный орех', 'ваниль'],
    'spring': ['ревень', 'щавель', 'молодые травы', 'цветы сирени', 'черемуха', 'мелисса', 'мята'],
    'summer': ['клубника', 'малина', 'смородина', 'крыжовник', 'вишня', 'базилик', 'укроп', 'петрушка'],
    'autumn': ['яблоки', 'груши', 'сливы', 'тыква', 'калина', 'рябина', 'орехи', 'мед']
}

CURRENT_SEASON = 'autumn'
BASE_SPIRITS = ['джин', 'водка', 'ром', 'виски', 'текила', 'коньяк', 'бренди']

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
        import requests
        response = requests.post(YANDEX_API_URL, headers=headers, json=data, timeout=30)
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

# Создание бота и диспетчера
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()

# Обработчики команд
@dp.message(Command('start'))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Создать рецепт", callback_data="recipe"),
            InlineKeyboardButton(text="Поиск", callback_data="search")
        ],
        [
            InlineKeyboardButton(text="Случайный", callback_data="random"),
            InlineKeyboardButton(text="Меню", callback_data="menu")
        ],
        [
            InlineKeyboardButton(text="Сезонные", callback_data="seasonal"),
            InlineKeyboardButton(text="Фудпейринг", callback_data="pairing")
        ],
        [
            InlineKeyboardButton(text="Тренды", callback_data="trends"),
            InlineKeyboardButton(text="Новости", callback_data="news")
        ],
        [
            InlineKeyboardButton(text="Создать рецепт", callback_data="create_recipe"),
            InlineKeyboardButton(text="Помощь", callback_data="help")
        ]
    ])
    
    welcome_text = """
MixMatrixBot - Ваш персональный бармен!

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

Выберите действие кнопкой или используйте команды!
    """
    
    await message.reply(welcome_text, reply_markup=keyboard)

@dp.message(Command('help'))
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
MixMatrixBot - Справка

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

@dp.message(Command('search'))
async def search_command(message: types.Message):
    """Обработчик команды /search"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.reply("Поиск коктейлей\n\nВведите название коктейля или ингредиент для поиска.\n\nПримеры:\n• Мартини\n• джин\n• текила\n• безалкогольный")
        return
    
    query = ' '.join(args)
    await message.reply(f"Ищу рецепты по запросу: {query}")
    
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
        logger.error(f"Ошибка поиска: {e}")
        await message.reply(f"Ошибка при поиске: {str(e)}")

# Обработчики callback кнопок
@dp.callback_query(lambda c: c.data == 'recipe')
async def process_callback_recipe(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Рецепт'"""
    await callback_query.answer()
    await recipe_command(callback_query.message)

@dp.callback_query(lambda c: c.data == 'search')
async def process_callback_search(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Поиск'"""
    await callback_query.answer()
    await callback_query.message.reply("Поиск коктейлей\n\nВведите название коктейля или ингредиент для поиска.\n\nПримеры:\n• Мартини\n• джин\n• текила\n• безалкогольный")

@dp.callback_query(lambda c: c.data == 'random')
async def process_callback_random(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Случайный'"""
    await callback_query.answer()
    await callback_query.message.reply("Случайный коктейль\n\nСоздаю для вас сюрприз-коктейль...")
    
    import random
    random_spirit = random.choice(['джин', 'водка', 'ром', 'виски', 'текила', 'коньяк'])
    seasonal_ingredients = ['яблоки', 'груши', 'тыква', 'мед', 'орехи']
    random_ingredients = random.sample(seasonal_ingredients, min(3, len(seasonal_ingredients)))
    
    prompt = f"""
Создай неожиданный и интересный рецепт коктейля на основе:
- Базовый спирт: {random_spirit}
- Сезонные ингредиенты: {', '.join(random_ingredients)}
- Сезон: осень (Россия)

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
    
    try:
        recipe = await call_yandex_api(prompt)
        await callback_query.message.reply(recipe)
    except Exception as e:
        logger.error(f"Ошибка создания случайного рецепта: {e}")
        await callback_query.message.reply(f"Извините, произошла ошибка: {str(e)}")

@dp.callback_query(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Помощь'"""
    await callback_query.answer()
    await help_command(callback_query.message)

# Обработчик текстовых сообщений
@dp.message()
async def handle_text_message(message: types.Message):
    """Обработчик текстовых сообщений"""
    try:
        response = await party_processor.process_request(message.text, message.from_user.id)
        await message.reply(response)
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await message.reply("Извините, произошла ошибка при обработке вашего запроса.")

async def main():
    """Основная функция"""
    try:
        logger.info("Запуск MIXTRIX Bot...")
        logger.info("База данных: готова")
        logger.info("Yandex API: подключен")
        logger.info("Гибридная система: активна")
        logger.info("Функции MIXTRIX: активны")
        logger.info("Бот готов к работе!")
        
        # Проверяем подключение к Telegram API
        bot_info = await bot.get_me()
        logger.info(f"Бот подключен: @{bot_info.username} ({bot_info.first_name})")
        
        # Запускаем polling
        await dp.start_polling(
            bot, 
            skip_updates=True,
            timeout=30,
            request_timeout=30,
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
        
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        logger.info("Попробуйте перезапустить бота через несколько секунд")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        logger.info("До свидания!")











