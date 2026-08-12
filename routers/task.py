from fastapi import APIRouter, Depends, HTTPException, status, Path
from authenticate import get_current_user
from database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.tasks import Tasks
from schema.tasks import TaskModel

router = APIRouter(prefix="/task", tags=["Tasks"])

@router.get("/", status_code=status.HTTP_200_OK)
async def get_task(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    try:
        result = await db.execute(select(Tasks).filter(Tasks.user_id == user["id"]))
        return result.scalars().all()
    
    except Exception:
         raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get all tasks"
            )
    
@router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int = Path(gt=0), user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    try:
        result = await db.execute(select(Tasks).filter(Tasks.user_id == user["id"], Tasks.id == task_id))
        task = result.scalars().first()

        if task is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

        return task
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get task"
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskModel, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    new_task = Tasks(
            title=request.title,
            description=request.description,
            priority=request.priority,
            complete=request.complete,
            user_id=user["id"],
            due_date=request.due_date
        )
    try:
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)

    except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Task creation failed"
            )

    return {"id": new_task.id, "message": "Task added successfully"}

@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(request: TaskModel, task_id : int = Path(gt=0), user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user["id"]))
    task = result.scalars().first()

    if task is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    
    task.title = request.title
    task.description = request.description
    task.complete = request.complete
    task.priority = request.priority
    task.due_date = request.due_date

    try:
        await db.commit()

    except Exception:
        await db.rollback()
        raise HTTPException (status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Task update failed")
        
    return {"message": "Task updated successfully"}

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id : int = Path(gt=0), user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user["id"]))
    task = result.scalars().first()

    if task is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

    try:
        await db.delete(task)
        await db.commit()

    except Exception:
        await db.rollback()
        raise HTTPException (status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Task delete failed")
        
    return {"message": "Task deleted successfully"}