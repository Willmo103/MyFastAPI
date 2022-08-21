from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# this is to hash passwords so as not to save them as plain text
# in the database.


def hash(password: str):
    return pwd_context.hash(password)
