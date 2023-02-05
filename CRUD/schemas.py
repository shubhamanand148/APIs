from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    published: Optional[bool] = False

#This is the model for the request which user sends to the server.
class Post(PostBase):
    content: str
    rating: Optional[int] = None


#This is the model for the response which user gets back from the server.
#In this project it is used only in "post/id"
class ResponsePost(PostBase):
    created_at: datetime

    class Config:
        orm_mode=True