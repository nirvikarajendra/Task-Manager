from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"))

Base = declarative_base()

AsyncSessionLocal = async_sessionmaker(autoflush=False, autocommit=False, bind=engine)

async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db

