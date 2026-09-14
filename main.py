from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="DevFlow API Engine",
    version="1.0.0"
)

# Mock in-memory database
tasks_db = [
    {"id": 1, "title": "Setup development environment", "completed": True},
    {"id": 2, "title": "Learn REST architectural principles", "completed": False}
]

class TaskCreate(BaseModel):
    title: str
    completed: bool = False

# 1. READ ALL (GET /api/v1/tasks)
@app.get("/api/v1/tasks", status_code=status.HTTP_200_OK)
def get_all_tasks():
    return {"data": tasks_db, "total": len(tasks_db)}

# 2. READ ONE (GET /api/v1/tasks/{task_id})
@app.get("/api/v1/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return {"data": task}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

# 3. CREATE (POST /api/v1/tasks)
@app.post("/api/v1/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    new_id = len(tasks_db) + 1
    new_task = {"id": new_id, "title": task.title, "completed": task.completed}
    tasks_db.append(new_task)
    return {"message": "Task created successfully", "data": new_task}