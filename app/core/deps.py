from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.token import ALGORITHM
from app.models.user import User
from app.repositories import user_repository

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token:str=Depends(oauth2_scheme),db:AsyncSession=Depends(get_db))->User:
    credantials_error=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credantials")
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=ALGORITHM)
    except jwt.InvalidTokenError:
        raise credantials_error
    user_id=int(payload.get("sub"))
    user = await user_repository.get_by_id(db, user_id)
    if user is None:
        raise credantials_error
    return user