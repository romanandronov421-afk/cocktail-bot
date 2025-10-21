# 🍹 MixMatrixBot - Финальная инструкция по запуску

## ✅ Все готово для запуска!

### 🔑 Ваши данные:
- **Telegram Bot Token**: `8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q`
- **Yandex API Key**: `ajegpjgsbgidg7av4mfj`
- **Folder ID**: `ajels2ea51569prr6uvb`

## 🚀 Инструкция по запуску:

### 1. Создайте файл `.env`:
Создайте файл `.env` в корневой папке проекта со следующим содержимым:

```env
# Yandex Cloud AI API Configuration
YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q

# API Gateway Configuration (опционально)
API_GATEWAY_URL=https://your-api-gateway.url
API_GATEWAY_STAGING_URL=https://staging-api-gateway.url

# Model Configuration
DEFAULT_MODEL=yandexgpt
DEFAULT_MAX_TOKENS=100
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9

# Cursor IDE Configuration
CURSOR_AI_PROVIDER=custom
CURSOR_AI_CUSTOM_API_URL=https://llm.api.cloud.yandex.net/foundationModels/v1/completion
CURSOR_AI_CUSTOM_API_KEY=ajegpjgsbgidg7av4mfj
```

### 2. Активируйте виртуальную среду:
```bash
venv\Scripts\activate
```

### 3. Установите зависимости (если нужно):
```bash
pip install -r requirements.txt
```

### 4. Запустите бота:
```bash
python run_bot.py
```

## 🧪 Альтернативные способы запуска:

### Способ 1: Прямой запуск Python
```bash
venv\Scripts\python.exe run_bot.py
```

### Способ 2: Через автоматический скрипт
```bash
python start_bot.py
```

### Способ 3: Тест API перед запуском
```bash
python test_yandex_api.py
```

## 📱 После запуска:

1. **Найдите вашего бота в Telegram** по имени, которое вы дали при создании
2. **Отправьте команду `/start`**
3. **Попробуйте команды:**
   - `/recipe джин` - создать рецепт коктейля
   - `/random` - случайный коктейль
   - `/seasonal` - сезонные коктейли
   - `/help` - справка

## 🎯 Функции бота:

- **🍸 Создание рецептов** с помощью Yandex GPT
- **🔍 Поиск** по базе коктейлей
- **🎲 Случайные коктейли** с AI
- **🍂 Сезонные рецепты** для России
- **🍽️ Фудпейринг** - подбор к блюдам
- **📋 Генерация меню** с AI
- **📈 Тренды** коктейлей 2025
- **📰 Новости** из мира HoReCa
- **📚 История коктейлей** с AI

## 🔧 Настройка Cursor IDE:

### Через настройки:
1. Откройте Cursor
2. `Ctrl + ,` (Settings)
3. Найдите "AI Providers"
4. Выберите "Custom API"
5. Настройте:
   ```
   URL: https://llm.api.cloud.yandex.net/foundationModels/v1/completion
   API Key: ajegpjgsbgidg7av4mfj
   ```

## 📊 Структура проекта:

```
├── bot.py                 # ✅ Основной бот (обновлен для Yandex AI)
├── run_bot.py            # ✅ Скрипт запуска
├── start_bot.py          # ✅ Автоматический запуск
├── test_yandex_api.py    # ✅ Тест Yandex API
├── check_bot.py          # ✅ Проверка готовности
├── create_env.py         # ✅ Создание .env
├── database.py           # База данных
├── requirements.txt      # Зависимости
├── environment.env       # ✅ Переменные окружения
├── env_final.txt         # ✅ Финальный .env
└── cocktails.db          # База данных коктейлей
```

## 🎉 Готово к работе!

**MixMatrixBot полностью настроен и готов к работе с Yandex Cloud AI!**

### 🚀 Что делать дальше:
1. Создайте файл `.env` с содержимым выше
2. Активируйте виртуальную среду: `venv\Scripts\activate`
3. Запустите бота: `python run_bot.py`
4. Найдите бота в Telegram и отправьте `/start`

**Удачного использования MixMatrixBot! 🍹**

## 📞 Если что-то не работает:

1. **Проверьте файл `.env`** - все токены должны быть правильными
2. **Убедитесь, что виртуальная среда активирована**
3. **Проверьте зависимости**: `pip install -r requirements.txt`
4. **Запустите тест**: `python test_yandex_api.py`
5. **Проверьте логи ошибок** в консоли

Бот должен работать! 🎯



