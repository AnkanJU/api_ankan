from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="Set up Async DB connection")
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    completed: bool | None = None

class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True