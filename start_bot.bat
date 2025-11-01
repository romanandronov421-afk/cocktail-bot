@echo off
echo 🍸 Запуск MIXTRIX Bot...
echo ================================

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
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
echo 🚀 Запускаем бота MIXTRIX...
echo.

REM Запускаем бота
python bot.py

echo.
echo 🎉 Бот завершил работу
pause






