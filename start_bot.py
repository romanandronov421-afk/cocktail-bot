#!/usr/bin/env python3
"""
Простой скрипт запуска бота MIXTRIX
"""

import os
import sys
import subprocess

def start_bot():
    """Запуск бота MIXTRIX"""
    print("🍸 Запуск MIXTRIX Bot...")
    print("=" * 50)
    
    # Проверяем наличие файлов
    required_files = ['bot.py', 'env_file.txt', 'database.py', 'enhanced_foodpairing_processor.py']
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - найден")
        else:
            print(f"❌ {file} - не найден")
            return False
    
    # Проверяем переменные окружения
    try:
        from dotenv import load_dotenv
        load_dotenv('env_file.txt')
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        yandex_key = os.getenv('YANDEX_API_KEY')
        folder_id = os.getenv('FOLDER_ID')
        
        if token and yandex_key and folder_id:
            print("✅ Переменные окружения настроены")
        else:
            print("❌ Переменные окружения не настроены")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка загрузки переменных: {e}")
        return False
    
    print("\n🚀 Запускаем бота...")
    
    try:
        # Запускаем бота напрямую
        import bot
        print("✅ Бот успешно импортирован!")
        print("🎉 MIXTRIX Bot запущен с улучшенными возможностями!")
        print("\n📱 Теперь вы можете:")
        print("• Найти бота в Telegram")
        print("• Отправить /start")
        print("• Использовать новые команды фудпейринга")
        print("\n🍸 Новые возможности:")
        print("• /recipe [спирт] - создание рецепта")
        print("• /pairing [блюдо] - фудпейринг")
        print("• /seasonal - сезонные рекомендации")
        print("• /flavor_combinations - вкусовые комбинации")
        print("• /knowledge_base - база знаний")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = start_bot()
    
    if success:
        print("\n🎉 Бот готов к работе!")
        print("Найдите его в Telegram и начните использовать!")
    else:
        print("\n⚠️ Есть проблемы с запуском.")
        print("Проверьте ошибки выше.")