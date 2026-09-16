"""Application configuration."""
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    DEBUG = False
    TESTING = False
    DATA_FILE = os.path.join(BASE_DIR, "data", "tasks.csv")


class DevConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATA_FILE = os.path.join(BASE_DIR, "data", "test_tasks.csv")
