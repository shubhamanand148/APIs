import models, utils, schemas
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter()

# User Registration Code below.

@router.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()        #Saves the changes to the Database.
    db.refresh(new_user)
    return (new_user)



@router.get("/users/{id}", response_model=schemas.UserResponse)
async def user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with ID: {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to find user with ID: {id} does not exist.")
    return user