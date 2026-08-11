from fastapi import APIRouter, Depends, HTTPException, status
from database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from authenticate import get_current_user
from models.users import Users
from schema.users import PasswordModel
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from sqlalchemy.future import select

router = APIRouter(prefix="/user", tags=["Users"])

ph = PasswordHasher()

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Users).filter(Users.id == user["id"]))

    user_model = result.scalars().first()

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return user_model

@router.put("/password", status_code=status.HTTP_200_OK)
async def update_password(request: PasswordModel, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    result = await  db.execute(select(Users).filter(Users.id == user["id"]))
    user_model = result.scalars().first()
    
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    try:
        ph.verify(user_model.hashed_password, request.password)
    except (VerifyMismatchError, InvalidHashError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    user_model.hashed_password = ph.hash(request.new_password)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Password update failed")
    
    return {"message": "Password updated successfully"}

