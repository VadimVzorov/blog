from flask import redirect, url_for
from functools import wraps



def check_role (user=None, roleType=[]):
    def decorator (f):
        @wraps(f)
        def check_for_role(*args, **kwargs):
            if user:
                for req_role in roleType:
                    if req_role in [role.role_name for role in user.roles]:
                        return f(*args, **kwargs)
                return redirect(url_for("entries", page=1))
            else:
                redirect(url_for("entries", page=1))
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
                redirect(url_for("entries", page=1))
        return check_for_author(*args, **kwargs)
    return decorator
