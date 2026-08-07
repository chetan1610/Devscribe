from fastapi import APIRouter
from app.core.database import get_db
from app.core.deps import get_current_user
from app.services import comment_service
from fastapi import HTTPException,status
from app.models.comment import Comment
from app.models.user import User
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.comment import CommentCreate,CommentOut

router=APIRouter(tags=["comments"])

@router.post("/posts/{post_id}/comments",response_model=CommentOut,status_code=status.HTTP_201_CREATED)
async def add_comment(post_id:int,data:CommentCreate,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    return await comment_service.add_comment(db,post_id,current_user.id,data.content)

@router.get("/posts/{post_id}/comments",response_model=list[CommentOut])
async def list_comments(post_id:int,db:AsyncSession=Depends(get_db)):
    return await comment_service.list_comments(db,post_id)


@router.delete("/comments/{comment_id}",status_code=status.HTTP_200_OK)
async def delete_comment(comment_id:int,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    await comment_service.delete_comment(db,comment_id,current_user.id)
    return {"detail":"comment deleted"}
