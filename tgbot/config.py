import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    @classmethod
    def set_env_file(cls, env_file_path: str):
        """
        Dynamically sets the path to the .env file for the model configuration.
        This method should ideally be used before any instances are created to avoid inconsistent configurations across instances.

        Args:
            env_file_path: The path to the .env file.
        """
        cls.model_config["env_file"] = env_file_path


class TgBot(BaseSettings, env_prefix="TGBOT_"):
    """
    Creates the TgBot object from environment variables.
    """

    token: SecretStr
    admin_ids: list[int]
    use_redis: bool = False


class DbConfig(BaseSettings, env_prefix="DB_"):
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes
    ----------
    host : str
        The host where the database server is located.
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    database : str
        The name of the database.
    port : int
        The port where the database server is listening.
    """

    host: str
    password: SecretStr
    user: str
    database: str
    port: int = 5432

    # For SQLAlchemy
    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """
        # TODO: If you're using SQLAlchemy, move the import to the top of the file!
        from sqlalchemy.engine.url import URL

        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password.get_secret_value(),
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)


class RedisConfig(BaseSettings, env_prefix="REDIS_"):
    """
    Redis configuration class.

    Attributes
    ----------
    password : Optional(SecretStr)
        The password used to authenticate with Redis.
    port : Optional(int)
        The port where Redis server is listening.
    host : Optional(str)
        The host where Redis server is located.
    """

    password: Optional[SecretStr]
    port: Optional[int] = 6379
    host: Optional[str] = "localhost"

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.password:
            return (
                f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/0"
            )
        else:
            return f"redis://{self.host}:{self.port}/0"


class Miscellaneous(BaseSettings, env_prefix="MISC_"):
    """
    Miscellaneous configuration class.

    This class holds settings for various other parameters.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes
    ----------
    other_params : str, optional
        A string used to hold other various parameters as required (default is None).
    """

    other_params: str


class Config(BaseModel):
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    misc : Miscellaneous
        Holds the values for miscellaneous settings.
    db : Optional[DbConfig]
        Holds the settings specific to the database (default is None).
    redis : Optional[RedisConfig]
        Holds the settings specific to Redis (default is None).
    """

    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig
    misc: Optional[Miscellaneous]


def load_config(env_file: Optional[str] = None):
    """
    Load configuration from a specified or default .env file.

    This function initializes configuration objects for the application
    based on the settings defined in a .env file. If no specific file is
    provided via `env_file`, it defaults to 'env'.

    Parameters:
        env_file (str, optional): Path to the .env file to use. Defaults to 'env'.

    Returns:
        Config: Config object containing settings loaded from the .env file.

    Raises:
        ValidationError: If any environment variables fail validation checks.
    """
    # Set the default .env file if none specified
    if env_file:
        BaseSettings.set_env_file(
            env_file
        )  # Set the environment file for all settings classes
    else:
        env_file = ".env"  # Default .env path

    # Convert to absolute path
    env_file_path = Path(env_file).resolve()

    # Check if the .env file exists
    if not env_file_path.exists():
        raise FileNotFoundError(
            f"The specified .env file does not exist: {env_file_path}"
        )

    logging.info(f"Loading configuration from {env_file_path}")

    try:

        # Create instances with the specified or default .env file
        config = Config(
            tg_bot=TgBot(_env_file=env_file),
            db=DbConfig(_env_file=env_file),
            redis=RedisConfig(_env_file=env_file),
            misc=Miscellaneous(_env_file=env_file),
        )
        logging.info(f"Configuration loaded from {env_file_path}")
        return config
    except Exception as e:
        logging.error(f"Error loading configuration from {env_file_path}: {e}")
        raise e
