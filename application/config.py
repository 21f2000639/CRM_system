class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS =True
    
class LocalDevelopmentConfig(Config):
    #CONFIG OF DATABASES
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.sqlite3"
    DEBUG = True
    
    #config for security
    SECRET_KEY = "This-is-secret"  #hash user creds in session
    SECURITY_PASSWORD_HASH = "bcrypt" # mechanism for hashing password
    SECURITY_PASSWORD_SALT = "This-is-secret-salt" #helps in hashing password
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    
