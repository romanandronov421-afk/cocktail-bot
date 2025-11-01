# 🚀 Развертывание MixMatrixBot

## 📋 Требования

- Python 3.8+
- Telegram Bot Token (от [@BotFather](https://t.me/BotFather))
- XAI API Key (от [xAI](https://x.ai/))

## 🔧 Локальная установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/romanandronov421-afk/cocktail-bot.git
cd cocktail-bot
```

### 2. Создание виртуального окружения
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env`:
```env
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
XAI_API_KEY=ваш_ключ_от_xAI
DEBUG=False
```

### 5. Инициализация базы данных
```bash
python database.py
```

### 6. Запуск бота
```bash
python run_bot.py
```

## ☁️ Развертывание на сервере

### Heroku
1. Создайте `Procfile`:
```
worker: python run_bot.py
```

2. Добавьте переменные окружения в настройках Heroku
3. Деплойте через Git

### VPS/Сервер
1. Установите Python и зависимости
2. Настройте systemd service:
```ini
[Unit]
Description=MixMatrixBot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/cocktail-bot
ExecStart=/path/to/venv/bin/python run_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Запустите сервис:
```bash
sudo systemctl enable cocktail-bot
sudo systemctl start cocktail-bot
```

### Docker
Создайте `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python database.py

CMD ["python", "run_bot.py"]
```

## 🔐 Безопасность

- Никогда не коммитьте файл `.env`
- Используйте сильные пароли для API ключей
- Регулярно обновляйте зависимости
- Настройте логирование для мониторинга

## 📊 Мониторинг

### Логи
```bash
# Просмотр логов
tail -f bot.log

# Системные логи (systemd)
journalctl -u cocktail-bot -f
```

### Метрики
- Количество активных пользователей
- Популярные команды
- Ошибки API

## 🔄 Обновление

1. Остановите бота
2. Обновите код:
```bash
git pull origin main
pip install -r requirements.txt
```
3. Перезапустите бота

## 🆘 Устранение неполадок

### Бот не отвечает
- Проверьте токен в `.env`
- Убедитесь, что бот запущен
- Проверьте логи на ошибки

### Ошибки API
- Проверьте ключ XAI API
- Убедитесь в наличии интернет-соединения
- Проверьте лимиты API

### Проблемы с базой данных
- Убедитесь, что файл `cocktails.db` существует
- Перезапустите инициализацию: `python database.py`

## 📞 Поддержка

- GitHub Issues: [Создать issue](https://github.com/romanandronov421-afk/cocktail-bot/issues)
- Telegram: [@your_support_bot](https://t.me/your_support_bot)

---

*Удачного развертывания! 🍹*

