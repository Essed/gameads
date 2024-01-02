from api.models import UserCreate, UserUI
from db.dals import UserDAL
from hasher import Hasher
from typing import Union
from db.dals import PlatformRole
from datetime import datetime


async def _create_new_user(body: UserCreate, session) -> UserUI:    
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.username,
            email=body.email,
            role=PlatformRole.ROLE_USER,
            registred_at=datetime.utcnow(),
            hashed_password=Hasher.get_password_hash(body.password)
        )
        return UserUI(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            role=user.role,
            registred_at=user.registred_at,
            balance=user.balance
        )


async def _delete_new_user(user_id, session) -> Union[int, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id,
        )
        return deleted_user_id



async def _get_user_by_id(user_id, session) -> Union[UserUI, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return UserUI(
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                role=user.role,
                balance=user.balance,
            )



async def _update_user(updated_user_params: dict, user_id: int, session) -> Union[int, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id,
            **updated_user_params
        )
        return updated_user_id



async def _get_user_by_email(email: str, session) -> Union[UserUI, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(
            email=email
        )
