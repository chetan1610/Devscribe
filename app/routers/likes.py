from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services import like_service
from app.repositories import like_repository

router = APIRouter(tags=["likes"])


@router.post("/posts/{post_id}/like", status_code=status.HTTP_201_CREATED)
async def like(post_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await like_service.like_post(db, current_user.id, post_id)
    return {"detail": "Post liked"}


@router.delete("/posts/{post_id}/like", status_code=status.HTTP_200_OK)
async def unlike(post_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await like_service.unlike_post(db, current_user.id, post_id)
    return {"detail": "Post unliked"}


@router.get("/posts/{post_id}/likes")
async def like_count(post_id: int, db: AsyncSession = Depends(get_db)):
    count = await like_repository.count_likes(db, post_id)
    return {"post_id": post_id, "likes": count}