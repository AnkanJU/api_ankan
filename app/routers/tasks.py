from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import TaskModel
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.security import verify_api_key

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])

# Protected: Requires X-API-Key
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
async def create_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db)):
    new_task = TaskModel(title=task_in.title, completed=task_in.completed)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

# Public: Read access
@router.get("/", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
async def get_all_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel))
    return result.scalars().all()

# Public: Read one access
@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return task

# Protected: Requires X-API-Key
@router.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_api_key)])
async def update_task(task_id: int, task_in: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    
    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task

# Protected: Requires X-API-Key
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_api_key)])
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")

    await db.delete(task)
    await db.commit()
    return