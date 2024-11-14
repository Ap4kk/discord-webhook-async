# discord-webhook-async

**discord-webhook-async** is an asynchronous library for working with Discord Webhooks in Python. The library uses `aiohttp` to make asynchronous HTTP requests and provides a convenient API for sending text messages, embed messages, files, editing messages and getting information about the webhook.

## Features

- **Sending Text Messages**: Sending simple text messages via Discord Webhook.
- **Sending Embed Messages**: Create and send messages with support for formatting in Discord (Embed).
- **File Sending**: Easy file sending via webhook with the ability to attach a description.
- **Message editing**: The ability to edit already sent messages by ID.
- **Deleting messages**: Deleting messages by ID.
- **Getting information about the webhook**: Getting metadata about the webhook (for example, name, avatar).
- **Retry support**: Built-in support for automatic retries in case of exponential delay errors.
- **Flexibility and customization**: The ability to customize webhook settings and sending methods.

## Installation

To install the library, run the following command:

```bash
pip install discord-webhook-async
```

## Usage example
1. **Sending a text message**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Sending a text message
    response = await webhook.send_message(content="Hello, Discord!")
    print(response)

    await webhook.close()

asyncio.run(main())
```
2. **Sending an Embed Message**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Creating and sending an Embed Message
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
3. **Sending a file**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Sending a file
    file_response = await webhook.send_file('path/to/your/file.txt', content="Here is a file!")
    print(file_response)

    await webhook.close()

asyncio.run(main())
```
4. **Editing the message**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Editing a message by ID
    message_id = "your_message_id"
    edit_response = await webhook.edit_message(message_id, content="Updated content")
    print(edit_response)

    await webhook.close()

asyncio.run(main())
```
5. **Deleting a message**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Deleting a message by ID
    delete_response = await webhook.delete_message(message_id="your_message_id")
    print(delete_response)

    await webhook.close()

asyncio.run(main())
```
6. **Getting information about the webhook**
```python
import asyncio
from discord_webhook_async import DiscordWebhook

async def main():
    webhook = DiscordWebhook('https://discord.com/api/webhooks/your-webhook-url')

    # Getting information about the webhook
    info_response = await webhook.get_webhook_info()
    print(info_response)

    await webhook.close()

asyncio.run(main())
```
## Settings and Parameters
1) **url**: The URL of the webhook (required parameter during initialization).
2) **retries**: Number of retry attempts in case of errors (default is 3).
3) **backoff_factor**: Multiplier for exponentially increasing the waiting time between retries (default is 1.0).
4) **session**: aiohttp session created at the first request, or you can transfer your session for multiple requests.
## Logging
The library uses the standard Python logging module to log errors and events. You can configure the logging level by specifying the logging configuration parameters.

Example of logging settings:
``python
import logging

logging.basicConfig(level=logging.DEBUG) # Logging level
``
## Error handling and retries
In case of temporary errors (for example, network problems), the library will automatically repeat requests.
The number of attempts and the time between them can be configured via the retries and backoff_factor parameters.
## License
**This project is licensed under the MIT license.**
## Contribution to the project
If you want to contribute, please create a fork of the repository, make changes and send a Pull Request.
## Contacts
If you have any questions or suggestions, you can contact us by e-mail: ap4k43@gmail.com .
