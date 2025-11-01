@echo off
chcp 65001
echo === Диагностика бота MixMatrix ===
echo.

echo Проверяем Python...
python --version
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден
    pause
    exit /b 1
)

echo.
echo Проверяем зависимости...
python -c "import aiogram; print('aiogram OK')"
if %errorlevel% neq 0 (
    echo ОШИБКА: aiogram не установлен
    echo Установите: pip install aiogram
    pause
    exit /b 1
)

python -c "import requests; print('requests OK')"
if %errorlevel% neq 0 (
    echo ОШИБКА: requests не установлен
    echo Установите: pip install requests
    pause
    exit /b 1
)

python -c "from dotenv import load_dotenv; print('python-dotenv OK')"
if %errorlevel% neq 0 (
    echo ОШИБКА: python-dotenv не установлен
    echo Установите: pip install python-dotenv
    pause
    exit /b 1
)

echo.
echo Проверяем файлы...
if not exist "env_file.txt" (
    echo ОШИБКА: Файл env_file.txt не найден
    pause
    exit /b 1
)

if not exist "bot.py" (
    echo ОШИБКА: Файл bot.py не найден
    pause
    exit /b 1
)

if not exist "database.py" (
    echo ОШИБКА: Файл database.py не найден
    pause
    exit /b 1
)

echo.
echo Все проверки пройдены!
echo Запускаем диагностику...
python diagnose_bot.py

echo.
echo Диагностика завершена.
pause









