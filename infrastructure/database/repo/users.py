import logging
from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        full_name: str,
        language: str,
        username: Optional[str] = None,
    ):
        """
        Creates or updates a new user in the database and returns the user object.
        Only fields provided as parameters will be updated in the case of a conflict.
        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param language: The user's language.
        :param username: The user's username. It's an optional parameter.
        :return: User object, None if there was an error while making a transaction.
        """
        try:

            insert_stmt = (
                insert(User)
                .values(
                    user_id=user_id,
                    username=username,
                    full_name=full_name,
                    language=language,
                )
                .on_conflict_do_update(
                    index_elements=[User.user_id],
                    set_=dict(
                        username=username,
                        full_name=full_name,
                    ),
                )
                .returning(User)
            )
            result = await self.session.execute(insert_stmt)

            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            # Log the error or re-raise with additional information if necessary
            logging.error(f"Failed to insert or update user: {e}")
            raise Exception("Failed to insert or update user in the database.") from e
        except Exception as e:
            await self.session.rollback()
            # Handle other exceptions, possibly re-raise
            logging.error(f"An unexpected error occurred: {e}")
            raise Exception(
                "An unexpected error occurred during database operations."
            ) from e
