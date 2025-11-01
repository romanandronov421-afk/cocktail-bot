#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Простой запуск бота"""
import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🍹 ЗАПУСК COCKTAIL BOT")
print("=" * 60)
print()

try:
    # Импортируем и запускаем бота
    from bot import main
    import asyncio
    
    print("✅ Модули загружены успешно")
    print("🚀 Запуск бота...\n")
    
    asyncio.run(main())
    
except KeyboardInterrupt:
    print("\n\n🛑 Бот остановлен")
except Exception as e:
    print(f"\n\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)




