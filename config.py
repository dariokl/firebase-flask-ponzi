import os

from dotenv import load_dotenv
load_dotenv()


class Config():
    """
    Used as main config file as application grow it can be very handy in handling separate
    config environments like "production", "development" etc...

    """

    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True


config = {
    'default': Config,
    'development': Development
}