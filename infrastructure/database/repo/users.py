from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def create_user(self, *args, **kwargs):
        ...
