"""The module contains a simple broadcaster that allows you to send messages to bot users"""

from asyncio import sleep
from typing import Iterable

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError, TelegramRetryAfter

from tgbot.config import logger


async def _send_message(bot: Bot, user_id: int | str, msg: str, disable_notification: bool) -> bool:
    """Sends a message to the selected user"""
    try:
        await bot.send_message(chat_id=user_id, text=msg, disable_notification=disable_notification)
    except TelegramForbiddenError:
        logger.error("Target [ID:%s]: The bot was blocked by the user", user_id)
    except TelegramRetryAfter as exc:
        logger.warning("Target [ID:%s]: Flood limit is exceeded, sleep %s seconds", user_id, exc.retry_after)
        await sleep(delay=exc.retry_after)
        # Recursive call
        return await _send_message(bot=bot, user_id=user_id, msg=msg, disable_notification=disable_notification)
    except TelegramAPIError:
        logger.error("Target [ID:%s]: failed", user_id)
    else:
        logger.info("Target [ID:%s]: success", user_id)
        return True
    return False


async def broadcast(bot: Bot, users: Iterable, msg: str, disable_notification: bool = False) -> None:
    """
    Simple broadcaster

    :param bot: Telegram bot (object of class Bot)
    :param users: Iterated sequence (list, tuple, etc.), containing user id
    :param msg: The message that will be sent to the bot user
    :param disable_notification: Show notification to user
    :return: None
    """
    if len(msg) == 0:
        logger.error("The message cannot be empty")
        return None

    count: int = 0
    try:
        for user_id in users:
            if await _send_message(bot=bot, user_id=user_id, msg=msg, disable_notification=disable_notification):
                count += 1
            # 20 messages per second (Limit: 30 messages per second)
            await sleep(delay=0.05)
    finally:
        logger.info("%s messages successful sent", count)
