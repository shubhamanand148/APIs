from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False
    rating: Optional[int] = None

class Post(PostBase):
    pass