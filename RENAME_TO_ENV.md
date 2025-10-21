# ✅ Файл готов! Переименуйте его в .env

## 🎯 Что нужно сделать:

### Способ 1: В проводнике Windows
1. Найдите файл `dot_env_file` в папке проекта
2. Щелкните правой кнопкой мыши на файле
3. Выберите "Переименовать"
4. Измените имя на `.env` (с точкой в начале)
5. Нажмите Enter

### Способ 2: В VS Code/Cursor
1. Найдите файл `dot_env_file` в панели файлов
2. Щелкните правой кнопкой мыши на файле
3. Выберите "Rename"
4. Измените имя на `.env`
5. Нажмите Enter

### Способ 3: Через командную строку (если работает)
```bash
ren dot_env_file .env
```

## 📋 Содержимое файла:

Файл `dot_env_file` содержит все необходимые настройки:

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

## 🚀 После переименования в .env:

### 1. Активируйте виртуальную среду:
```bash
venv\Scripts\activate
```

### 2. Запустите бота:
```bash
python run_bot.py
```

### 3. Найдите бота в Telegram:
- Найдите вашего бота по имени
- Отправьте команду `/start`
- Попробуйте команды: `/recipe джин`, `/random`, `/seasonal`

## 🎉 Готово!

После переименования файла в `.env` ваш MixMatrixBot будет готов к работе с Yandex Cloud AI!

### 📱 Команды бота:
- `/start` - начать работу
- `/recipe [спирт]` - создать рецепт с AI
- `/random` - случайный коктейль
- `/seasonal` - сезонные коктейли
- `/pairing [блюдо]` - подбор к блюду
- `/help` - справка

**Удачного использования MixMatrixBot! 🍹**



