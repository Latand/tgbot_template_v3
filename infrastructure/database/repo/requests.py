from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repo.users import UserRepo
from infrastructure.database.setup import create_engine


@dataclass
class RequestsRepo:
    session: AsyncSession
    users: UserRepo = None


def example_usage():
    from infrastructure.database.setup import create_session_pool
    from tgbot.config import load_config

    config = load_config()
    engine = create_engine(config.db)
    session_pool = create_session_pool(engine)

    async with session_pool() as session:
        repo = RequestsRepo(session)
        await repo.users.create_user()
        ...
