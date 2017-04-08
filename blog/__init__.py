import os
#operating sys --- system to access env
from flask import Flask
#import principal
# from flask.ext.principal import Principal, Permission, RoleNeed

# from flask_permissions.core import Permissions
# from flask_login import LoginManager, current_user
# from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
#name is stand value
# import pdb; pdb.set_trace()
# db = SQLAlchemy(app)
# perms = Permissions(app, db, current_user)

#load the extension
# principals = Principal(app)


config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import views
from . import filters
from . import login
