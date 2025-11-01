@echo off
echo ========================================
echo  Запуск MIXTRIX Bot
echo ========================================
echo.

REM Проверка наличия Python
where py >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python не найден!
    echo Установите Python 3.11 или выше
    pause
    exit /b 1
)

echo [OK] Python найден
echo.

REM Проверка файла env_file.txt
if not exist env_file.txt (
    echo [ERROR] Файл env_file.txt не найден!
    echo Создайте файл с переменными окружения
    pause
    exit /b 1
)

echo [OK] Файл env_file.txt найден
echo.

REM Запуск бота
echo [INFO] Запуск бота...
echo ========================================
echo.

py -3.11 bot.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Ошибка при запуске бота!
    echo.
    pause
)

