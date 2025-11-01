#!/usr/bin/env python3
"""
Скрипт для тестирования логики обработчиков кнопок бота
Проверяет, что все обработчики корректно определены и вызывают нужные функции
"""

import inspect
import sys
from typing import Dict, List

# Импортируем бота
try:
    import bot
except ImportError:
    print("❌ Не удалось импортировать bot.py")
    sys.exit(1)

# Все кнопки из главного меню
BUTTONS = {
    'recipe': '🍸 Создать рецепт',
    'search': '🔍 Поиск',
    'random': '🎲 Случайный',
    'menu': '📋 Меню',
    'seasonal': '🍂 Сезонные',
    'pairing': '🍽️ Фудпейринг',
    'trends': '📈 Тренды',
    'news': '📰 Новости',
    'create_recipe': '➕ Создать рецепт',
    'help': 'ℹ️ Помощь'
}

def find_handler(callback_data: str) -> Dict:
    """Найти обработчик для callback_data"""
    # Получаем все функции-обработчики из модуля bot
    handlers = []
    for name, obj in inspect.getmembers(bot):
        if inspect.isfunction(obj):
            # Проверяем декораторы
            if hasattr(obj, '__wrapped__'):
                handlers.append({
                    'name': name,
                    'func': obj,
                    'wrapped': obj.__wrapped__
                })
    
    # Ищем обработчик через диспетчер
    # В реальности обработчики регистрируются через @dp.callback_query()
    # Но мы можем проверить их наличие через код
    
    return {'handlers': handlers}

def check_buttons():
    """Проверка всех кнопок"""
    print("🔍 Проверка обработчиков кнопок...\n")
    
    # Читаем исходный код bot.py
    try:
        with open('bot.py', 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print("❌ Файл bot.py не найден")
        return
    
    results = {}
    
    for callback_data, button_name in BUTTONS.items():
        print(f"Проверяю: {button_name} (callback_data='{callback_data}')")
        
        # Ищем обработчик в коде
        pattern = f"@dp.callback_query.*callback_data.*==.*['\"]{callback_data}['\"]"
        import re
        
        # Более гибкий поиск
        patterns = [
            f"callback_data.*==.*['\"]{callback_data}['\"]",
            f"c\\.data.*==.*['\"]{callback_data}['\"]",
            f"c\\.data\\.startswith\\(['\"]{callback_data.split('_')[0]}"
        ]
        
        found = False
        handler_name = None
        
        for pattern in patterns:
            matches = re.findall(pattern, code)
            if matches:
                found = True
                # Ищем имя функции после декоратора
                lines = code.split('\n')
                for i, line in enumerate(lines):
                    if re.search(pattern, line):
                        # Следующие строки должны содержать async def
                        for j in range(i+1, min(i+10, len(lines))):
                            if 'async def' in lines[j]:
                                handler_name = lines[j].split('async def')[1].split('(')[0].strip()
                                break
                        break
                if handler_name:
                    break
        
        if found:
            print(f"  ✅ Обработчик найден: {handler_name or 'unknown'}")
            results[callback_data] = {'status': '✅', 'handler': handler_name}
        else:
            print(f"  ❌ Обработчик НЕ найден!")
            results[callback_data] = {'status': '❌', 'handler': None}
        print()
    
    # Итоговая статистика
    print("\n" + "="*50)
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print("="*50)
    
    total = len(results)
    working = sum(1 for r in results.values() if r['status'] == '✅')
    broken = total - working
    
    print(f"Всего кнопок: {total}")
    print(f"✅ Работающих: {working}")
    print(f"❌ Не найденных: {broken}")
    
    if broken > 0:
        print("\n⚠️ Проблемные кнопки:")
        for callback_data, result in results.items():
            if result['status'] == '❌':
                print(f"  - {BUTTONS[callback_data]} ({callback_data})")
    
    print("\n" + "="*50)
    
    # Проверка команд
    print("\n📋 Проверка команд:")
    commands = {
        'start': 'start_command',
        'help': 'help_command',
        'recipe': 'recipe_command',
        'menu': 'menu_command',
        'random': 'random_command',
        'seasonal': 'seasonal_command',
        'pairing': 'pairing_command',
        'search': 'search_command',
        'trends': 'trends_command',
        'news': 'news_command',
    }
    
    for cmd, func_name in commands.items():
        if hasattr(bot, func_name):
            print(f"  ✅ /{cmd} -> {func_name}")
        else:
            print(f"  ❌ /{cmd} -> {func_name} НЕ НАЙДЕНА")

if __name__ == '__main__':
    print("🧪 Тестирование обработчиков кнопок MIXTRIX Bot\n")
    print("="*50 + "\n")
    check_buttons()
    print("\n✅ Проверка завершена!")

