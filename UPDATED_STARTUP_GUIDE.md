# 🍹 MixMatrixBot - Обновленные инструкции по запуску

## ✅ Обновленные данные:

### Yandex Cloud AI:
- **API Key**: `ajegpjgsbgidg7av4mfj`
- **Folder ID**: `ajels2ea51569prr6uvb`

## 📋 Что нужно для запуска бота:

### 1. Создайте файл `.env`:
Создайте файл `.env` в корневой папке проекта со следующим содержимым:

```env
# Yandex Cloud AI API Configuration
YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_telegram_токен_от_BotFather
XAI_API_KEY=ваш_xai_ключ
```

### 2. Получите недостающие токены:
- **TELEGRAM_BOT_TOKEN**: Найдите @BotFather в Telegram, создайте бота
- **XAI_API_KEY**: Зарегистрируйтесь на x.ai и получите API ключ

## 🚀 Способы запуска:

### Способ 1: Тест Yandex API
```bash
python test_yandex_api.py
```

### Способ 2: Проверка готовности
```bash
python check_bot.py
```

### Способ 3: Запуск бота
```bash
# Активируйте виртуальную среду
venv\Scripts\activate

# Запустите бота
python run_bot.py
```

### Способ 4: Прямой запуск Python
```bash
venv\Scripts\python.exe run_bot.py
```

## 🔧 Настройка Cursor IDE:

### Через настройки UI:
1. Откройте Cursor
2. Перейдите в Settings (`Ctrl + ,`)
3. Найдите раздел "AI Providers"
4. Выберите "Custom API"
5. Настройте:
   ```
   URL: https://llm.api.cloud.yandex.net/foundationModels/v1/completion
   API Key: ajegpjgsbgidg7av4mfj
   ```

### Через файл конфигурации:
Создайте файл `settings.json` в папке конфигурации Cursor:

```json
{
  "cursor.ai.provider": "custom",
  "cursor.ai.customApiUrl": "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
  "cursor.ai.customApiKey": "ajegpjgsbgidg7av4mfj"
}
```

## 🧪 Тестирование:

### 1. Тест Yandex API:
```bash
python test_yandex_api.py
```

### 2. Проверка окружения:
```bash
python check_bot.py
```

## 🎯 Функции бота:

- **🍸 Создание рецептов** с помощью Yandex GPT
- **🔍 Поиск** по базе коктейлей
- **🎲 Случайные коктейли**
- **🍂 Сезонные рецепты** для России
- **🍽️ Фудпейринг** - подбор к блюдам
- **📋 Генерация меню**
- **📈 Тренды** коктейлей 2025
- **📰 Новости** из мира HoReCa

## 📱 Команды бота:

- `/start` - начать работу
- `/help` - справка
- `/recipe [спирт]` - создать рецепт
- `/search [запрос]` - поиск
- `/random` - случайный коктейль
- `/seasonal` - сезонные коктейли
- `/pairing [блюдо]` - подбор к блюду
- `/menu [тип] [количество]` - генерация меню
- `/trends` - тренды 2025
- `/news` - новости
- `/history [коктейль]` - история коктейля

## 🔄 Обновления:

Для обновления бота:
1. Остановите бота (Ctrl+C)
2. Обновите код
3. Перезапустите бота

## 📞 Поддержка:

При возникновении проблем:
1. Проверьте файл `.env`
2. Убедитесь, что все зависимости установлены
3. Проверьте токены
4. Запустите тест: `python test_yandex_api.py`

---

**Удачного использования MixMatrixBot! 🍹**

## 🎉 Готово к запуску!

Все необходимые файлы созданы:
- ✅ `bot.py` - основной бот
- ✅ `run_bot.py` - скрипт запуска
- ✅ `test_yandex_api.py` - тест API
- ✅ `check_bot.py` - проверка готовности
- ✅ `environment.env` - переменные окружения
- ✅ `env_template.txt` - шаблон .env

Просто создайте файл `.env` с токенами и запустите бота!
















