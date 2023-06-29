from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:
    def __init__(self, session):
        self.session: AsyncSession = session

