from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from database import get_db
import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'], prefix='/login')

@router.post("")

# OAuth2PasswordRequestForm allows us to enter the values as a form. Itis a dictionary consisting of 2 keys:
# 1. Username: It can have any value id/email/username.
# 2. Password: It has to be the password of the user.
async def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Search for the user based on email id of the user.
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

# If the Email ID provided while logging in does not exists. Return 404 with "Invalid Creadentials"
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

# If the Password provided while logging in does not match the hashed password stored in database.
# Return 404 with "Invalid Creadentials"
    if not utils.verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id, "user_email": user.email,
                                                    "user_pwd": user.password})

    return {"token": access_token, "token_type": "bearer token"}
