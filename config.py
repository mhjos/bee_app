class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rootpassword@db/bee_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey'
