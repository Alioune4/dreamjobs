class Config:
    """Base configuration."""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://dreamjobs:dreamjobs@localhost:5432/dreamjobs"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "c6cb1e67f6cc9b808152f7f46963912da411bb2fffb1a192eb23df76b9197edb"
