# 🍹 MixMatrixBot - Привязан к Yandex Cloud AI

## ✅ Бот успешно привязан к Yandex Cloud AI!

### 🔑 Используемые ключи:
- **Yandex API Key**: `ajegpjgsbgidg7av4mfj`
- **Folder ID**: `ajels2ea51569prr6uvb`

## 🚀 Быстрый запуск:

### 1. Создайте файл .env:
```bash
python create_env.py
```

### 2. Получите Telegram токен:
1. Найдите @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен

### 3. Обновите файл .env:
Замените `ваш_telegram_токен_от_BotFather` на реальный токен

### 4. Запустите бота:
```bash
python run_bot.py
```

## 🧪 Тестирование:

### Тест Yandex API:
```bash
python test_yandex_api.py
```

### Проверка готовности:
```bash
python check_bot.py
```

## 🎯 Что изменилось:

### ✅ Обновления:
- **Заменили XAI API на Yandex Cloud AI**
- **Обновили все функции генерации рецептов**
- **Настроили правильные параметры API**
- **Создали скрипты для автоматической настройки**

### 🔧 Функции бота:
- **🍸 Создание рецептов** - теперь через Yandex GPT
- **🔍 Поиск** по базе коктейлей
- **🎲 Случайные коктейли** с AI
- **🍂 Сезонные рецепты** для России
- **🍽️ Фудпейринг** - подбор к блюдам
- **📋 Генерация меню** с AI
- **📈 Тренды** коктейлей 2025
- **📰 Новости** из мира HoReCa

## 📱 Команды бота:

- `/start` - начать работу
- `/help` - справка
- `/recipe [спирт]` - создать рецепт с AI
- `/search [запрос]` - поиск
- `/random` - случайный коктейль с AI
- `/seasonal` - сезонные коктейли с AI
- `/pairing [блюдо]` - подбор к блюду с AI
- `/menu [тип] [количество]` - генерация меню с AI
- `/trends` - тренды 2025
- `/news` - новости
- `/history [коктейль]` - история коктейля с AI

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
├── bot.py                 # Основной бот (обновлен для Yandex AI)
├── run_bot.py            # Скрипт запуска
├── test_yandex_api.py    # Тест Yandex API
├── check_bot.py          # Проверка готовности
├── create_env.py         # Создание .env файла
├── database.py           # База данных
├── requirements.txt      # Зависимости
├── environment.env       # Переменные окружения
├── env_template.txt      # Шблон .env
└── cocktails.db          # База данных коктейлей
```

## 🎉 Готово к использованию!

Бот полностью привязан к Yandex Cloud AI и готов к работе. Все функции генерации рецептов теперь используют Yandex GPT для создания качественных и креативных коктейлей!

### 🚀 Следующие шаги:
1. Получите Telegram токен от @BotFather
2. Запустите `python create_env.py`
3. Обновите токен в файле `.env`
4. Запустите бота: `python run_bot.py`

**Удачного использования MixMatrixBot с Yandex AI! 🍹**
















