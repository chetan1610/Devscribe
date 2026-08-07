from app.core.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from app.models.post import Post
from app.models.user import User
from sqlalchemy import Text
from sqlalchemy import DateTime,func
from datetime import datetime


class Comment(Base):
    __tablename__="comments"
    id:Mapped[int]=mapped_column(primary_key=True)
    post_id:Mapped[int]=mapped_column(ForeignKey("posts.id"),index=True)
    author_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
    content:Mapped[str]=mapped_column(Text)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())