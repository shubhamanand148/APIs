#This project demonstrate the use of APIs (fastapi) to perform CRUD Operations on a postgres Database.
#To use the APIs run in cmd: uvicorn fastapi_CRUD:app --reload

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2, time
from psycopg2.extras import RealDictCursor

app = FastAPI()

#This is a Pydantic model. i.e. title and content are required fields.
#published is an optional field, and if not provided its default value will be false.
#rating is an optional field, and if not provided it will be null.
class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

while True:
    try:
        database_connect = psycopg2.connect(host='localhost', database='Products Database',
        user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = database_connect.cursor()
        print("Database Connection Successful")
        break

    except Exception as error:
        print("Connection to posts Database Failed.\nError: ", error)
        time.sleep(5)


# Sample memory data.
# my_posts = [{"title": "Post 1 Title", "content": "Post 1 Content", "id": 1},
#            {"title": "Post 2 Title", "content": "Post 2 Content", "id": 2},
#            {"title": "Post 3 Title", "content": "Post 3 Content", "id": 3},
#            {"title": "Post 4 Title", "content": "Post 4 Content", "id": 4}]

# def find_post(id):
#    for post in my_posts:
#        if post["id"] == id:
#            return post

#def find_post_index(id):
#    for i, post in enumerate(my_posts):
#        if post['id'] == id:
#            return i


@app.get("/posts")
async def get_posts():
    cursor.execute("SELECT * FROM public.posts")
    all_posts = cursor.fetchall()
    return {"Data": all_posts}

#Creates Post
#The default status code is 200, but it is recommended to use 201 while creating a data.
@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(post: Post):

    cursor.execute("""INSERT INTO public.posts (title, content, published, rating) VALUES (%s, %s, %s, %s) 
                      RETURNING *""", (post.title, post.content, post.published, post.rating))
    new_post = cursor.fetchall()
    database_connect.commit() #This saves the new post to Database.

    return {"Data": new_post}

@app.get("/posts/latest")
async def get_latest_post():
    cursor.execute("""SELECT * FROM public.posts ORDER BY created_at""")
    post = cursor.fetchone()
    return {"Latest Post: ": post}

@app.get("/posts/{id}")
async def post_by_id(id: int):
    cursor.execute("""SELECT * FROM public.posts WHERE id = {0}""".format(id))
    post = cursor.fetchall()

    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with ID: {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to find post with ID: {id} does not exist.")
    return {"Post": post}

# HTTP Status 204 (No Content) indicates that the server has successfully fulfilled the request
# and that there is no content to send in the response payload body.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):

    cursor.execute("""DELETE FROM public.posts WHERE id = {0} RETURNING *""".format(id))
    deleted_post = cursor.fetchone()
    print(deleted_post)
    database_connect.commit()

    #Chech if the index is there in the ID.
    if deleted_post == None:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with ID: {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to delete post with ID: {id} does not exist.")     

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update Post
@app.put("/posts/{id}")
async def update_post(id: int, post: Post):

    cursor.execute("""UPDATE public.posts SET title=%s, content=%s, published=%s, rating=%s 
    WHERE id=%s RETURNING *""", (post.title, post.content, post.published, post.rating, str(id)))
    updated_post = cursor.fetchone()
    database_connect.commit() #This saves the new post to Database.

    #Chech if the index is there in the ID.
    if updated_post == None:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with ID: {id} does not exist."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Unable to Update post with ID: {id} does not exist.")

    return {"data": updated_post}
