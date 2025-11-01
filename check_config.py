#!/usr/bin/env python3
"""Проверка конфигурации перед запуском бота"""
import sys
import os
from dotenv import load_dotenv

print("=" * 50)
print("ПРОВЕРКА КОНФИГУРАЦИИ БОТА")
print("=" * 50)

# Проверка Python
print(f"\n✓ Python версия: {sys.version}")

# Загрузка переменных окружения
load_dotenv('env_file.txt')

# Проверка переменных окружения
print("\n📋 Проверка переменных окружения:")
env_vars = {
    'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
    'YANDEX_API_KEY': os.getenv('YANDEX_API_KEY'),
    'FOLDER_ID': os.getenv('FOLDER_ID'),
}

all_ok = True
for key, value in env_vars.items():
    if value:
        print(f"  ✓ {key}: OK (длина: {len(value)})")
    else:
        print(f"  ✗ {key}: ОТСУТСТВУЕТ")
        all_ok = False

# Проверка файлов
print("\n📁 Проверка файлов:")
files_to_check = [
    'bot.py',
    'database.py',
    'hybrid_processor.py',
    'cocktail_party_processor.py',
    'enhanced_foodpairing_processor.py',
    'env_file.txt',
    'cocktails.db'
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"  ✓ {file}: существует")
    else:
        print(f"  ✗ {file}: отсутствует")
        all_ok = False

# Проверка импортов
print("\n🔍 Проверка импортов:")
try:
    import aiogram
    print("  ✓ aiogram: OK")
except ImportError as e:
    print(f"  ✗ aiogram: {e}")
    all_ok = False

try:
    from database import CocktailDatabase
    print("  ✓ database: OK")
except ImportError as e:
    print(f"  ✗ database: {e}")
    all_ok = False

try:
    from hybrid_processor import HybridCocktailProcessor
    print("  ✓ hybrid_processor: OK")
except ImportError as e:
    print(f"  ✗ hybrid_processor: {e}")
    all_ok = False

# Проверка базы данных
print("\n💾 Проверка базы данных:")
try:
    from database import CocktailDatabase
    db = CocktailDatabase()
    with db.conn:
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM recipes")
        count = cursor.fetchone()[0]
        print(f"  ✓ База данных: OK ({count} коктейлей)")
except Exception as e:
    print(f"  ✗ База данных: {e}")
    all_ok = False

print("\n" + "=" * 50)
if all_ok:
    print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ - ГОТОВ К ЗАПУСКУ")
else:
    print("❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ - ТРЕБУЕТСЯ ИСПРАВЛЕНИЕ")
print("=" * 50)

sys.exit(0 if all_ok else 1)




