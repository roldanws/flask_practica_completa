class BaseConfig(object):
    SECRET_KEY = 'SecretKey'
    DEBUG = True
    TESTING = False
class ProductionConfig(BaseConfig):
    DEBUG = False
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'SecretKey'

