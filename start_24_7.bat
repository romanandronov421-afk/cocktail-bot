@echo off
title MIXTRIX Bot Manager 24/7
color 0A

echo.
echo  ███╗   ███╗██╗██╗  ██╗████████╗██████╗ ██╗██╗  ██╗
echo  ████╗ ████║██║╚██╗██╔╝╚══██╔══╝██╔══██╗██║╚██╗██╔╝
echo  ██╔████╔██║██║ ╚███╔╝   ██║   ██████╔╝██║ ╚███╔╝ 
echo  ██║╚██╔╝██║██║ ██╔██╗   ██║   ██╔══██╗██║ ██╔██╗ 
echo  ██║ ╚═╝ ██║██║██╔╝ ██╗  ██║   ██║  ██║██║██╔╝ ██╗
echo  ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝  ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
echo.
echo  🍸 Bot Manager 24/7 - Автоматический перезапуск
echo  ================================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo Установите Python с https://python.org
    pause
    exit /b 1
)

REM Проверяем наличие файлов
if not exist "bot.py" (
    echo ❌ bot.py не найден!
    pause
    exit /b 1
)

if not exist "env_file.txt" (
    echo ❌ env_file.txt не найден!
    pause
    exit /b 1
)

echo ✅ Все файлы найдены
echo ✅ Python доступен

echo.
echo 🚀 Запуск бота в режиме 24/7...
echo 📱 Для остановки нажмите Ctrl+C
echo.

REM Запускаем менеджер бота
python bot_manager_24_7.py

echo.
echo 👋 Бот остановлен
pause






