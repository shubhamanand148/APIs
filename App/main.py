#This project demonstrate the use of APIs (fastapi) to perform CRUD Operations on a postgres Database.
#To use the APIs run in cmd: uvicorn fastapi_CRUD:app --reload

from fastapi import FastAPI, Response, status, HTTPException, Depends
import models, schemas
from database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

#Creates Post
#The default status code is 200, but it is recommended to use 201 while creating a data.
@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(post: schemas.Post, db: Session = Depends(get_db)):

# post is Post class and models.Post is from models class.
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()        #Saves the changes to the Database.
    db.refresh(new_post)
    
    return {"Data": new_post}

@app.get("/posts/latest")
async def get_latest_post(db: Session = Depends(get_db)):

    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return {"Latest Post: ": post}

@app.get("/posts/{id}")
async def post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with ID: {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to find post with ID: {id} does not exist.")
    return {"Post": post}

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

    update_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post}