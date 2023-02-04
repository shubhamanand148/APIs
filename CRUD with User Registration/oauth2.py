from jose import JWTError, jwt
from datetime import datetime, timedelta

# The JWT Login Token consists of 4 things (Constant values) which we will need to provide
# and the payload or data provided by the user.
# 1. SECRET_KEY: Its a key which resides on the API Server.
# 2. Hashing algorith
# 3. Access Token Expiry Minutes: The time in minutes after which the user will be automatically logged out.
#    Expiry token can be left empty, which would keep the user logged in indefinetely.
#    But it is not good practice.

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    data_to_encode = data.copy()

    expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({'exp': expire_time})

    encoded_jwt_token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt_token
