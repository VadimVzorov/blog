import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://vadimvzorov:@localhost:5432/blogful"
    DEBUG = True

class ProductionConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgres://hzyqgyzzrjtaom:5dc8aa5c47529024ef8c40951ab1866dae63d120e9d512055ac96848f6473cfd@ec2-54-225-67-3.compute-1.amazonaws.com:5432/dates3p8m82mhl"
    DEBUG = True
