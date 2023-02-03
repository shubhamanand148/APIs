#This project demonstrate the use of APIs (fastapi) to perform CRUD Operations on a postgres Database.
#To use the APIs run in cmd: uvicorn fastapi_CRUD:app --reload

from fastapi import FastAPI, Response, status, HTTPException, Depends
import models, schemas, utils
from database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

#Creates Post
#The default status code is 200, but it is recommended to use 201 while creating a data.
@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(post: schemas.Post, db: Session = Depends(get_db)):

# post is Post class and models.Post is from models class.
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()        #Saves the changes to the Database.
    db.refresh(new_post)
    print(post.content)
    return new_post

@app.get("/posts/latest")
async def get_latest_post(db: Session = Depends(get_db)):

    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return post

@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with ID: {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to find post with ID: {id} does not exist.")
    return post

# HTTP Status 204 (No Content) indicates that the server has successfully fulfilled the request
# and that there is no content to send in the response payload body.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    #Chech if the index is there in the ID.
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to delete post with ID: {id} does not exist.")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Update Post
@app.put("/posts/{id}")
async def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):

    update_post = db.query(models.Post).filter(models.Post.id == id)

    #Chech if the index is there in the ID.
    if update_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to Update post with ID: {id} does not exist.")

    update_post.update({**post.dict()}, synchronize_session=False)
    db.commit()

    return post

#########################################################################################################

# User Registration Code below.

@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()        #Saves the changes to the Database.
    db.refresh(new_user)
    return (new_user)



@app.get("/users/{id}", response_model=schemas.UserResponse)
async def user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with ID: {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to find user with ID: {id} does not exist.")
    return user