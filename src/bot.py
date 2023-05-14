"""Launches the bot"""

from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.config import bot_config, logger

from tgbot.handlers import ROUTERS
from tgbot.misc.bot_commands import set_default_commands
from tgbot.services.broadcaster import broadcast


async def on_startup(bot: Bot) -> None:
    """The functions that runs when the bot starts, before the dp.start_polling()"""
    await set_default_commands(bot=bot)
    await broadcast(bot=bot, users=bot_config.admin_ids, msg="Bot was started", disable_notification=True)


async def on_shutdown(bot: Bot) -> None:
    """The functions that runs when the bot is stopped"""
    await broadcast(bot=bot, users=bot_config.admin_ids, msg="Bot was stopped", disable_notification=True)


async def start_bot() -> None:
    """Launches the bot"""
    bot: Bot = Bot(token=bot_config.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(storage=MemoryStorage())
    dp.include_routers(*ROUTERS)
    dp.startup.register(callback=on_startup)
    dp.shutdown.register(callback=on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("Starting bot")
        run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as exc:
        logger.critical("Unhandled error: %s", repr(exc))
    finally:
        logger.info("Bot stopped!")
