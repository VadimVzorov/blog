from flask import abort
from functools import wraps


def check_role (user=None, roleType=[]):
    def decorator (f):
        @wraps(f)
        def check_for_role(*args, **kwargs):
            if user:
                for req_role in roleType:
                    if req_role in [role.role_name for role in user.roles]:
                        return f(*args, **kwargs)
                return abort(403)
            else:
                abort(403)
        return check_for_role
    return decorator

def check_author (user=None, post=None):
    def decorator(f):
        @wraps(f)
        def check_for_author(*args, **kwargs):
            if user.id == post.author_id:
                return f(*args, **kwargs)
            elif "Admin" in [role.role_name for role in user.roles]:
                return f(*args, **kwargs)
            else:
                abort(403)
        return check_for_author(*args, **kwargs)
    return decorator
