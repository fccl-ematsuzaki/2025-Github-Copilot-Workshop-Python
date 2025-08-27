# Configuration settings for the Pomodoro Timer application

class Config:
    # Default timer settings
    DEFAULT_WORK_DURATION = 25  # minutes
    DEFAULT_BREAK_DURATION = 5  # minutes
    DEFAULT_LONG_BREAK_DURATION = 15  # minutes
    DEFAULT_SESSIONS_BEFORE_LONG_BREAK = 4
    
    # Application settings
    SECRET_KEY = "dev"  # Change this in production
    DEBUG = True
    TESTING = False


class TestConfig(Config):
    TESTING = True
    DEBUG = True
