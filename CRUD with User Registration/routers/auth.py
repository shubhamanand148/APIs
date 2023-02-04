from fastapi import HTTPException, Depends, APIRouter, Response, status
from sqlalchemy.orm import Session
from database import get_db
import schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'], prefix='/login')

@router.post("")
async def login(user_credential: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.email).first()

# If the Email ID provided while logging in does not exists. Return 404 with "Invalid Creadentials"
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

# If the Password provided while logging in does not match the hashed password stored in database.
# Return 404 with "Invalid Creadentials"
    if not utils.verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id, "user.email": user.email,
                                                    "user.pwd": user.password})

    return {"token": access_token, "token_type": "bearer token"}
