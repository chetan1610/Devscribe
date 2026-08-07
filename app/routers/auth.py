from fastapi import APIRouter,Depends,status,Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate,UserOut,UserLogin,TokenOut
from app.services import auth_service
from app.core.rate_limit import check_rate_limit

router=APIRouter(prefix="/auth",tags=["auth"])

@router.post("/signup",response_model=UserOut,status_code=status.HTTP_201_CREATED)
async def signup(data:UserCreate,db: AsyncSession=Depends(get_db)):
    
    return await auth_service.signup(db,data)

@router.post("/login",response_model=TokenOut,status_code=status.HTTP_200_OK)
async def login(data:UserLogin,request:Request,db:AsyncSession=Depends(get_db)):
    ip=request.client.host
    await check_rate_limit(f"ratelimit:login:{ip}",limit=5,window=60)
    return await auth_service.login(db,data.email,data.password)

