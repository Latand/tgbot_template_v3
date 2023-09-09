import asyncio
import logging
import pathlib

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
    If the environment is development, the function sets up logging to the console with the package path filter.
    Otherwise, the function sets up logging to the file.

    Args:
        config (Config): The configuration object.

    Returns:
        None

    Example usage:
        setup_logging(config)
    """
    logger = logging.getLogger(__name__)

    if config.environment == "dev":
        # note - didn't find a way to set the filter in BasicConfig, so I used loggerDict
        package_filter = LoggingPackagePathFilter()
        loggers_names = [name for name in logging.root.manager.loggerDict] + ["root"]
        for logger_name in loggers_names:
            logging.getLogger(logger_name).addFilter(package_filter)

        # setup logging configuration for dev environment with StreamHandler
        log_format = "%(pathname)s:%(lineno)s [%(name)s]: %(message)s"
        formatter = logging.Formatter(log_format)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handlers = [handler]
    else:
        # define logs directory and path to logs file and create logs directory if it does not exist
        logs_directory = pathlib.Path("logs")
        logs_path = logs_directory / "logs.txt"
        pathlib.Path(logs_directory).mkdir(parents=True, exist_ok=True)

        # setup logging configuration for prod environment with FileHandler
        handler = logging.FileHandler(logs_path, mode="a")
        log_format = "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        handlers = [handler]
        # reduce aiogram logging level
        logging.getLogger("aiogram").setLevel(logging.WARNING)

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=handlers,
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
