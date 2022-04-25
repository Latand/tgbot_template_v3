from aiogram import Router
from aiogram.types import Message

user_router = Router()


@user_router.message(commands=["start"])
async def user_start(message: Message):
    await message.reply("Вітаю, звичайний користувач!")
