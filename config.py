import os


basedir = os.path.abspath(os.path.dirname(__file__))


def env_flag(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_database_uri():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url
    return "sqlite:///" + os.path.join(basedir, "zirel.db")


def get_engine_options():
    database_url = os.environ.get("DATABASE_URL", "")
    if database_url.startswith(("postgres://", "postgresql://")):
        return {}
    return {
        "connect_args": {
            "timeout": 15,
        },
    }


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    WISHLIST_MODE = env_flag("WISHLIST_MODE", default=False)
    CLOSED_BETA_INVITES = env_flag("CLOSED_BETA_INVITES", default=True)
    BETA_ACCOUNT_LIMIT = int(os.environ.get("BETA_ACCOUNT_LIMIT", "100"))
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = get_engine_options()
