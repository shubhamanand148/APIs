#This project demonstrate the use of APIs (fastapi) to perform CRUD Operations on a postgres Database.
#To use the APIs run in cmd: uvicorn fastapi_CRUD:app --reload

from fastapi import FastAPI
import models
from database import engine
from routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)