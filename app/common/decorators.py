import re
from functools import wraps
from flask import request
from app.models.users import Users as User

def authenticate(func):
    wraps(func)
    def inner_methos(*args,**kwargs):
        if "Authorization" in request.headers:
            token=request.headers.get("Authorization")
            user=User.verify_token(token)
            if user:
                kwargs['user']=user
                kwargs['token']=token
                return func(*args,**kwargs)
            else:
                return {"status":"failed","message":"Not authorised"},409
        else:
            return {"status":"failed","message":"Not authorised"},409
    inner_methos.__doc__=func.__doc__
    return inner_methos