#!/usr/bin/env python3
"""
Скрипт для запуска бота MIXTRIX в режиме 24/7
с автоматическим перезапуском при ошибках
"""

import os
import sys
import time
import subprocess
import signal
from datetime import datetime

class BotManager:
    """Менеджер для управления ботом 24/7"""
    
    def __init__(self):
        self.bot_process = None
        self.restart_count = 0
        self.max_restarts = 10  # Максимум перезапусков за час
        self.restart_window = 3600  # Окно времени в секундах
        self.last_restart_time = 0
        
    def log(self, message):
        """Логирование с временной меткой"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def start_bot(self):
        """Запуск бота"""
        try:
            self.log("🍸 Запуск MIXTRIX Bot...")
            
            # Проверяем наличие файлов
            if not os.path.exists('bot.py'):
                self.log("❌ Файл bot.py не найден!")
                return False
                
            if not os.path.exists('env_file.txt'):
                self.log("❌ Файл env_file.txt не найден!")
                return False
            
            # Запускаем бота как отдельный процесс
            self.bot_process = subprocess.Popen(
                [sys.executable, 'bot.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.log("✅ Бот успешно запущен!")
            self.log(f"📊 PID процесса: {self.bot_process.pid}")
            return True
            
        except Exception as e:
            self.log(f"❌ Ошибка запуска бота: {e}")
            return False
    
    def stop_bot(self):
        """Остановка бота"""
        if self.bot_process:
            try:
                self.log("🛑 Остановка бота...")
                self.bot_process.terminate()
                
                # Ждем завершения процесса
                try:
                    self.bot_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.log("⚠️ Принудительное завершение процесса...")
                    self.bot_process.kill()
                    self.bot_process.wait()
                
                self.log("✅ Бот остановлен")
                self.bot_process = None
                
            except Exception as e:
                self.log(f"❌ Ошибка остановки бота: {e}")
    
    def is_bot_running(self):
        """Проверка, работает ли бот"""
        if self.bot_process is None:
            return False
            
        # Проверяем статус процесса
        poll = self.bot_process.poll()
        return poll is None
    
    def can_restart(self):
        """Проверка, можно ли перезапустить бота"""
        current_time = time.time()
        
        # Если прошло больше часа с последнего перезапуска, сбрасываем счетчик
        if current_time - self.last_restart_time > self.restart_window:
            self.restart_count = 0
        
        return self.restart_count < self.max_restarts
    
    def restart_bot(self):
        """Перезапуск бота"""
        if not self.can_restart():
            self.log("❌ Превышено максимальное количество перезапусков!")
            return False
        
        self.restart_count += 1
        self.last_restart_time = time.time()
        
        self.log(f"🔄 Перезапуск бота (попытка {self.restart_count}/{self.max_restarts})...")
        
        self.stop_bot()
        time.sleep(5)  # Пауза перед перезапуском
        
        return self.start_bot()
    
    def monitor_bot(self):
        """Мониторинг работы бота"""
        self.log("🚀 Запуск мониторинга бота 24/7...")
        self.log("📱 Для остановки нажмите Ctrl+C")
        
        # Запускаем бота
        if not self.start_bot():
            self.log("❌ Не удалось запустить бота!")
            return
        
        try:
            while True:
                time.sleep(30)  # Проверяем каждые 30 секунд
                
                if not self.is_bot_running():
                    self.log("⚠️ Бот остановлен! Перезапускаем...")
                    
                    if not self.restart_bot():
                        self.log("❌ Не удалось перезапустить бота!")
                        break
                else:
                    # Бот работает нормально
                    if self.restart_count > 0:
                        self.log("✅ Бот работает стабильно")
                        self.restart_count = 0  # Сбрасываем счетчик при стабильной работе
                
        except KeyboardInterrupt:
            self.log("🛑 Получен сигнал остановки...")
            self.stop_bot()
            self.log("👋 Мониторинг остановлен")
        except Exception as e:
            self.log(f"❌ Критическая ошибка: {e}")
            self.stop_bot()

def main():
    """Основная функция"""
    print("🍸 MIXTRIX Bot Manager 24/7")
    print("=" * 50)
    
    # Проверяем Python
    print(f"✅ Python версия: {sys.version}")
    
    # Проверяем файлы
    required_files = ['bot.py', 'env_file.txt']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - найден")
        else:
            print(f"❌ {file} - не найден!")
            return
    
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
            print("❌ Переменные окружения не настроены!")
            return
            
    except Exception as e:
        print(f"❌ Ошибка загрузки переменных: {e}")
        return
    
    print("\n🎯 Возможности бота:")
    print("• Фудпейринг на основе The Flavor Bible")
    print("• 300+ вкусовых комбинаций")
    print("• Интеграция всех профессиональных источников")
    print("• Сезонные рекомендации для России")
    print("• Автоматический перезапуск при ошибках")
    
    print("\n🚀 Запуск в режиме 24/7...")
    
    # Создаем менеджер и запускаем мониторинг
    manager = BotManager()
    manager.monitor_bot()

if __name__ == "__main__":
    main()






