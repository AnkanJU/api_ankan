from pydantic import BaseModel, Field, field_validator

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, example="Implement validation middleware")
    completed: bool = False

    @field_validator("title")
    @classmethod
    def validate_title_content(cls, v: str) -> str:
        clean_title = v.strip()
        if not clean_title:
            raise ValueError("Task title cannot be blank or whitespace only")
        return clean_title

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_optional_title(cls, v: str | None) -> str | None:
        if v is not None:
            clean_title = v.strip()
            if not clean_title:
                raise ValueError("Updated title cannot be blank")
            return clean_title
        return v

class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True