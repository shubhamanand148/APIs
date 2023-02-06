# user_cred in this file is used for user authentication.

import models, schemas, oauth2
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(prefix="/posts", tags=['posts'])

#This gets all the posts in the database. It does not require user authentication.
@router.get("")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

#This Creates Post. It requires user authentication.
#The default status code is 200, but it is recommended to use 201 while creating a data.
@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)

# user_cred variable returns us the id and email of the user logged in.
async def create_post(post: schemas.Post, db: Session = Depends(get_db),
                      current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

# post is Post class and models.Post is from models class.
    print(current_user.email, "\t", current_user.id)
    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()        #Saves the changes to the Database.
    db.refresh(new_post)
    return new_post

# This gets the last added post from the database. 
@router.get("/latest", response_model=schemas.PostResponse)
async def get_latest_post(db: Session = Depends(get_db)):

    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return post

@router.get("/{id}", response_model=schemas.PostResponse)
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),
                      current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    #Chech if the index is there in the ID.
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to delete post with ID: {id} does not exist.")

    # If the logged in user is not the owner of the post. Throw error message.
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail = f"Not authorized to delete the post.")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Update Post
@router.put("/{id}")
async def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db),
                      current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    post_to_be_updated = db.query(models.Post).filter(models.Post.id == id)

    #Chech if the index is there in the ID.
    if post_to_be_updated.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to Update post with ID: {id} does not exist.")

    # If the logged in user is not the owner of the post. Throw error message.
    if post_to_be_updated.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorized to update the post.")

    post_to_be_updated.update({**post.dict()}, synchronize_session=False)
    db.commit()

    return post