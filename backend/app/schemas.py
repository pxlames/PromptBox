from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PromptBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str
    tags: Optional[str] = ""


class PromptCreate(PromptBase):
    pass


class PromptUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = None
    tags: Optional[str] = None


class PromptOut(PromptBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


