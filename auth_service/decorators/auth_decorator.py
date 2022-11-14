from functools import wraps
from flask import session

from ..constants import resources


def check_session(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        print(kwargs)
        print(args)
        if session.get('authenticated') is None:
            return {'success': False, 'errors': [{'message': resources.UNAUTHENTICATED}]}, 403
        return func(*args, **kwargs)
    return wrapper_func
