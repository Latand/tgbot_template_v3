"""
The module presents a function that changes the default list of commands for the bot.
You can set different commands depending on the language of the user or show certain commands only to administrators.

Learn more: https://core.telegram.org/bots/api#setmycommands
"""

from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot) -> None:
    """Sets default commands for the bot"""
    commands: list[BotCommand] = [
        BotCommand(command="start", description="▶️ Starts the bot"),
        BotCommand(command="help", description="ℹ️ Bot info"),
    ]
    await bot.set_my_commands(commands=commands, scope=None, language_code=None)
