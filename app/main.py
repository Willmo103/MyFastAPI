import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine
from . import schemas, models, utils
from . routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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



app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/home")
def home():
    return {"location": "Home"}

