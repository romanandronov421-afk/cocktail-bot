@echo off
chcp 65001
echo === Установка зависимостей для бота ===
echo.

echo Устанавливаем aiogram...
pip install aiogram
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить aiogram
    pause
    exit /b 1
)

echo Устанавливаем requests...
pip install requests
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить requests
    pause
    exit /b 1
)

echo Устанавливаем python-dotenv...
pip install python-dotenv
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить python-dotenv
    pause
    exit /b 1
)

echo.
echo ✓ Все зависимости установлены успешно!
echo.
echo Проверяем файл env_file.txt...
if not exist "env_file.txt" (
    echo ОШИБКА: Файл env_file.txt не найден
    pause
    exit /b 1
)

echo ✓ Файл env_file.txt найден
echo.
echo Запускаем бота...
python bot_simple.py

pause









