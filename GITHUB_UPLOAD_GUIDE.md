# 🍹 Инструкция по загрузке проекта на GitHub

## Проблема
GitHub блокирует загрузку из-за обнаружения API ключей в истории коммитов. Даже после удаления секретов из файлов, GitHub помнит старые коммиты.

## Решение

### Вариант 1: Создать новый репозиторий на GitHub

1. **Перейдите на GitHub.com** и создайте новый репозиторий:
   - Нажмите "New repository"
   - Название: `cocktail-bot-clean`
   - Сделайте репозиторий публичным или приватным (на ваш выбор)
   - НЕ инициализируйте с README, .gitignore или лицензией

2. **Загрузите файлы через веб-интерфейс**:
   - Перейдите в созданный репозиторий
   - Нажмите "uploading an existing file"
   - Перетащите все файлы из папки проекта (кроме .git, venv, __pycache__)
   - Добавьте коммит сообщение: "Initial commit - Cocktail Bot project"
   - Нажмите "Commit changes"

### Вариант 2: Использовать GitHub CLI

Если у вас установлен GitHub CLI:

```bash
# Создать новый репозиторий
gh repo create cocktail-bot-clean --public

# Добавить файлы
git add .
git commit -m "Initial commit - Cocktail Bot project"
git push origin main
```

### Вариант 3: Отключить защиту от секретов

1. Перейдите в настройки репозитория: `https://github.com/romanandronov421-afk/cocktail-bot/settings`
2. В разделе "Security" найдите "Secret scanning"
3. Временно отключите "Push protection"
4. Попробуйте загрузить снова

## Файлы для загрузки

Убедитесь, что загружаете все эти файлы:
- ✅ Все .py файлы (bot.py, main.py, database.py и т.д.)
- ✅ Все .md файлы (документация)
- ✅ Конфигурационные файлы (.ini, .env, .yaml)
- ✅ requirements.txt
- ✅ .gitignore
- ❌ НЕ загружайте: .git папку, venv папку, __pycache__ папки

## После загрузки

1. **Создайте файл .env** с вашими реальными ключами:
```env
YANDEX_API_KEY=ваш_реальный_yandex_api_ключ
TELEGRAM_BOT_TOKEN=ваш_реальный_telegram_токен
FOLDER_ID=ваш_folder_id
```

2. **Обновите конфигурационные файлы** с реальными значениями

3. **Установите зависимости**:
```bash
pip install -r requirements.txt
```

4. **Запустите бота**:
```bash
python bot.py
```

## Альтернативное решение

Если ничего не помогает, можно:
1. Создать новый аккаунт GitHub
2. Создать новый репозиторий там
3. Загрузить файлы

---

**Примечание**: Все секретные данные уже заменены на заглушки (YOUR_YANDEX_API_KEY, YOUR_TELEGRAM_BOT_TOKEN) для безопасности.
