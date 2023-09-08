import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from tgbot.config import load_config, Config
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.misc.logging import LoggingPackagePathFilter
from tgbot.services import broadcaster


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    middleware_types = [
        ConfigMiddleware(config),
        # DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging(config: Config):
    """
    Set up logging configuration for the application.

    The function sets up logging for production and development environments.
    If the environment is development, the function will add a filter to the logger that will create a full path
    to the file where the log record was created. This is done to make it easier to find the place where the log
    record was created.
    Otherwise, the function will set up a colorized logging configuration using the betterlogging library.

    Args:
        config (Config): The configuration object.

    Returns:
        None

    Example usage:
        setup_logging(config)
    """
    logger = logging.getLogger("__name__")
    log_level = logging.INFO

    if config.environment == "dev":
        package_filter = LoggingPackagePathFilter()
        logger.addFilter(package_filter)
        log_format = "%(pathname)s:%(lineno)s: %(message)s"
    else:
        bl.basic_colorized_config(level=log_level)
        log_format = "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
        logging.getLogger("aiogram").setLevel(logging.WARNING)  # reduce aiogram logging

    logging.basicConfig(
            level=log_level,
            format=log_format,
    )
    logger.info("Starting bot in %s environment", config.environment)


def get_storage(config):
    """
    Return storage based on the provided configuration.

    Args:
        config (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


async def main():
    config = load_config(".env")
    setup_logging(config)
    storage = get_storage(config)

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    dp.include_routers(*routers_list)

    register_global_middlewares(dp, config)

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот був вимкнений!")
