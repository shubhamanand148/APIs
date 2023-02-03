from passlib.context import CryptContext

#It tells which hashing algorithm (bcrypt) to use.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)