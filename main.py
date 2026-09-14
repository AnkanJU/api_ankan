from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="DevFlow API Engine",
    version="1.0.0"
)

# Mock in-memory database
tasks_db = [
    {"id": 1, "title": "Setup development environment", "completed": True},
    {"id": 2, "title": "Learn REST architectural principles", "completed": False}
]

# Pydantic Schemas
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, example="Complete Phase 4 CRUD operations")
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

# --- REST ENDPOINTS ---

# 1. READ ALL (GET)
@app.get("/api/v1/tasks", status_code=status.HTTP_200_OK)
def get_all_tasks():
    return {"data": tasks_db, "total": len(tasks_db)}

# 2. READ ONE (GET)
@app.get("/api/v1/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return {"data": task}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")

# 3. CREATE (POST)
@app.post("/api/v1/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    new_id = tasks_db[-1]["id"] + 1 if tasks_db else 1
    new_task = {"id": new_id, "title": task.title, "completed": task.completed}
    tasks_db.append(new_task)
    return {"message": "Task created successfully", "data": new_task}

# 4. FULL UPDATE (PUT)
@app.put("/api/v1/tasks/{task_id}", status_code=status.HTTP_200_OK)
def replace_task(task_id: int, task_in: TaskCreate):
    for idx, task in enumerate(tasks_db):
        if task["id"] == task_id:
            updated_task = {"id": task_id, "title": task_in.title, "completed": task_in.completed}
            tasks_db[idx] = updated_task
            return {"message": "Task replaced successfully", "data": updated_task}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")

# 5. PARTIAL UPDATE (PATCH)
@app.patch("/api/v1/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task_partial(task_id: int, task_in: TaskUpdate):
    for task in tasks_db:
        if task["id"] == task_id:
            update_data = task_in.model_dump(exclude_unset=True)
            task.update(update_data)
            return {"message": "Task updated successfully", "data": task}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")

# 6. DELETE
@app.delete("/api/v1/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for idx, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(idx)
            return  # 204 status responses return no body
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")