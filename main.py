from fastapi import FastAPI
from database import Base, engine
from models import tasks, users
from routers import task, user, auth

app = FastAPI()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)
