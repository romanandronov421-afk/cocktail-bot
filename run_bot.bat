@echo off
title MIXTRIX Bot - Прямой запуск
color 0A

echo.
echo  ███╗   ███╗██╗██╗  ██╗████████╗██████╗ ██╗██╗  ██╗
echo  ████╗ ████║██║╚██╗██╔╝╚══██╔══╝██╔══██╗██║╚██╗██╔╝
echo  ██╔████╔██║██║ ╚███╔╝   ██║   ██████╔╝██║ ╚███╔╝ 
echo  ██║╚██╔╝██║██║ ██╔██╗   ██║   ██╔══██╗██║ ██╔██╗ 
echo  ██║ ╚═╝ ██║██║██╔╝ ██╗  ██║   ██║  ██║██║██╔╝ ██╗
echo  ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝  ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
echo.
echo  🍸 Прямой запуск бота
echo  ====================
echo.

REM Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo Установите Python с https://python.org
    pause
    exit /b 1
)

REM Проверяем файлы
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
echo 🚀 Запуск бота...
echo.

REM Запускаем бота напрямую
python run_bot_direct.py

echo.
echo 👋 Бот остановлен
pause






