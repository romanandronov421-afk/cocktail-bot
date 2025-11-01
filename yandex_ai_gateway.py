"""
Yandex Cloud AI API Gateway Integration
Интеграция с API Gateway для работы с моделями Yandex GPT
"""

import os
import json
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

@dataclass
class Message:
    """Класс для представления сообщения в чате"""
    role: str  # system, user, assistant
    content: str

@dataclass
class ChatCompletionRequest:
    """Класс для запроса завершения чата"""
    model: str
    messages: List[Message]
    max_tokens: int = 100
    temperature: float = 0.7
    top_p: float = 0.9
    stream: bool = False

@dataclass
class ChatCompletionResponse:
    """Класс для ответа завершения чата"""
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

class YandexAIGatewayClient:
    """Клиент для работы с Yandex Cloud AI через API Gateway"""
    
    def __init__(self, api_gateway_url: str, api_key: str):
        """
        Инициализация клиента
        
        Args:
            api_gateway_url: URL API Gateway
            api_key: API ключ для аутентификации
        """
        self.api_gateway_url = api_gateway_url.rstrip('/')
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Асинхронный контекстный менеджер - вход"""
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер - выход"""
        if self.session:
            await self.session.close()
    
    async def create_chat_completion(
        self, 
        request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        """
        Создание завершения чата
        
        Args:
            request: Запрос на завершение чата
            
        Returns:
            Ответ с завершением чата
            
        Raises:
            aiohttp.ClientError: Ошибка HTTP запроса
            ValueError: Ошибка валидации данных
        """
        if not self.session:
            raise RuntimeError("Сессия не инициализирована. Используйте async with.")
        
        # Подготавливаем данные запроса
        request_data = {
            "model": request.model,
            "messages": [
                {"role": msg.role, "content": msg.content} 
                for msg in request.messages
            ],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "stream": request.stream
        }
        
        try:
            async with self.session.post(
                f"{self.api_gateway_url}/v1/chat/completions",
                json=request_data
            ) as response:
                response.raise_for_status()
                response_data = await response.json()
                
                return ChatCompletionResponse(
                    id=response_data.get("id", ""),
                    object=response_data.get("object", ""),
                    created=response_data.get("created", 0),
                    model=response_data.get("model", ""),
                    choices=response_data.get("choices", []),
                    usage=response_data.get("usage", {})
                )
                
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Ошибка HTTP запроса: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка парсинга JSON ответа: {e}")
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """
        Получение списка доступных моделей
        
        Returns:
            Список доступных моделей
            
        Raises:
            aiohttp.ClientError: Ошибка HTTP запроса
        """
        if not self.session:
            raise RuntimeError("Сессия не инициализирована. Используйте async with.")
        
        try:
            async with self.session.get(
                f"{self.api_gateway_url}/v1/models"
            ) as response:
                response.raise_for_status()
                response_data = await response.json()
                return response_data.get("data", [])
                
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Ошибка HTTP запроса: {e}")
    
    async def stream_chat_completion(
        self, 
        request: ChatCompletionRequest
    ):
        """
        Потоковое создание завершения чата
        
        Args:
            request: Запрос на завершение чата
            
        Yields:
            Части ответа в потоковом режиме
        """
        if not self.session:
            raise RuntimeError("Сессия не инициализирована. Используйте async with.")
        
        # Включаем потоковый режим
        request.stream = True
        
        request_data = {
            "model": request.model,
            "messages": [
                {"role": msg.role, "content": msg.content} 
                for msg in request.messages
            ],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "stream": True
        }
        
        try:
            async with self.session.post(
                f"{self.api_gateway_url}/v1/chat/completions",
                json=request_data
            ) as response:
                response.raise_for_status()
                
                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data: '):
                        data = line[6:]  # Убираем префикс 'data: '
                        if data == '[DONE]':
                            break
                        try:
                            yield json.loads(data)
                        except json.JSONDecodeError:
                            continue
                            
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Ошибка HTTP запроса: {e}")

class YandexAIService:
    """Сервис для работы с Yandex AI через API Gateway"""
    
    def __init__(self):
        """Инициализация сервиса"""
        self.api_key = os.getenv('YANDEX_API_KEY')
        self.folder_id = os.getenv('FOLDER_ID')
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        
        if not self.api_key:
            raise ValueError("YANDEX_API_KEY не найден в переменных окружения")
        if not self.folder_id:
            raise ValueError("FOLDER_ID не найден в переменных окружения")
    
    async def generate_response(
        self, 
        user_message: str, 
        system_prompt: str = "",
        max_tokens: int = 100,
        temperature: float = 0.7
    ) -> str:
        """
        Генерация ответа на сообщение пользователя
        
        Args:
            user_message: Сообщение пользователя
            system_prompt: Системный промпт (опционально)
            max_tokens: Максимальное количество токенов
            temperature: Температура генерации
            
        Returns:
            Сгенерированный ответ
        """
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "text": system_prompt})
        messages.append({"role": "user", "text": user_message})
        
        data = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": temperature,
                "maxTokens": max_tokens
            },
            "messages": messages
        }
        
        try:
            import requests
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if 'result' in result and 'alternatives' in result['result']:
                return result['result']['alternatives'][0]['message']['text']
            else:
                return "Ошибка: неожиданный формат ответа от Yandex API"
                
        except requests.exceptions.Timeout:
            return "Ошибка: превышено время ожидания ответа от Yandex API"
        except requests.exceptions.ConnectionError:
            return "Ошибка: нет подключения к Yandex API"
        except requests.exceptions.HTTPError as e:
            return f"Ошибка HTTP: {e.response.status_code}"
        except Exception as e:
            return f"Ошибка при обращении к Yandex AI: {str(e)}"

# Пример использования
async def main():
    """Пример использования сервиса"""
    try:
        service = YandexAIService()
        
        # Простой запрос
        response = await service.generate_response(
            "Привет! Расскажи мне о коктейлях.",
            max_tokens=200,
            temperature=0.8
        )
        print(f"Ответ: {response}")
        
        # Запрос с системным промптом
        response = await service.generate_response(
            "Какой коктейль лучше всего подходит для вечеринки?",
            system_prompt="Ты эксперт по коктейлям и бармен.",
            max_tokens=150
        )
        print(f"Экспертный ответ: {response}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())





