from fastapi import APIRouter, Depends, HTTPException, status
from database import get_async_db
from jose import jwt 
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from argon2 import PasswordHasher
from schema.users import RegisterModel, LoginModel
from models.users import Users
from sqlalchemy.future import select
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()

router = APIRouter(prefix="/auth", tags=['Authentication'])

ph = PasswordHasher()

def create_access_token(username: str, user_id: str, role: str):
    payload = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("EXPIRES_DELTA")))
    payload.update({'exp': expires})
    return jwt.encode(payload, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))




@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterModel, db: AsyncSession = Depends(get_async_db)):
        user = (await db.execute(select(Users).filter(Users.email == request.email))).scalars().first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = "Email already exists."
            )
    
        password_hashed = ph.hash(request.password)

        new_user = Users(
            username = request.username,
            email = request.email,
            first_name = request.first_name,
            last_name = request.last_name,
            hashed_password = password_hashed
        )
        try:
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
        except Exception:
            await db.rollback()
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )
         
        return {
        "message": "Registered Successfully",
        "user_id": new_user.id
    }
   


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: LoginModel, db: AsyncSession = Depends(get_async_db)):
        user = (await db.execute(select(Users).filter(Users.email == request.email))).scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
        
        try:
            ph.verify(user.hashed_password, request.password)
        except (VerifyMismatchError, InvalidHashError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        token = create_access_token(username=user.username, user_id=user.id, role=user.role) 

        return {"message": f"Welcome back, {user.email}", "token":token}

#logout function