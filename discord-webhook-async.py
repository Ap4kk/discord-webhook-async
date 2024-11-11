import aiohttp
import asyncio
import logging
import time
from typing import Optional, Dict, Any, List

# Конфигурация логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DiscordWebhook:
    def __init__(self, url: str, retries: int = 3, backoff_factor: float = 1.0):
        """
        Инициализация вебхука.

        :param url: URL вебхука.
        :param retries: Количество попыток повторного запроса при ошибке.
        :param backoff_factor: Множитель для экспоненциального времени ожидания между повторными попытками.
        """
        self.url = url
        self.session = None
        self.retries = retries
        self.backoff_factor = backoff_factor

    async def _get_session(self):
        """Создаёт сессию при первом запросе и возвращает её."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        """Закрывает сессию."""
        if self.session:
            await self.session.close()

    async def send_message(self, content: Optional[str] = None, username: Optional[str] = None,
                           avatar_url: Optional[str] = None, embed: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Отправляет сообщение в Discord webhook."""
        payload = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url,
            "embeds": [embed] if embed else None
        }
        return await self._send_request(payload)

    async def send_embed(self, title: str, description: str, color: int = 0x000000,
                         fields: Optional[List[Dict[str, Any]]] = None, footer: Optional[str] = None,
                         image_url: Optional[str] = None, thumbnail_url: Optional[str] = None) -> Dict[str, Any]:
        """Отправляет embed сообщение с дополнительными возможностями."""
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "fields": fields if fields else [],
            "footer": {"text": footer} if footer else None,
            "image": {"url": image_url} if image_url else None,
            "thumbnail": {"url": thumbnail_url} if thumbnail_url else None
        }
        return await self.send_message(embed=embed)

    async def send_file(self, file_path: str, content: Optional[str] = None, username: Optional[str] = None,
                        avatar_url: Optional[str] = None) -> Dict[str, Any]:
        """Отправляет файл через webhook."""
        async with aiohttp.ClientSession() as session:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'content': content,
                    'username': username,
                    'avatar_url': avatar_url
                }
                return await self._send_request(data, files=files, session=session)

    async def edit_message(self, message_id: str, content: Optional[str] = None,
                           username: Optional[str] = None, avatar_url: Optional[str] = None,
                           embed: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Редактирует уже отправленное сообщение по его ID."""
        payload = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url,
            "embeds": [embed] if embed else None
        }
        edit_url = f"{self.url}/messages/{message_id}"
        return await self._send_request(payload, method='PATCH', url=edit_url)

    async def delete_message(self, message_id: str) -> Dict[str, Any]:
        """Удаляет сообщение по его ID."""
        delete_url = f"{self.url}/messages/{message_id}"
        return await self._send_request({}, method='DELETE', url=delete_url)

    async def get_webhook_info(self) -> Dict[str, Any]:
        """Получает информацию о webhook (например, имя, аватар)."""
        return await self._send_request({}, method='GET')

    async def _send_request(self, data: Dict[str, Any], method: str = 'POST', files: Optional[dict] = None,
                            session: Optional[aiohttp.ClientSession] = None, url: Optional[str] = None) -> Dict[str, Any]:
        """Отправляет запрос на webhook с указанным методом с повторными попытками в случае ошибок."""
        url = url or self.url
        session = session or await self._get_session()
        attempt = 0
        while attempt <= self.retries:
            try:
                async with session.request(method, url, data=data, files=files) as response:
                    response.raise_for_status()  # Поднимет ошибку для плохого статуса
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                logging.error(f"Ошибка HTTP: {e.status} - {e.message}")
                if attempt == self.retries:
                    return {"error": f"Max retries reached: {e.message}"}
            except aiohttp.ClientError as e:
                logging.error(f"Ошибка при отправке запроса: {e}")
                if attempt == self.retries:
                    return {"error": f"Request failed: {e}"}
            except Exception as e:
                logging.error(f"Непредвиденная ошибка: {e}")
                if attempt == self.retries:
                    return {"error": f"Unexpected error: {e}"}
            
            # Экспоненциальная задержка перед повторной попыткой
            attempt += 1
            backoff_time = self.backoff_factor * (2 ** attempt)  # Экспоненциальный бэкофф
            logging.info(f"Повторная попытка через {backoff_time} секунд...")
            time.sleep(backoff_time)
            
# Пример использования
async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Отправка сообщения
    response = await webhook.send_message(content="Hello, Discord!")
    print(response)

    # Отправка embed
    embed_response = await webhook.send_embed(
        title="Embed Title", 
        description="This is an embed description", 
        color=0xFF5733, 
        footer="Footer Text"
    )
    print(embed_response)

    # Редактирование сообщения
    message_id = "your_message_id"
    edit_response = await webhook.edit_message(message_id, content="Updated content")
    print(edit_response)

    # Удаление сообщения
    delete_response = await webhook.delete_message(message_id)
    print(delete_response)

    # Получение информации о webhook
    info_response = await webhook.get_webhook_info()
    print(info_response)

    await webhook.close()

# Запуск
asyncio.run(main())
