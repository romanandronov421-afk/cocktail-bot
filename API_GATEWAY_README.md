# Yandex Cloud AI API Gateway

Полная конфигурация для развертывания API Gateway с интеграцией Yandex Cloud AI.

## Структура проекта

```
├── api-gateway-config.yaml    # OpenAPI спецификация
├── yandex_ai_gateway.py      # Python клиент для интеграции
├── docker-compose.yml        # Docker конфигурация
├── nginx.conf               # Nginx конфигурация
├── environment.env          # Переменные окружения
└── README.md               # Документация
```

## Быстрый старт

### 1. Настройка переменных окружения

Скопируйте файл `environment.env` в `.env` и заполните необходимые значения:

```bash
cp environment.env .env
```

Отредактируйте `.env`:
```env
# Yandex Cloud AI API Configuration
YANDEX_API_KEY=ваш_реальный_ключ
FOLDER_ID=ваш_реальный_folder_id

# API Gateway Configuration
API_GATEWAY_URL=https://your-api-gateway.url
API_GATEWAY_STAGING_URL=https://staging-api-gateway.url
```

### 2. Развертывание с Docker

```bash
# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

### 3. Проверка работы

```bash
# Health check
curl http://localhost:8080/health

# Тест API
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ваш_ключ" \
  -d '{
    "model": "yandexgpt",
    "messages": [{"role": "user", "content": "Привет!"}],
    "max_tokens": 100
  }'
```

## Конфигурация Cursor IDE

### Через настройки UI:

1. Откройте Cursor
2. Перейдите в Settings (`Ctrl + ,`)
3. Найдите раздел "AI Providers"
4. Выберите "Custom API"
5. Настройте:
   ```
   URL: https://llm.api.cloud.yandex.net/foundationModels/v1/completion
   API Key: ваш_API_ключ
   ```

### Через файл конфигурации:

Создайте файл `settings.json` в папке конфигурации Cursor:

```json
{
  "cursor.ai.provider": "custom",
  "cursor.ai.customApiUrl": "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
  "cursor.ai.customApiKey": "ваш_API_ключ"
}
```

## Использование Python клиента

```python
import asyncio
from yandex_ai_gateway import YandexAIService

async def main():
    service = YandexAIService()
    
    # Простой запрос
    response = await service.generate_response(
        "Расскажи о коктейлях",
        max_tokens=200,
        temperature=0.8
    )
    print(response)

asyncio.run(main())
```

## API Endpoints

### POST /v1/chat/completions

Создание завершения чата.

**Запрос:**
```json
{
  "model": "yandexgpt",
  "messages": [
    {"role": "user", "content": "Привет!"}
  ],
  "max_tokens": 100,
  "temperature": 0.7
}
```

**Ответ:**
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "yandexgpt",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Привет! Как дела?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

### GET /v1/models

Получение списка доступных моделей.

**Ответ:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "yandexgpt",
      "object": "model",
      "created": 1677610602,
      "owned_by": "yandex"
    }
  ]
}
```

## Безопасность

1. **Никогда не коммитьте API ключи** в репозиторий
2. **Используйте HTTPS** в продакшене
3. **Настройте CORS** правильно для вашего домена
4. **Ограничьте доступ** к API Gateway через firewall
5. **Мониторьте использование** API ключей

## Мониторинг

### Логи Nginx

```bash
# Просмотр логов доступа
docker-compose logs api-gateway

# Просмотр логов ошибок
docker-compose exec api-gateway tail -f /var/log/nginx/error.log
```

### Статус сервисов

```bash
# Статус всех контейнеров
docker-compose ps

# Статус Nginx
curl http://localhost:8080/nginx_status
```

## Troubleshooting

### Проблема: API ключ не работает

**Решение:**
1. Проверьте правильность API ключа в `.env`
2. Убедитесь, что ключ активен в Yandex Cloud
3. Проверьте права доступа к API

### Проблема: CORS ошибки

**Решение:**
1. Проверьте настройки CORS в `nginx.conf`
2. Убедитесь, что домен добавлен в разрешенные
3. Проверьте заголовки запроса

### Проблема: Таймауты

**Решение:**
1. Увеличьте таймауты в `nginx.conf`
2. Проверьте производительность backend сервиса
3. Мониторьте использование ресурсов

## Масштабирование

### Горизонтальное масштабирование

```yaml
# В docker-compose.yml
services:
  proxy-service:
    deploy:
      replicas: 3
```

### Вертикальное масштабирование

```yaml
# В docker-compose.yml
services:
  proxy-service:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

## Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs`
2. Проверьте статус сервисов: `docker-compose ps`
3. Проверьте конфигурацию: `docker-compose config`
4. Создайте issue в репозитории проекта



