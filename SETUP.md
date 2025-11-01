# 🔧 Настройка MixMatrixBot

## 📋 Быстрая настройка

### 1. Создайте файл `.env`
Создайте файл `.env` в корне проекта со следующим содержимым:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather

# XAI API Configuration
XAI_API_KEY=ваш_ключ_от_xAI

# Other Configuration
DEBUG=False
```

### 2. Получение токенов

#### Telegram Bot Token:
1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

#### XAI API Key:
1. Перейдите на [x.ai](https://x.ai/)
2. Зарегистрируйтесь или войдите в аккаунт
3. Перейдите в раздел API Keys
4. Создайте новый ключ
5. Скопируйте полученный ключ

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Инициализация базы данных
```bash
python database.py
```

### 5. Запуск бота
```bash
python run_bot.py
```

## 🔒 Безопасность

- **НИКОГДА** не коммитьте файл `.env` в Git
- Используйте `.env.example` для демонстрации структуры
- Регулярно обновляйте API ключи
- Используйте сильные пароли

## 🚀 Готово!

После выполнения всех шагов ваш бот будет готов к работе!

