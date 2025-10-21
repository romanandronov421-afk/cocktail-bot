# 🔗 Интеграция с GitHub

## 📁 Структура репозитория

```
cocktail-bot/
├── bot.py                 # Основной файл бота
├── database.py            # Работа с базой данных
├── run_bot.py            # Скрипт запуска
├── requirements.txt       # Зависимости Python
├── .env                  # Переменные окружения (НЕ коммитить!)
├── cocktails.db          # База данных SQLite
├── README.md             # Основная документация
├── QUICK_START.md        # Быстрый старт
├── DEPLOYMENT.md         # Инструкции по развертыванию
├── EXAMPLES.md           # Примеры использования
├── GITHUB_INTEGRATION.md # Этот файл
└── venv/                 # Виртуальное окружение (НЕ коммитить!)
```

## 🚫 Файлы для .gitignore

Создайте файл `.gitignore`:
```gitignore
# Переменные окружения
.env

# Виртуальное окружение
venv/
env/
ENV/

# База данных (опционально)
cocktails.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# Логи
*.log

# Временные файлы
*.tmp
*.temp
```

## 🔧 Настройка репозитория

### 1. Инициализация Git
```bash
git init
git add .
git commit -m "Initial commit: MixMatrixBot with AI integration"
```

### 2. Подключение к GitHub
```bash
git remote add origin https://github.com/romanandronov421-afk/cocktail-bot.git
git branch -M main
git push -u origin main
```

### 3. Настройка веток
```bash
# Создание ветки для разработки
git checkout -b develop

# Создание ветки для функций
git checkout -b feature/new-commands
```

## 🔐 Настройка секретов

### GitHub Secrets
В настройках репозитория добавьте:
- `TELEGRAM_BOT_TOKEN` - токен бота
- `XAI_API_KEY` - ключ XAI API
- `DATABASE_URL` - URL базы данных (для продакшена)

### Локальная разработка
Создайте `.env.example`:
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# XAI API Configuration
XAI_API_KEY=your_xai_api_key_here

# Other Configuration
DEBUG=False
```

## 🚀 CI/CD с GitHub Actions

Создайте `.github/workflows/deploy.yml`:
```yaml
name: Deploy MixMatrixBot

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to server
      run: |
        # Ваши команды развертывания
        echo "Deploying to production..."
```

## 📋 Issues и Project Management

### Шаблоны Issues
Создайте `.github/ISSUE_TEMPLATE/bug_report.md`:
```markdown
---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows, Linux, macOS]
 - Python version: [e.g. 3.11]
 - Bot version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### Шаблон Pull Request
Создайте `.github/pull_request_template.md`:
```markdown
## Описание изменений
Краткое описание того, что было изменено.

## Тип изменений
- [ ] Исправление бага
- [ ] Новая функция
- [ ] Изменение документации
- [ ] Рефакторинг
- [ ] Другое

## Чеклист
- [ ] Код протестирован
- [ ] Документация обновлена
- [ ] Нет конфликтов с main
- [ ] Все тесты проходят

## Дополнительная информация
Любая дополнительная информация для ревьюера.
```

## 🏷️ Управление версиями

### Семантическое версионирование
- `MAJOR` - кардинальные изменения
- `MINOR` - новые функции
- `PATCH` - исправления багов

### Создание релизов
```bash
# Создание тега
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Создание релиза на GitHub
gh release create v1.0.0 --title "MixMatrixBot v1.0.0" --notes "Первая версия бота"
```

## 📊 Мониторинг и аналитика

### GitHub Insights
- **Traffic** - статистика просмотров
- **Contributors** - участники проекта
- **Commits** - активность разработки
- **Code frequency** - частота изменений

### Интеграции
- **Codecov** - покрытие кода тестами
- **Dependabot** - обновления зависимостей
- **GitHub Security** - проверка уязвимостей

## 🤝 Сотрудничество

### Code Review
1. Создайте Pull Request
2. Назначьте ревьюеров
3. Обсудите изменения
4. Внесите правки
5. Смержите после одобрения

### Contributing Guidelines
Создайте `CONTRIBUTING.md`:
```markdown
# Руководство по участию

## Как внести вклад
1. Форкните репозиторий
2. Создайте ветку для функции
3. Внесите изменения
4. Создайте Pull Request

## Стандарты кода
- Используйте PEP 8
- Добавляйте docstrings
- Покрывайте код тестами

## Процесс разработки
1. Обсудите изменения в Issue
2. Создайте ветку
3. Реализуйте функцию
4. Напишите тесты
5. Обновите документацию
```

## 📚 Документация

### README.md
- Описание проекта
- Установка и запуск
- Примеры использования
- API документация

### Wiki
- Детальные инструкции
- FAQ
- Troubleshooting
- Roadmap

## 🔄 Workflow

### Основной процесс
1. **Feature branch** → разработка
2. **Pull Request** → код-ревью
3. **Merge to main** → интеграция
4. **Deploy** → развертывание
5. **Release** → релиз

### Ветки
- `main` - стабильная версия
- `develop` - разработка
- `feature/*` - новые функции
- `hotfix/*` - критические исправления

---

*Удачной разработки! 🍹*

