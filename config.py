class Config:
    """Base configuration."""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://dreamjobs:dreamjobs@localhost:5432/dreamjobs"
    SQLALCHEMY_TRACK_MODIFICATIONS = False