# 🍸 MIXTRIX - Пошаговая инструкция по развертыванию

## 📋 Обзор проекта

**MIXTRIX🍸** - профессиональная система для создания коктейлей и управления барными картами для индустрии HoReCA.

### 🎯 Возможности:
- 🤖 AI-генерация рецептов с фудпейрингом
- 📋 Создание сезонных коктейльных карт
- 🍽️ Профессиональный фудпейринг
- 🌿 Сезонность ингредиентов для России
- 📰 Новости HORECA индустрии
- 🌍 Международная поддержка

---

## 🚀 Этап 1: Подготовка окружения

### 1.1 Установка Python
```bash
# Скачайте Python 3.11+ с python.org
# Убедитесь, что Python добавлен в PATH
python --version
```

### 1.2 Создание виртуального окружения
```bash
# Создание виртуального окружения
python -m venv mixtrix_env

# Активация (Windows)
mixtrix_env\Scripts\activate

# Активация (Linux/Mac)
source mixtrix_env/bin/activate
```

### 1.3 Установка зависимостей
```bash
pip install aiogram python-dotenv aiohttp sqlite3 asyncio
```

---

## 🗄️ Этап 2: Настройка базы данных

### 2.1 Создание профессиональной базы данных
```bash
# Запуск скрипта заполнения базы
python populate_mixtrix_db.py
```

### 2.2 Проверка базы данных
```bash
# Проверка структуры
python -c "
import sqlite3
conn = sqlite3.connect('mixtrix_professional.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
print('Таблицы:', [row[0] for row in cursor.fetchall()])
conn.close()
"
```

---

## 🔑 Этап 3: Настройка API ключей

### 3.1 Создание файла окружения
Создайте файл `env_file.txt`:
```env
# Telegram Bot Token (получить у @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Yandex Cloud AI (получить в Yandex Cloud Console)
YANDEX_API_KEY=your_yandex_api_key
FOLDER_ID=your_folder_id

# Настройки AI
DEFAULT_MODEL=yandexgpt
DEFAULT_MAX_TOKENS=1000
DEFAULT_TEMPERATURE=0.7
DEFAULT_TOP_P=0.9
```

### 3.2 Получение Telegram Bot Token
1. Найдите @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте полученный токен

### 3.3 Настройка Yandex Cloud AI
1. Зарегистрируйтесь в Yandex Cloud
2. Создайте сервисный аккаунт
3. Получите API ключ и Folder ID
4. Добавьте в `env_file.txt`

---

## 🤖 Этап 4: Тестирование AI модуля

### 4.1 Тест AI генерации
```bash
python mixtrix_ai.py
```

### 4.2 Тест профессиональной системы
```bash
python mixtrix_professional.py
```

---

## 📱 Этап 5: Запуск Telegram бота

### 5.1 Запуск бота
```bash
python mixtrix_telegram_bot.py
```

### 5.2 Проверка работы
1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Проверьте все функции

---

## 🌐 Этап 6: Развертывание на хостинге Beget

### 6.1 Подготовка к деплою
```bash
# Создание архива проекта
tar -czf mixtrix_project.tar.gz *.py *.db *.txt requirements.txt

# Или через zip
zip -r mixtrix_project.zip *.py *.db *.txt requirements.txt
```

### 6.2 Настройка на Beget

#### 6.2.1 Создание аккаунта
1. Зарегистрируйтесь на beget.com
2. Выберите тарифный план
3. Создайте хостинг

#### 6.2.2 Загрузка файлов
1. Войдите в панель управления Beget
2. Откройте файловый менеджер
3. Загрузите архив проекта
4. Распакуйте файлы

#### 6.2.3 Настройка Python
1. В панели управления выберите "Python"
2. Создайте Python приложение
3. Укажите путь к `mixtrix_telegram_bot.py`
4. Установите зависимости

#### 6.2.4 Настройка переменных окружения
1. В настройках приложения добавьте переменные:
   - `TELEGRAM_BOT_TOKEN`
   - `YANDEX_API_KEY`
   - `FOLDER_ID`

#### 6.2.5 Настройка базы данных
1. Создайте SQLite базу данных
2. Загрузите `mixtrix_professional.db`
3. Убедитесь в правах доступа

### 6.3 Настройка автозапуска
```bash
# Создание systemd сервиса (Linux)
sudo nano /etc/systemd/system/mixtrix-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=MIXTRIX Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/mixtrix
ExecStart=/path/to/mixtrix_env/bin/python mixtrix_telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активация сервиса:
```bash
sudo systemctl enable mixtrix-bot
sudo systemctl start mixtrix-bot
sudo systemctl status mixtrix-bot
```

---

## 🔧 Этап 7: Настройка мониторинга

### 7.1 Логирование
```bash
# Проверка логов
tail -f mixtrix.log

# Ротация логов
logrotate /etc/logrotate.d/mixtrix
```

### 7.2 Мониторинг производительности
```bash
# Мониторинг процессов
ps aux | grep mixtrix

# Мониторинг ресурсов
htop
```

---

## 📊 Этап 8: Настройка аналитики

### 8.1 Создание дашборда
```python
# Создание файла analytics.py
import sqlite3
import json
from datetime import datetime, timedelta

def get_usage_stats():
    """Получение статистики использования"""
    conn = sqlite3.connect('mixtrix_professional.db')
    cursor = conn.cursor()
    
    # Статистика за последние 7 дней
    week_ago = datetime.now() - timedelta(days=7)
    
    cursor.execute("""
        SELECT action, COUNT(*) as count
        FROM usage_analytics
        WHERE timestamp >= ?
        GROUP BY action
        ORDER BY count DESC
    """, (week_ago,))
    
    stats = cursor.fetchall()
    conn.close()
    
    return stats
```

### 8.2 Настройка уведомлений
```python
# Создание файла notifications.py
import asyncio
from aiogram import Bot

async def send_admin_notification(message: str):
    """Отправка уведомления администратору"""
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    admin_id = os.getenv('ADMIN_TELEGRAM_ID')
    
    await bot.send_message(admin_id, f"🔔 MIXTRIX Alert: {message}")
    await bot.session.close()
```

---

## 🚀 Этап 9: Масштабирование

### 9.1 Настройка кластера
```bash
# Использование Docker для масштабирования
docker build -t mixtrix-bot .
docker run -d --name mixtrix-bot mixtrix-bot
```

### 9.2 Настройка балансировщика нагрузки
```nginx
# nginx.conf
upstream mixtrix_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name mixtrix.yourdomain.com;
    
    location / {
        proxy_pass http://mixtrix_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔒 Этап 10: Безопасность

### 10.1 Настройка SSL
```bash
# Получение SSL сертификата
certbot --nginx -d mixtrix.yourdomain.com
```

### 10.2 Настройка файрвола
```bash
# Настройка UFW (Ubuntu)
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 10.3 Резервное копирование
```bash
# Создание скрипта бэкапа
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz mixtrix_professional.db *.py
```

---

## 📈 Этап 11: Оптимизация

### 11.1 Кэширование
```python
# Добавление Redis для кэширования
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_recipe(recipe_id: str, recipe_data: dict):
    """Кэширование рецепта"""
    redis_client.setex(f"recipe:{recipe_id}", 3600, json.dumps(recipe_data))

def get_cached_recipe(recipe_id: str):
    """Получение рецепта из кэша"""
    cached = redis_client.get(f"recipe:{recipe_id}")
    return json.loads(cached) if cached else None
```

### 11.2 Оптимизация базы данных
```sql
-- Создание индексов
CREATE INDEX idx_cocktails_category ON cocktails(category);
CREATE INDEX idx_cocktails_season ON cocktails(seasonal_availability);
CREATE INDEX idx_ingredients_category ON ingredients(category);
CREATE INDEX idx_usage_timestamp ON usage_analytics(timestamp);
```

---

## 🎯 Этап 12: Тестирование

### 12.1 Функциональное тестирование
```bash
# Запуск тестов
python -m pytest tests/

# Тестирование API
python test_api.py

# Тестирование базы данных
python test_database.py
```

### 12.2 Нагрузочное тестирование
```bash
# Использование Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/health

# Использование wrk
wrk -t12 -c400 -d30s http://localhost:8000/api/health
```

---

## 📱 Этап 13: Мобильное приложение

### 13.1 Создание API для мобильного приложения
```python
# Создание файла mobile_api.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MIXTRIX Mobile API")

class RecipeRequest(BaseModel):
    base_spirit: str
    difficulty: str
    season: str

@app.post("/api/generate_recipe")
async def generate_recipe(request: RecipeRequest):
    """API для генерации рецептов"""
    # Логика генерации рецепта
    return {"recipe": "generated_recipe"}
```

### 13.2 Настройка веб-интерфейса
```html
<!-- Создание файла web_interface.html -->
<!DOCTYPE html>
<html>
<head>
    <title>MIXTRIX Professional</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>🍸 MIXTRIX Professional</h1>
    <div id="recipe-generator">
        <!-- Интерфейс генерации рецептов -->
    </div>
</body>
</html>
```

---

## 🌍 Этап 14: Международная поддержка

### 14.1 Настройка локализации
```python
# Создание файла localization.py
import json

LANGUAGES = {
    'ru': 'Русский',
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano'
}

def get_localized_text(key: str, language: str = 'ru') -> str:
    """Получение локализованного текста"""
    with open(f'locales/{language}.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)
    return translations.get(key, key)
```

### 14.2 Создание файлов локализации
```json
// locales/en.json
{
    "welcome": "Welcome to MIXTRIX!",
    "generate_recipe": "Generate Recipe",
    "create_menu": "Create Menu",
    "food_pairing": "Food Pairing"
}
```

---

## 📊 Этап 15: Аналитика и отчеты

### 15.1 Создание дашборда аналитики
```python
# Создание файла analytics_dashboard.py
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def create_usage_chart():
    """Создание графика использования"""
    conn = sqlite3.connect('mixtrix_professional.db')
    
    # Загрузка данных
    df = pd.read_sql_query("""
        SELECT DATE(timestamp) as date, COUNT(*) as usage_count
        FROM usage_analytics
        WHERE timestamp >= date('now', '-30 days')
        GROUP BY DATE(timestamp)
        ORDER BY date
    """, conn)
    
    # Создание графика
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['usage_count'])
    plt.title('MIXTRIX Usage Over Time')
    plt.xlabel('Date')
    plt.ylabel('Usage Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('usage_chart.png')
    
    conn.close()
```

---

## 🎉 Заключение

После выполнения всех этапов у вас будет:

✅ **Полнофункциональный MIXTRIX бот**
✅ **Профессиональная база данных**
✅ **AI-генерация рецептов**
✅ **Фудпейринг система**
✅ **Сезонные рекомендации**
✅ **HORECA новости**
✅ **Международная поддержка**
✅ **Развертывание на Beget**
✅ **Мониторинг и аналитика**

### 🚀 Следующие шаги:
1. **Маркетинг** - продвижение в HoReCA сообществе
2. **Партнерства** - сотрудничество с барами и ресторанами
3. **Расширение** - добавление новых функций
4. **Мобильное приложение** - разработка iOS/Android версии
5. **Интеграции** - подключение к POS системам

### 📞 Поддержка:
- **Документация**: README.md
- **Issues**: GitHub Issues
- **Сообщество**: Telegram канал MIXTRIX
- **Email**: support@mixtrix.com

---

*Инструкция создана для MIXTRIX Professional System*  
*Версия: 1.0*  
*Дата: 2024*












