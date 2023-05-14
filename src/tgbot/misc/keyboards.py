"""
In this module you can store the keyboards used in the bot

Example:
    Import the keyboard and keys:
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    Creating a keyboard with three buttons:
        test_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="First button", callback_data="data_from_first_button")],
                [InlineKeyboardButton(text="Second button", callback_data="data_from_second_button")],
                [InlineKeyboardButton(text="Third button", callback_data="data_from_third_button")],
            ]
        )

    Attach the keyboard to the message:
        await message.answer(text="Some message",reply_markup=test_kb)
"""
