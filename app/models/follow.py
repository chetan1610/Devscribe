from sqlalchemy import ForeignKey,DateTime,UniqueConstraint,func
from  app.core.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer
from datetime import datetime
from app.models.user import User

class Follow(Base):
    __tablename__="follows"
    __table_args__=(UniqueConstraint("follower_id","following_id",name="uq_follower_following"),)
    
    id:Mapped[int]=mapped_column(primary_key=True)
    follower_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
    following_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())