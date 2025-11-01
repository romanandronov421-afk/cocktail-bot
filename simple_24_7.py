#!/usr/bin/env python3
"""
Простой скрипт для запуска бота MIXTRIX в режиме 24/7
"""

import os
import sys
import time
import subprocess
import signal
from datetime import datetime

def log(message):
    """Логирование с временной меткой"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def start_bot_24_7():
    """Запуск бота в режиме 24/7"""
    log("🍸 Запуск MIXTRIX Bot в режиме 24/7...")
    
    # Проверяем файлы
    if not os.path.exists('bot.py'):
        log("❌ Файл bot.py не найден!")
        return False
        
    if not os.path.exists('env_file.txt'):
        log("❌ Файл env_file.txt не найден!")
        return False
    
    log("✅ Все файлы найдены")
    
    restart_count = 0
    max_restarts = 5
    
    while restart_count < max_restarts:
        try:
            log(f"🚀 Запуск бота (попытка {restart_count + 1}/{max_restarts})...")
            
            # Запускаем бота
            process = subprocess.Popen(
                [sys.executable, 'bot.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            log(f"✅ Бот запущен! PID: {process.pid}")
            log("📱 Бот работает 24/7. Для остановки нажмите Ctrl+C")
            
            # Ждем завершения процесса
            process.wait()
            
            log("⚠️ Бот остановлен. Перезапускаем через 10 секунд...")
            restart_count += 1
            
            if restart_count < max_restarts:
                time.sleep(10)
            else:
                log("❌ Превышено максимальное количество перезапусков!")
                break
                
        except KeyboardInterrupt:
            log("🛑 Получен сигнал остановки...")
            if 'process' in locals():
                process.terminate()
            log("👋 Бот остановлен")
            break
        except Exception as e:
            log(f"❌ Ошибка: {e}")
            restart_count += 1
            if restart_count < max_restarts:
                log("🔄 Перезапуск через 10 секунд...")
                time.sleep(10)
            else:
                log("❌ Критическая ошибка! Остановка.")
                break
    
    return True

def main():
    """Основная функция"""
    print("🍸 MIXTRIX Bot 24/7")
    print("=" * 30)
    
    # Проверяем Python
    print(f"✅ Python: {sys.version}")
    
    # Проверяем переменные окружения
    try:
        from dotenv import load_dotenv
        load_dotenv('env_file.txt')
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if token:
            print("✅ Telegram Bot Token настроен")
        else:
            print("❌ Telegram Bot Token не настроен!")
            return
            
    except Exception as e:
        print(f"❌ Ошибка загрузки переменных: {e}")
        return
    
    print("\n🎯 Возможности:")
    print("• Фудпейринг на основе The Flavor Bible")
    print("• 300+ вкусовых комбинаций")
    print("• Автоматический перезапуск при ошибках")
    print("• Работа 24/7")
    
    print("\n🚀 Запуск...")
    
    # Запускаем бота
    start_bot_24_7()

if __name__ == "__main__":
    main()






