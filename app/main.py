import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/home")
def home():
    return {"location": "Home"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # connection.commit()
    # new_post = cursor.fetchone()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.")
    return {"post": post}


@app.delete("/posts/{id}")
def delete_post(id: str, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # post = cursor.fetchone()
    # connection.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} no longer exists.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    original_post = post_query.first()
    if original_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} no longer exists.")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}

