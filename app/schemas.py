from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class SourceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    type: str = Field(pattern="^(rss|html)$")
    url: str
    enabled: bool = True

class SourceOut(BaseModel):
    id: int
    name: str
    type: str
    url: str
    enabled: bool
    created_at: datetime
    class Config:
        from_attributes = True

class ItemOut(BaseModel):
    id: int
    source_id: int
    title: str
    url: str
    published_at: Optional[datetime]
    snippet: Optional[str]
    fetched_at: Optional[datetime]
    class Config:
        from_attributes = True
