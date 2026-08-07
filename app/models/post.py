from app.core.database import Base
from sqlalchemy.orm import Mapped,mapped_column, relationship

from sqlalchemy import String,ForeignKey,Text,DateTime,func

from datetime import datetime
from app.models.user import User

class Post(Base):
    __tablename__="posts"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    author_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
    author:Mapped["User"]=relationship()
    
    title:Mapped[str]=mapped_column(String(200))
    content:Mapped[str]=mapped_column(Text)
    slug:Mapped[str]=mapped_column(String(250),unique=True,index=True)
    status:Mapped[str]=mapped_column(String(20),default="draft")
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())