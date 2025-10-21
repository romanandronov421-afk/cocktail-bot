# 🔧 Исправление ошибки базы данных

## ❌ Проблема:
```
sqlite3.OperationalError: table recipes has no column named category
```

## ✅ Решение:

### 1. Удалите старую базу данных:
```bash
del cocktails.db
```

### 2. Создайте файл .env вручную:
Создайте файл `.env` в корневой папке со следующим содержимым:

```env
BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q
YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb
```

### 3. Запустите бота:
```bash
python main.py
```

## 🔧 Что исправлено:

1. **База данных** - добавлена команда `DROP TABLE IF EXISTS recipes` для удаления старой таблицы
2. **Структура таблицы** - пересоздана с правильными колонками
3. **main.py** - обновлен для правильной инициализации базы данных

## 📋 Содержимое файла .env:
```env
BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q
YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb
```

## 🚀 После исправления:

1. **Удалите старую базу данных:**
   ```bash
   del cocktails.db
   ```

2. **Создайте файл .env** с содержимым выше

3. **Запустите бота:**
   ```bash
   python main.py
   ```

4. **Найдите бота в Telegram и отправьте `/start`**

## 🎯 Команды бота:
- `/start` - начать работу
- `/recipe джин` - создать рецепт с AI
- `/seasonal` - сезонные коктейли для октября
- `/search текила` - поиск в базе данных
- `/menu conceptual 3` - концептуальное меню

**Проблема с базой данных решена! Бот готов к работе! 🍹**



