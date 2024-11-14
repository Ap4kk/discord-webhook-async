import aiohttp
import asyncio
import logging
import time
from typing import Optional, Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class DiscordWebhook:
    def __init__(self, url: str, retries: int = 3, backoff_factor: float = 1.0):
        """
        Initialize the webhook.

        :param url: Webhook URL.
        :param retries: Number of retries if a request fails.
        :param backoff_factor: Multiplier for exponential backoff time between retries.
        """
        self.url = url
        self.session = None
        self.retries = retries
        self.backoff_factor = backoff_factor

    async def _get_session(self):
        """Creates a session if one doesn't exist and returns it."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        """Closes the session."""
        if self.session:
            await self.session.close()

    async def send_message(self, content: Optional[str] = None, username: Optional[str] = None,
                           avatar_url: Optional[str] = None, embed: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Sends a message via the Discord webhook."""
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
        """Sends an embed message with additional formatting options."""
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
        """Sends a file via the webhook."""
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
        """Edits a previously sent message by its ID."""
        payload = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url,
            "embeds": [embed] if embed else None
        }
        edit_url = f"{self.url}/messages/{message_id}"
        return await self._send_request(payload, method='PATCH', url=edit_url)

    async def delete_message(self, message_id: str) -> Dict[str, Any]:
        """Deletes a message by its ID."""
        delete_url = f"{self.url}/messages/{message_id}"
        return await self._send_request({}, method='DELETE', url=delete_url)

    async def get_webhook_info(self) -> Dict[str, Any]:
        """Retrieves information about the webhook (e.g., name, avatar)."""
        return await self._send_request({}, method='GET')

    async def _send_request(self, data: Dict[str, Any], method: str = 'POST', files: Optional[dict] = None,
                            session: Optional[aiohttp.ClientSession] = None, url: Optional[str] = None) -> Dict[
        str, Any]:
        """Sends a request to the webhook with retries in case of errors."""
        url = url or self.url
        session = session or await self._get_session()
        attempt = 0
        while attempt <= self.retries:
            try:
                async with session.request(method, url, json=data) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                logging.error(f"HTTP Error: {e.status} - {e.message}")
                if attempt == self.retries:
                    return {"error": f"Max retries reached: {e.message}"}
            except aiohttp.ClientError as e:
                logging.error(f"Request failed: {e}")
                if attempt == self.retries:
                    return {"error": f"Request failed: {e}"}
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                if attempt == self.retries:
                    return {"error": f"Unexpected error: {e}"}

            attempt += 1
            backoff_time = self.backoff_factor * (2 ** attempt)
            logging.info(f"Retrying in {backoff_time} seconds...")
            await asyncio.sleep(backoff_time)
