from . import app
from flask import Markup
import mistune as md

@app.template_filter()
def markdown(text):
    return Markup(md.markdown(text,escape=True))

@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    return date.strftime(format)


# Thoughts
# - check whether entry author is the user?
# - check whether admin in is one of the roles

@app.template_filter()
def author_check(user, entry):
    return user.id == entry.author_id or "Admin"\
    in [role.role_name for role in user.roles]
    #     return True
    # else:
    #     return False

        # {allowed: True}
