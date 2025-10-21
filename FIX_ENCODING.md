# 🔧 Исправление ошибки кодировки

## ❌ Проблема:
```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x98 in position 652
```

## ✅ Решение:

### 1. Создайте файл .env:
```bash
python create_env_simple.py
```

### 2. Или создайте вручную:
Переименуйте `env_file.txt` в `.env`

### 3. Запустите бота:
```bash
python main.py
```

## 📋 Содержимое файла .env:
```env
BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q
YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb
```

## 🔧 Что исправлено:

1. **config.ini** - пересоздан с правильной кодировкой UTF-8
2. **main.py** - добавлен параметр `encoding='utf-8'` для чтения конфигурации
3. **env_file.txt** - создан файл с правильной кодировкой
4. **create_env_simple.py** - скрипт для создания .env файла

## 🚀 После исправления:

1. **Создайте файл .env:**
   ```bash
   python create_env_simple.py
   ```

2. **Запустите бота:**
   ```bash
   python main.py
   ```

3. **Найдите бота в Telegram и отправьте `/start`**

## 🎯 Команды бота:
- `/start` - начать работу
- `/recipe джин` - создать рецепт с AI
- `/seasonal` - сезонные коктейли для октября
- `/search текила` - поиск в базе данных
- `/menu conceptual 3` - концептуальное меню

**Проблема с кодировкой решена! Бот готов к работе! 🍹**



