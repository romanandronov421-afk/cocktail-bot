# 🍸 MIXTRIX - Полное руководство по добавлению знаний

## 📚 Что у нас есть сейчас

### ✅ База данных рецептов (40 рецептов):
- **12 классических** рецептов из "Код коктейля"
- **10 авторских** рецептов из "Код коктейля"  
- **13 примиксов** и сиропов
- **2 сезонных** рецепта
- **2 безалкогольных** рецепта (mocktail)
- **1 современный** рецепт

### ✅ Справочники:
- `ingredients_guide.txt` - справочник ингредиентов
- `techniques_guide.txt` - техники приготовления
- `glassware_guide.txt` - типы бокалов
- `pairing_guide.txt` - фудпейринг

### ✅ Скрипты для добавления:
- `add_recipes.py` - добавление новых рецептов
- `create_guides.py` - создание справочников

## 🛠️ Способы добавления знаний

### 1. 📖 Добавление рецептов

#### Через скрипт (рекомендуется):
```bash
# Редактируйте add_recipes.py
# Добавьте новые рецепты в список new_recipes
# Запустите скрипт
venv\Scripts\python.exe add_recipes.py
```

#### Структура рецепта:
```python
recipe = (
    "Название рецепта",           # name
    "60 мл джин, 30 мл сок",     # ingredients  
    "Шейк со льдом",             # method
    "джин",                      # base_spirit
    "категория",                 # category
    "источник",                  # source
    "Описание вкуса",            # description
    "коктейльный",               # glassware
    "лаймовая цедра",            # garnish
    "легкий",                    # difficulty
    "3 мин"                      # prep_time
)
```

### 2. 🤖 Обновление AI знаний

#### В config.ini:
```ini
[YandexGPT]
SystemMessage = You are MIXTRIX🍸 - a culinary expert specializing in beverage recipes and food pairing. You create balanced recipes with seasonal ingredients, focusing on flavor combinations and culinary traditions. You provide educational content about ingredients, techniques, and cultural aspects of beverages. Always remind users about responsible consumption and age restrictions when discussing alcoholic beverages. Avoid political topics and focus only on culinary content.

# Добавьте новые знания:
# - Современные техники: молекулярная гастрономия
# - Новые ингредиенты: ферментированные продукты  
# - Тренды 2025: zero-proof коктейли
```

### 3. 📝 Добавление новых команд

#### Пример команды справочника:
```python
@dp.message(Command('ingredients'))
async def ingredients_command(message: types.Message):
    """Справочник ингредиентов"""
    with open('ingredients_guide.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    await message.reply(content, parse_mode='Markdown')
```

### 4. 🔍 Расширение поиска

#### Добавление новых категорий:
```python
# В функции search_command
if query.lower() in ['современный', 'modern']:
    cursor.execute("SELECT * FROM recipes WHERE category = ?", ('современный',))
    recipes = cursor.fetchall()
```

## 📋 Пошаговые инструкции

### Шаг 1: Определите тип знаний
- **Рецепты** → Используйте `add_recipes.py`
- **Справочная информация** → Используйте `create_guides.py`
- **AI контекст** → Редактируйте `config.ini`
- **Новые команды** → Редактируйте `main.py`

### Шаг 2: Подготовьте данные
- Структурируйте информацию
- Используйте единый формат
- Проверьте корректность данных

### Шаг 3: Реализуйте изменения
- Отредактируйте соответствующий файл
- Запустите скрипт (если используете)
- Протестируйте изменения

### Шаг 4: Примените изменения
- Остановите бота: `taskkill /F /IM python.exe`
- Запустите бота: `venv\Scripts\python.exe main.py`
- Проверьте работу новых функций

## 🎯 Практические примеры

### Пример 1: Добавление сезонных рецептов
```python
# В add_recipes.py добавьте:
seasonal_recipes = [
    ("Winter Manhattan", "60 мл виски, 30 мл вермут, 2 дэш биттерс", 
     "Стир со льдом", "виски", "сезонный", "MIXTRIX", 
     "Зимний вариант Manhattan", "коктейльный", "апельсиновая цедра", 
     "средний", "3 мин"),
]
```

### Пример 2: Добавление команды справочника
```python
# В main.py добавьте:
@dp.message(Command('ingredients'))
async def ingredients_command(message: types.Message):
    """Справочник ингредиентов"""
    try:
        with open('ingredients_guide.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        await message.reply(content, parse_mode='Markdown')
    except FileNotFoundError:
        await message.reply("Справочник ингредиентов не найден.")
```

### Пример 3: Обновление AI промпта
```python
# В config.ini обновите SystemMessage:
SystemMessage = You are MIXTRIX🍸 - a culinary expert specializing in beverage recipes and food pairing. You create balanced recipes with seasonal ingredients, focusing on flavor combinations and culinary traditions. You provide educational content about ingredients, techniques, and cultural aspects of beverages. Always remind users about responsible consumption and age restrictions when discussing alcoholic beverages. Avoid political topics and focus only on culinary content.

# Новые знания:
# - Современные техники: молекулярная гастрономия, sous-vide
# - Тренды 2025: zero-proof коктейли, fat-washing
# - Специальные ингредиенты: ферментированные продукты, умами
```

## 🔧 Технические детали

### Файлы для редактирования:
- `main.py` - основной код бота
- `config.ini` - конфигурация AI
- `add_recipes.py` - скрипт добавления рецептов
- `create_guides.py` - скрипт создания справочников
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

## 📊 Текущая статистика

### База данных:
- **Всего рецептов**: 40
- **Категории**: 6 (классический, авторский, примикс, сезонный, mocktail, современный)
- **Источники**: Код коктейля, MIXTRIX

### Команды:
- `/start` - запуск с проверкой возраста
- `/rules` - правила пользования
- `/examples` - примеры использования
- `/recipe` - создание рецепта
- `/search` - поиск рецептов
- `/classic` - классические рецепты
- `/signature` - авторские рецепты
- `/premix` - примиксы и сиропы
- `/recipe_detail` - подробный рецепт

## 💡 Советы по добавлению знаний

1. **Структурируйте данные** - используйте единый формат
2. **Тестируйте изменения** - проверяйте работу после каждого изменения
3. **Документируйте** - ведите учет добавленных знаний
4. **Резервируйте** - сохраняйте копии файлов перед изменениями
5. **Постепенно** - добавляйте знания небольшими порциями
6. **Категоризируйте** - используйте понятные категории
7. **Проверяйте качество** - убедитесь в корректности информации

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

## 🎉 Заключение

Теперь у вас есть полный набор инструментов для добавления знаний в MIXTRIX🍸:

- ✅ **40 рецептов** в базе данных
- ✅ **4 справочника** готовых к использованию
- ✅ **2 скрипта** для добавления знаний
- ✅ **Подробные инструкции** по всем способам
- ✅ **Готовые шаблоны** для быстрого старта

**MIXTRIX🍸 готов к расширению знаний!** 🍸

