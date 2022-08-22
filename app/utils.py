from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# this is to hash passwords so as not to save them as plain text
# in the database.
def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

