from environs import Env

env = Env()
env.read_env()


class Config:
    """Set Flask configuration vars."""

    # Database
    SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = env.bool(
        'SQLALCHEMY_TRACK_MODIFICATIONS', default=False)
