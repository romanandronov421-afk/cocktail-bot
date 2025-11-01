#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

print("=== Проверка и запуск бота ===")

# Проверяем Python
print(f"Python версия: {sys.version}")

# Проверяем файлы
print("\nПроверяем файлы:")
files = ['env_file.txt', 'bot_simple.py']
for file in files:
    if os.path.exists(file):
        print(f"✓ {file}")
    else:
        print(f"✗ {file} - НЕ НАЙДЕН")
        sys.exit(1)

# Проверяем зависимости
print("\nПроверяем зависимости:")
deps = ['aiogram', 'requests', 'dotenv']
missing = []

for dep in deps:
    try:
        __import__(dep)
        print(f"✓ {dep}")
    except ImportError:
        print(f"✗ {dep} - не установлен")
        missing.append(dep)

if missing:
    print(f"\nУстановите недостающие зависимости:")
    print(f"pip install {' '.join(missing)}")
    sys.exit(1)

print("\n✓ Все проверки пройдены!")
print("Запускаем бота...")

# Запускаем бота
try:
    import subprocess
    subprocess.run([sys.executable, 'bot_simple.py'])
except KeyboardInterrupt:
    print("\n🛑 Бот остановлен")
except Exception as e:
    print(f"\n❌ Ошибка: {e}")









