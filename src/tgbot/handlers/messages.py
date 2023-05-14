"""
This module contains handlers that handle messages from users

Handlers:
    echo    - echoes the user's message

Note:
    Routers are imported into the __init__.py package handlers,
    where a tuple of ROUTERS is assembled for further registration in the dispatcher
"""

from aiogram import F, Router
from aiogram.types import Message


# Create router
msg_router = Router(name="msg_router")


async def echo(message: Message) -> None:
    """Responds to echoing messages"""
    await message.reply(text=f"<pre>{message.text}</pre>")


# Register routers
msg_router.message.register(echo, F.text)
