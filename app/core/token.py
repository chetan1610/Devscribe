from datetime import datetime,timedelta,timezone

import jwt

from app.core.config import settings

ALGORITHM="HS256"

def create_access_token(user_id:int)->str:
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={"sub":str(user_id),"exp":expire,"type":"access"}
    return jwt.encode(payload,settings.SECRET_KEY,algorithm=ALGORITHM)


def create_refresh_token(user_id:int)->str:
    expire=datetime.now(timezone.utc)+timedelta(days=7)
    payload={"sub":str(user_id),"exp":expire,"type":"refresh"}
    return jwt.encode(payload,settings.SECRET_KEY,algorithm=ALGORITHM)

