# discord-webhook-async

**discord-webhook-async** — это асинхронная библиотека для работы с Discord Webhooks на Python. Библиотека использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет удобный API для отправки текстовых сообщений, embed-сообщений, файлов, редактирования сообщений и получения информации о webhook.

## Особенности

- **Отправка текстовых сообщений**: Отправка простых текстовых сообщений через Discord Webhook.
- **Отправка Embed-сообщений**: Создание и отправка сообщений с поддержкой форматирования в Discord (Embed).
- **Отправка файлов**: Легкая отправка файлов через webhook с возможностью прикреплять описание.
- **Редактирование сообщений**: Возможность редактировать уже отправленные сообщения по ID.
- **Удаление сообщений**: Удаление сообщений по ID.
- **Получение информации о webhook**: Получение метаданных о webhook (например, имя, аватар).
- **Поддержка повторных попыток**: Встроенная поддержка автоматических повторных попыток в случае ошибок с экспоненциальной задержкой.
- **Гибкость и настройка**: Возможность настроить параметры webhook и методы отправки.

## Установка

Для установки библиотеки выполните следующую команду:

```bash
pip install discord-webhook-async
```

## Пример использования
1. **Отправка текстового сообщения**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Отправляем текстовое сообщение
    response = await webhook.send_message(content="Hello, Discord!")
    print(response)

    await webhook.close()

asyncio.run(main())
```
2. **Отправка Embed-сообщения**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Создание и отправка Embed-сообщения
    embed_response = await webhook.send_embed(
        title="Embed Title", 
        description="This is an embed description", 
        color=0xFF5733, 
        footer="Footer Text",
        image_url="https://example.com/image.jpg",
        thumbnail_url="https://example.com/thumbnail.jpg"
    )
    print(embed_response)

    await webhook.close()

asyncio.run(main())
```
3. **Отправка файла**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Отправка файла
    file_response = await webhook.send_file('path/to/your/file.txt', content="Here is a file!")
    print(file_response)

    await webhook.close()

asyncio.run(main())
```
4. **Редактирование сообщения**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Редактирование сообщения по ID
    message_id = "your_message_id"
    edit_response = await webhook.edit_message(message_id, content="Updated content")
    print(edit_response)

    await webhook.close()

asyncio.run(main())
```
5. **Удаление сообщения**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Удаление сообщения по ID
    delete_response = await webhook.delete_message(message_id="your_message_id")
    print(delete_response)

    await webhook.close()

asyncio.run(main())
```
6. **Получение информации о webhook**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Получение информации о webhook
    info_response = await webhook.get_webhook_info()
    print(info_response)

    await webhook.close()

asyncio.run(main())
```
## Настройки и параметры
1) **url**: URL вебхука (обязательный параметр при инициализации).
2) **retries**: Количество попыток повторных запросов в случае ошибок (по умолчанию 3).
3) **backoff_factor**: Множитель для экспоненциального увеличения времени ожидания между повторными попытками (по умолчанию 1.0).
4) **session**: Сессия aiohttp, создаваемая при первом запросе, или можно передать свою сессию для многократных запросов.
## Логирование
Библиотека использует стандартный модуль Python logging для логирования ошибок и событий. Вы можете настроить уровень логирования, указав параметры конфигурации logging.

Пример настройки логирования:
```python
import logging

logging.basicConfig(level=logging.DEBUG)  # Уровень логирования
```
## Обработка ошибок и повторные попытки
В случае временных ошибок (например, сетевых проблем) библиотека будет автоматически повторять запросы.
Количество попыток и время между ними можно настроить через параметры retries и backoff_factor.
## Лицензия
**Этот проект лицензирован под лицензией MIT.**
## Вклад в проект
Если вы хотите внести свой вклад, пожалуйста, создайте форк репозитория, внесите изменения и отправьте Pull Request.
## Контакты
Если у вас есть вопросы или предложения, вы можете обратиться по адресу электронной почты: ap4k43@gmail.com.
