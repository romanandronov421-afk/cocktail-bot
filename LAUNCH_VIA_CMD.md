# 🚀 ЗАПУСК MIXMATRIXBOT ЧЕРЕЗ КОМАНДНУЮ СТРОКУ

## ❗ ПРОБЛЕМА С POWERSHELL
PowerShell полностью сломан. Используйте обычную командную строку Windows (cmd).

## 📝 ШАГ 1: СОЗДАНИЕ ФАЙЛА .ENV

### Способ 1: Переименование файла
1. Найдите файл `env_file.txt` в папке проекта
2. Переименуйте его в `.env` (с точкой в начале)

### Способ 2: Создание нового файла
1. Создайте новый текстовый файл
2. Назовите его `.env`
3. Скопируйте содержимое:

```env
YANDEX_API_KEY=ajegpjgsbgidg7av4mfj
FOLDER_ID=ajels2ea51569prr6uvb
TELEGRAM_BOT_TOKEN=8303598270:AAF3lCM3RTyBjUxfUSXryUgSk2lZ8mpBO8Q
DEFAULT_MODEL=yandexgpt
DEFAULT_MAX_TOKENS=1000
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9
```

## 🚀 ШАГ 2: ЗАПУСК ЧЕРЕЗ КОМАНДНУЮ СТРОКУ

### Откройте командную строку (cmd):
1. Нажмите **Win + R**
2. Введите `cmd`
3. Нажмите **Enter**

### Перейдите в папку проекта:
```cmd
cd "C:\Users\Админ\OneDrive\Документы\cocktail-bot\cocktail-bot"
```

### Активируйте виртуальную среду:
```cmd
venv\Scripts\activate
```

### Запустите бота через py:
```cmd
py main.py
```

### ИЛИ через python:
```cmd
python main.py
```

## 🎯 ШАГ 3: ТЕСТИРОВАНИЕ

### Найдите бота в Telegram:
1. Откройте Telegram
2. Найдите вашего бота по имени
3. Отправьте команду `/start`

### Попробуйте команды:
- `/recipe джин` - создать рецепт с AI
- `/seasonal` - сезонные коктейли для октября
- `/search текила` - поиск в базе данных
- `/menu conceptual 3` - концептуальное меню

## 🔧 АЛЬТЕРНАТИВНЫЕ СПОСОБЫ ЗАПУСКА:

### Способ 1: Через batch файл
```cmd
start_bot.bat
```

### Способ 2: Через Python скрипт
```cmd
py simple_start.py
```

### Способ 3: Прямой запуск main.py
```cmd
py main.py
```

## 🛑 ОСТАНОВКА БОТА:
- Нажмите **Ctrl + C** в командной строке
- Или закройте окно командной строки

## 🎉 ГОТОВО!

После выполнения всех шагов ваш MixMatrixBot будет работать с Yandex Cloud AI!

**Удачного использования! 🍹**
















