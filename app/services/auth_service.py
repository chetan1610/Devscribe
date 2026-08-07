from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password,verify_password
from app.repositories import user_repository
from app.schemas.user import UserCreate
from app.models.user import User

from app.core.token import create_access_token,create_refresh_token


async def signup(db:AsyncSession,data:UserCreate)->User:
    if await user_repository.get_by_email(db,data.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already registered")
    if await user_repository.get_by_username(db,data.username) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="username already taken")
    
    hashed=hash_password(data.password)
    
    return await user_repository.create(db,username=data.username,email=data.email,hashed_password=hashed)
        
        
async def login(db:AsyncSession,email:str,password:str)->User:
    user=await user_repository.get_by_email(db,email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")
    if not verify_password(password,user.hashed_password):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")
    
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }
        
        