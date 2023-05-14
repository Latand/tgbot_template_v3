"""
The module contains various filters that can be used in handlers

Example:
    Import the filter into the module with handlers:
        from tgbot.misc.filters import IsAdmin

    Create a router and add a filter to it:
        admin_router = Router()
        admin_router.message.filter(IsAdmin())

    Let's register the right handler with the decorator:
        @admin_router.message(CommandStart())
        async def admin_start(message: Message):
            await message.reply("Hello, admin!")
"""

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from tgbot.config import bot_config


class IsAdmin(BaseFilter):
    """The filter allows you to determine if the sender of the message is a bot administrator"""

    async def __call__(self, obj: CallbackQuery | Message) -> bool:
        """Returns True if the sender of the message or callback query is a bot administrator"""
        return obj.from_user.id in bot_config.admin_ids
