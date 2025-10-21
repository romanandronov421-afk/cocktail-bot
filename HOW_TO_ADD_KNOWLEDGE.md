# 📚 Как добавлять знания в MIXTRIX🍸

## 🎯 Способы добавления знаний

### 1. 📖 Добавление рецептов в базу данных

#### Через код (программно):
```python
# В файле main.py, функция init_database()
def add_new_recipes():
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    # Новые рецепты
    new_recipes = [
        ("Название рецепта", "ингредиенты", "метод", "базовый спирт", 
         "категория", "источник", "описание", "бокал", "украшение", 
         "сложность", "время"),
        # Добавьте столько рецептов, сколько нужно
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO recipes 
        (name, ingredients, method, base_spirit, category, source, 
         description, glassware, garnish, difficulty, prep_time) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, new_recipes)
    
    conn.commit()
    conn.close()
```

#### Структура рецепта:
```python
recipe = (
    "Название рецепта",           # name
    "60 мл джин, 30 мл сок",     # ingredients  
    "Шейк со льдом",             # method
    "джин",                      # base_spirit
    "классический",              # category (классический/авторский/примикс)
    "Источник",                  # source
    "Описание вкуса",            # description
    "коктейльный",               # glassware
    "лаймовая цедра",            # garnish
    "легкий",                    # difficulty (легкий/средний/сложный)
    "3 мин"                      # prep_time
)
```

### 2. 🤖 Обновление AI промптов

#### В файле config.ini:
```ini
[YandexGPT]
SystemMessage = You are MIXTRIX🍸 - a culinary expert specializing in beverage recipes and food pairing. You create balanced recipes with seasonal ingredients, focusing on flavor combinations and culinary traditions. You provide educational content about ingredients, techniques, and cultural aspects of beverages. Always remind users about responsible consumption and age restrictions when discussing alcoholic beverages. Avoid political topics and focus only on culinary content.

# Добавьте новые знания в SystemMessage:
# - Новые техники приготовления
# - Специальные ингредиенты
# - Кулинарные традиции
# - Современные тренды
```

#### В коде (функция call_yandex_api):
```python
async def call_yandex_api(prompt: str) -> str:
    # Добавьте контекстные знания
    knowledge_context = """
    Дополнительные знания:
    - Новые техники: молекулярная гастрономия, sous-vide
    - Современные ингредиенты: ферментированные продукты
    - Тренды 2025: zero-proof коктейли, fat-washing
    """
    
    enhanced_prompt = f"{knowledge_context}\n\n{prompt}"
    # Остальной код...
```

### 3. 📝 Добавление новых команд

#### Пример новой команды:
```python
@dp.message(Command('new_command'))
async def new_command_handler(message: types.Message):
    """Обработчик новой команды"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    # Логика команды
    response = "Ответ на новую команду"
    await message.reply(response, parse_mode='Markdown')
```

### 4. 🔍 Расширение поиска

#### Добавление новых категорий:
```python
# В функции search_command добавить:
if query.lower() in ['новая_категория', 'new_category']:
    cursor.execute("SELECT * FROM recipes WHERE category = ?", ('новая_категория',))
    recipes = cursor.fetchall()
    # Обработка результатов...
```

### 5. 📚 Добавление справочной информации

#### Создание новых справочных команд:
```python
@dp.message(Command('ingredients'))
async def ingredients_command(message: types.Message):
    """Справочник ингредиентов"""
    ingredients_info = """
    🥄 **Справочник ингредиентов**
    
    **Спирты:**
    - Джин: можжевеловые ноты
    - Виски: дымные и ванильные
    - Ром: тропические и карамельные
    - Текила: агавовые и пряные
    
    **Ликеры:**
    - Трипл сек: апельсиновый
    - Шартрез: травяной
    - Кампари: горький
    
    **Сиропы:**
    - Simple Syrup: базовый сладкий
    - Grenadine: гранатовый
    - Orgeat: миндальный
    """
    await message.reply(ingredients_info, parse_mode='Markdown')
```

## 🛠️ Практические примеры

### Пример 1: Добавление сезонных рецептов
```python
# Добавить в init_database()
seasonal_recipes = [
    ("Winter Manhattan", "60 мл виски, 30 мл вермут, 2 дэш биттерс", 
     "Стир со льдом", "виски", "сезонный", "MIXTRIX", 
     "Зимний вариант Manhattan", "коктейльный", "апельсиновая цедра", 
     "средний", "3 мин"),
]
```

### Пример 2: Добавление техник приготовления
```python
# В SystemMessage добавить:
techniques_knowledge = """
Техники приготовления:
- Шейк: энергичное встряхивание со льдом
- Стир: перемешивание ложкой
- Билд: смешивание в бокале
- Мудл: разминание ингредиентов
- Дабл-шейк: двойное встряхивание
"""
```

### Пример 3: Добавление фудпейринга
```python
# Создать новую команду
@dp.message(Command('pairing_guide'))
async def pairing_guide_command(message: types.Message):
    """Руководство по фудпейрингу"""
    pairing_info = """
    🍽️ **Руководство по фудпейрингу**
    
    **К мясу:**
    - Стейк → Manhattan, Old Fashioned
    - Рыба → Gin Fizz, White Wine Spritzer
    
    **К десертам:**
    - Шоколад → Espresso Martini, Brandy Alexander
    - Фрукты → Daiquiri, Bellini
    
    **К сыру:**
    - Твердые сыры → Whiskey Sour, Negroni
    - Мягкие сыры → Prosecco, Kir Royale
    """
    await message.reply(pairing_info, parse_mode='Markdown')
```

## 📋 Пошаговая инструкция

### Шаг 1: Определите тип знаний
- Рецепты → База данных
- Техники → AI промпты
- Справочная информация → Новые команды
- Категории → Расширение поиска

### Шаг 2: Выберите способ добавления
- **База данных**: Для структурированных данных (рецепты)
- **AI промпты**: Для контекстных знаний
- **Новые команды**: Для справочной информации
- **Расширение существующих**: Для улучшения функций

### Шаг 3: Реализуйте изменения
1. Отредактируйте соответствующий файл
2. Добавьте новый код
3. Протестируйте изменения
4. Перезапустите бота

### Шаг 4: Проверьте работу
1. Отправьте тестовые команды
2. Проверьте поиск
3. Убедитесь в корректности ответов

## 🔧 Технические детали

### Файлы для редактирования:
- `main.py` - основной код бота
- `config.ini` - конфигурация AI
- `cocktails.db` - база данных (создается автоматически)

### Структура базы данных:
```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,              -- Название рецепта
    ingredients TEXT,              -- Ингредиенты
    method TEXT,                  -- Метод приготовления
    base_spirit TEXT,             -- Базовый спирт
    category TEXT,                -- Категория
    source TEXT,                  -- Источник
    description TEXT,             -- Описание
    glassware TEXT,               -- Бокал
    garnish TEXT,                 -- Украшение
    difficulty TEXT,              -- Сложность
    prep_time TEXT               -- Время приготовления
);
```

## 💡 Советы по добавлению знаний

1. **Структурируйте данные** - используйте единый формат
2. **Тестируйте изменения** - проверяйте работу после каждого изменения
3. **Документируйте** - ведите учет добавленных знаний
4. **Резервируйте** - сохраняйте копии файлов перед изменениями
5. **Постепенно** - добавляйте знания небольшими порциями

## 🚀 Готовые шаблоны

### Шаблон нового рецепта:
```python
new_recipe = (
    "Название рецепта",
    "60 мл базовый спирт, 30 мл дополнительный ингредиент",
    "Техника приготовления",
    "базовый спирт",
    "категория",
    "источник",
    "Описание вкуса и особенностей",
    "тип бокала",
    "украшение",
    "сложность",
    "время приготовления"
)
```

### Шаблон новой команды:
```python
@dp.message(Command('command_name'))
async def command_name_handler(message: types.Message):
    """Описание команды"""
    # Логика команды
    response = "Ответ пользователю"
    await message.reply(response, parse_mode='Markdown')
```

**Теперь вы знаете, как добавлять знания в MIXTRIX🍸!** 🍸

