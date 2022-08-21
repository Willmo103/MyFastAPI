import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        connection = psycopg2.connect(host='localhost', database='Fastapi',
                                      user="postgres", password="Will10351432!", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/home")
def home():
    return {"location": "Home"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    connection.commit()
    new_post = cursor.fetchone()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.")
    return {"post": post}


@app.delete("/posts/{id}")
def delete_post(id: str):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} no longer exists.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    connection.commit()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} no longer exists.")

    return {"data": post}
