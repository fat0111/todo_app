from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass 

class TodoResponse(TodoBase):
    id: str
    completed: bool
    created_at: Optional[str] = None

    class Config:
        from_attributes = True