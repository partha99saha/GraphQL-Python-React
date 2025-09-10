from jose import jwt
from config import Config
from database import SessionLocal
from models import User
from flask import request


def create_jwt(user):
    payload = {"user_id": user.id, "username": user.username}
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token


def get_user_from_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        db = SessionLocal()
        return db.query(User).get(user_id)
    except Exception:
        return None


# GraphQL & Flask context helper
def context_from_request(req):
    auth = req.headers.get("Authorization")
    user = None
    if auth and auth.startswith("Bearer "):
        token = auth.split(" ", 1)[1]
        user = get_user_from_token(token)
    return {"request": req, "user": user}
