"""Setting up the configuration for the bot"""

import logging
import sys
from os import path
from pathlib import Path

from environs import Env, EnvError


# Change DEBUG to False when running on a production server
DEBUG: bool = True


# Path settings
_BASE_DIR: Path = Path(__file__).resolve().parent.parent
BOT_LOGO: str = path.normpath(path.join(_BASE_DIR, "tgbot/assets/img/bot_logo.jpg"))
ENV_FILE: str = path.normpath(path.join(_BASE_DIR, ".env"))
LOG_FILE: str = path.normpath(path.join(_BASE_DIR, "tgbot.log"))


# Disables full traceback of errors in the log file
if not DEBUG:
    sys.tracebacklimit = 0

# Logger config
logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=None if DEBUG else LOG_FILE,
    encoding="utf-8",
    format=f"[%(asctime)s] %(levelname)-8s {'%(filename)s:%(lineno)d - ' if DEBUG else ''}%(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


class BotConfig:
    """Reads variables from the .env file"""

    def __init__(self, path_to_env_file: str) -> None:
        """Initializing a class or terminating a program if no .env file is found"""
        if not path.exists(path=path_to_env_file):
            logger.critical("The .env file was not found in the path %s", path_to_env_file)
            sys.exit(1)
        self._env: Env = Env()
        self._env.read_env(path=path_to_env_file, recurse=False)

    @property
    def token(self) -> str:
        """Returns the bot token or terminates the program in case of an error"""
        try:
            return str(self._env.str("BOT_TOKEN"))
        except EnvError as exc:
            logger.critical("BOT_TOKEN not found: %s", repr(exc))
            sys.exit(repr(exc))

    @property
    def admin_ids(self) -> tuple[int, ...] | None:
        """Returns administrator IDs or None if ADMINS is not set in the .env file"""
        try:
            return tuple(map(int, self._env.list("ADMINS")))
        except (EnvError, ValueError) as exc:
            logger.warning("ADMINS ids not found: %s", repr(exc))
            return None


bot_config = BotConfig(path_to_env_file=ENV_FILE)
