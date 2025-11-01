#!/usr/bin/env python3
"""
Проверка статуса бота MIXTRIX
"""

import os
import sys

def check_status():
    """Проверка статуса системы"""
    print("🍸 Проверка статуса MIXTRIX Bot")
    print("=" * 40)
    
    # Проверяем Python
    print(f"✅ Python версия: {sys.version}")
    
    # Проверяем файлы
    files = ['bot.py', 'env_file.txt', 'database.py', 'enhanced_foodpairing_processor.py']
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file} - найден")
        else:
            print(f"❌ {file} - не найден")
    
    # Проверяем переменные окружения
    try:
        from dotenv import load_dotenv
        load_dotenv('env_file.txt')
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        yandex_key = os.getenv('YANDEX_API_KEY')
        folder_id = os.getenv('FOLDER_ID')
        
        if token:
            print("✅ TELEGRAM_BOT_TOKEN - настроен")
        else:
            print("❌ TELEGRAM_BOT_TOKEN - не настроен")
            
        if yandex_key:
            print("✅ YANDEX_API_KEY - настроен")
        else:
            print("❌ YANDEX_API_KEY - не настроен")
            
        if folder_id:
            print("✅ FOLDER_ID - настроен")
        else:
            print("❌ FOLDER_ID - не настроен")
            
    except Exception as e:
        print(f"❌ Ошибка загрузки переменных: {e}")
    
    print("\n🎯 Новые возможности бота:")
    print("• Фудпейринг на основе The Flavor Bible")
    print("• 300+ вкусовых комбинаций")
    print("• Интеграция всех профессиональных источников")
    print("• Сезонные рекомендации для России")
    print("• Улучшенная генерация рецептов")
    
    print("\n🚀 Команды для запуска:")
    print("• start_bot.bat - запуск через bat-файл")
    print("• python bot.py - прямой запуск")
    print("• python check_status.py - проверка статуса")

if __name__ == "__main__":
    check_status()






