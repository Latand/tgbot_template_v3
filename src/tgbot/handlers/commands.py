"""
The module contains handlers that respond to commands from bot users

Contains:
    start_cmd_from_admin    - response to the '/start' command from the bot administrators
    start_cmd_from_user     - response to the '/start' command from the bot users
    help_cmd                - response to the '/help' command

Note:
    Routers are imported into the __init__.py package handlers,
    where a tuple of ROUTERS is assembled for further registration in the dispatcher
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from tgbot.config import BOT_LOGO
from tgbot.misc.filters import IsAdmin


# Create router
cmd_router = Router(name="cmd_router")


async def start_cmd_from_admin(message: Message) -> None:
    """This handler receive messages with `/start` command from bot admins"""
    await message.answer(text="👋 Hello, admin!")


async def start_cmd_from_user(message: Message) -> None:
    """This handler receive messages with `/start` command from bot users"""
    username: str = message.from_user.first_name
    await message.answer(text=f"👋 Hello, {username if username else 'user'}!")


async def help_cmd(message: Message) -> None:
    """This handler receive messages with `/help` command"""
    caption: str = (
        "This is a template for a telegram bot written in Python using the "
        "<b><a href='https://github.com/aiogram/aiogram'>aiogram</a></b> framework"
        "\n\n"
        "The source code of the template is"
        " available in the repository on <b><a href='https://github.com/rin-gil/aiogram_v3_template'>GitHub</a></b>"
    )
    await message.answer_photo(photo=FSInputFile(path=BOT_LOGO), caption=caption)


# Register routers
cmd_router.message.register(start_cmd_from_admin, *(Command(commands=["start"]), IsAdmin()))
cmd_router.message.register(start_cmd_from_user, Command(commands=["start"]))
cmd_router.message.register(help_cmd, Command(commands=["help"]))
