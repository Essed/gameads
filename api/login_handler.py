from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from db.session import get_db
from fastapi.security import OAuth2PasswordRequestForm
from api.models import Token
from fastapi import HTTPException, status
from datetime import timedelta
import settings
from security import create_access_token
from api.actions.auth import authentificate_user


login_router = APIRouter()


@login_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authentificate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expire_delta = access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


