# 🚀 СОЗДАНИЕ ФАЙЛА .ENV ВРУЧНУЮ

## ❗ ПРОБЛЕМА С ТЕРМИНАЛОМ
Терминал PowerShell не работает корректно. Вам нужно создать файл .env вручную.

## 📝 ИНСТРУКЦИЯ ПО СОЗДАНИЮ ФАЙЛА .ENV

### ШАГ 1: Создайте новый файл
1. Откройте проводник Windows
2. Перейдите в папку проекта: `C:\Users\Админ\OneDrive\Документы\cocktail-bot\cocktail-bot`
3. Щелкните правой кнопкой мыши в пустом месте
4. Выберите "Создать" → "Текстовый документ"

### ШАГ 2: Назовите файл
1. Назовите файл `.env` (с точкой в начале)
2. Нажмите Enter
3. Если Windows спросит о расширении, нажмите "Да"

### ШАГ 3: Скопируйте содержимое
Откройте файл `.env` и скопируйте в него следующее содержимое:

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
DEFAULT_MAX_TOKENS=1000
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9

# Cursor IDE Configuration
CURSOR_AI_PROVIDER=custom
CURSOR_AI_CUSTOM_API_URL=https://llm.api.cloud.yandex.net/foundationModels/v1/completion
CURSOR_AI_CUSTOM_API_KEY=ajegpjgsbgidg7av4mfj
```

### ШАГ 4: Сохраните файл
1. Нажмите Ctrl + S
2. Закройте файл

## 🚀 ЗАПУСК БОТА

### Откройте командную строку (cmd):
1. Нажмите Win + R
2. Введите `cmd`
3. Нажмите Enter

### Перейдите в папку проекта:
```cmd
cd "C:\Users\Админ\OneDrive\Документы\cocktail-bot\cocktail-bot"
```

### Активируйте виртуальную среду:
```cmd
venv\Scripts\activate
```

### Запустите бота:
```cmd
python main.py
```

## 🎯 ТЕСТИРОВАНИЕ

### Найдите бота в Telegram:
1. Откройте Telegram
2. Найдите вашего бота по имени
3. Отправьте команду `/start`

### Попробуйте команды:
- `/recipe джин` - создать рецепт с AI
- `/seasonal` - сезонные коктейли для октября
- `/search текила` - поиск в базе данных
- `/menu conceptual 3` - концептуальное меню

## 🔧 АЛЬТЕРНАТИВНЫЙ СПОСОБ

Если не получается создать файл `.env`, можете:

1. **Переименовать существующий файл:**
   - Найдите файл `env_new_file.txt` в папке проекта
   - Переименуйте его в `.env`

2. **Использовать готовый файл:**
   - Файл `env_ready.txt` уже содержит нужные настройки
   - Переименуйте его в `.env`

## 🎉 ГОТОВО!

После создания файла `.env` ваш MixMatrixBot будет готов к работе с Yandex Cloud AI!

**Удачного использования! 🍹**



