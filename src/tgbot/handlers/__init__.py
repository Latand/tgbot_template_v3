"""
The module contains event handlers in the bot.

Note:
    Error handlers cannot be passed with this tuple and must be registered separately:
        application.add_handlers(handlers=HANDLERS)
        application.add_error_handler(callback=error_handler)

Modules:
    callbacks.py    - handlers for user button presses
    commands.py     - handlers for user commands
    messages.py     - handlers for user messages
    errors.py       - handlers for errors

Constants:
    ROUTERS - a tuple of routers to import and include in bot.py
"""

from aiogram import Router

from tgbot.handlers.commands import cmd_router
from tgbot.handlers.messages import msg_router


# the order of the elements is important
ROUTERS: tuple[Router, ...] = (
    cmd_router,
    msg_router,
)
