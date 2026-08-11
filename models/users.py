from sqlalchemy import Column, Integer, Boolean, String, Enum
from database import Base


class Users(Base):
    __tablename__  = 'task_users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role =  Column(Enum("admin", "user", name="role_enum"), default="user")