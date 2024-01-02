from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
from db.dals import UserDAL
from hasher import Hasher
from db.session import get_db
from typing import Union
from db.models import User
import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

async def _get_user_by_email_for_auth(email: str, session):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(
            email=email
        )


async def authentificate_user(email: str, password: str, session) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email, session)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user



async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALHORITHM]
        )
        email: str = payload.get("sub")
        print("email extracted is ", email)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email=email, session=db)
    if user is None:
        raise credentials_exception
    return user