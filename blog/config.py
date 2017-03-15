import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://vadimvzorov:@localhost:5432/blogful"
    DEBUG = True

class ProductionConfig(object):
    DEBUG = True
