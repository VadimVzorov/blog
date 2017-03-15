import os
from flask import Flask

app = Flask(__name__)
print(os.environ)
if 'HEROKU' in os.environ:
    # production on Heroku
    config_path = os.environ.get("CONFIG_PATH", "blog.config.ProductionConfig")
else:
    # development on localhost
    config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")

app.config.from_object(config_path)

from . import views
from . import filters
