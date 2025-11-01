@echo off
chcp 65001 >nul
echo ============================================
echo ЗАПУСК COCKTAIL BOT
echo ============================================
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo.
echo Проверка конфигурации...
python start_bot_check.py
pause




