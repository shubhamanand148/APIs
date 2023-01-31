# APIs

1. **fastapi_CRUD.py:** It is a simple project which does CRUD operations with postgres using fastapi and sql.
                        It uses Pydantic data model i.e. We check the request/response data we get for any constraints.
                        Like if we want to keep a certain value as integer, or if some value is required. It throws exception if the constraints are not met.

2. **Apps:** It is a project which does CRUD application using fastapi and sqlalchemy (write sql commands as python).
             It uses both sqlalchemy (in models.py) and pydantic model(in schemas.py).
             The sqlalchemy model is used to create table in postgres and is similar to pydentic model.
             In this project, we are putting the constraints also on the request which we receive.
