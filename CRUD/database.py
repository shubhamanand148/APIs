from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database-name>'
DATABASE_URL = 'postgresql://postgres:admin@localhost/postgres-db'

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()