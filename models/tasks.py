from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime
from database import Base
from datetime import datetime, timezone


class Tasks(Base):
    __tablename__  = 'tasks'

    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default= False)
    created_date = Column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey("task_users.id"))