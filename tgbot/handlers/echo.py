from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

echo_router = Router()


@echo_router.message(F.text, StateFilter(None))
async def bot_echo(message: types.Message):
    text = ["Ехо без стану.", "Повідомлення:", message.text]

    await message.answer("\n".join(text))


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f"Ехо у стані {hcode(state_name)}",
        "Зміст повідомлення:",
        hcode(message.text),
    ]
    await message.answer("\n".join(text))
