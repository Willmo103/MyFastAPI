from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Will10351432!@localhost/Fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# code for raw sql database connection
#
# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor
#
#
# while True:
#     try:
#         connection = psycopg2.connect(host='localhost', database='Fastapi',
#                                       user="postgres", password="Will10351432!", cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)
