import os
from flask_login import UserMixin
from dotenv import load_dotenv

load_dotenv()

class User(UserMixin):

# where username is simply the value of id method of UserMixin uses in cookie session to reconstruct class User
    def __init__(self, username):
        self.id = username


    @staticmethod
    def validate(username: str, password: str) -> bool:
        return(
            username == os.getenv("LOGIN_USERNAME")
            and
            password == os.getenv("LOGIN_PASSWORD")
        )
