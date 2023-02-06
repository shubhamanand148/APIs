from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import schemas, database, models

# The JWT Login Token consists of 4 things (Constant values) which we will need to provide.
# 1. SECRET_KEY: Its a key which resides on the API Server.
# 2. Hashing algorith
# 3. Access Token Expiry Minutes: The time in minutes after which the user will be automatically logged out.
#    Expiry token can be left empty, which would keep the user logged in indefinetely.
#    But it is not good practice.
# 4. The payload or data provided by the user.

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    data_to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({'exp': expire_time})

    encoded_jwt_token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt_token


def verify_access_token(token: str, credential_exception):

    try:
        
        # Get the payload from the JWT Token.
        paylaod = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        # Retrieve id and email from the payload of JWT Token.
        id: str = paylaod.get("user_id")
        email: str = paylaod.get("user_email")

        if id is None:
            raise credential_exception

        token_data = schemas.TokenData(id = id, email = email)
    
    except JWTError:
        raise credential_exception

    return token_data


# This function fetches the user from the database once the verify_access_token function gives the id.
# So that we can attach the user to path operation and perform logics.
# Alternatively, the path operations can fetch the users.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials.",
                                         headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user