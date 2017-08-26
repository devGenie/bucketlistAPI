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

def validate(params):
    def validate_wrapper(func):
        wraps(func)

        def inner_method(*args, **kwargs):
            errors = {'missing': [], 'errors': []}
            for key in params.keys():
                if key in request.data:
                    if len(request.data.get(key))>0:
                        if params[key]['type'] == 'integer':
                            regexp=re.compile(r"(^[0-9]*$#)")
                            compare=request.data.get(key)
                            if not regexp.match(compare):
                                errors['errors'].append({'value':compare,'field type':key,'message':'Please provide a valid integer'})

                        if params[key]['type'] == 'text':
                            regexp=re.compile(r"(^[a-zA-Z0-9]*$)")
                            compare=request.data.get(key)
                            if not regexp.match(compare):
                                errors['errors'].append({'value':compare,'field type':key,'message':'Please provide a valid string'})
                            else:
                                if 'min-length' in params[key] and len(compare.strip()) < params[key]['min-length']:
                                    errors['errors'].append({'value':compare,'field type':key,'message':'Minimum length reached'})
                                    

                        if params[key]['type'] == 'email':
                            address = re.compile(
                                r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
                            compare=request.data.get(key)
                            if not address.match(compare):
                                errors['errors'].append({'value':compare,'field type':key,'message':'Please provide a valid email'})
                    else:
                        errors['missing'].append(key)
                else:
                    errors['missing'].append(key)

            if len(errors['missing'])>0 or len(errors['errors'])>0:
                return {'status':'failed','message':'Please check your input','errors':errors},400
            else:
                return func(*args,**kwargs)

        inner_method.__doc__ = func.__doc__
        return inner_method
    return validate_wrapper
