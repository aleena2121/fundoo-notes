import os

from dotenv import load_dotenv

from app.utils.exceptions import RequiredEnvVarError

load_dotenv()


def get_required_env(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise RequiredEnvVarError(var_name)
    return value


DB_USER = get_required_env("DB_USER")
DB_PASSWORD = get_required_env("DB_PASSWORD")
DB_HOST = get_required_env("DB_HOST")
DB_PORT = get_required_env("DB_PORT")
DB_NAME = get_required_env("DB_NAME")

SECRET_KEY = get_required_env("SECRET_KEY")
ALGORITHM = "HS256"

UVICORN_HOST = get_required_env("UVICORN_HOST")
UVICORN_PORT = int(get_required_env("UVICORN_PORT"))

SMTP_SERVER = get_required_env("SMTP_SERVER")
SMTP_PORT = int(get_required_env("SMTP_PORT"))
SMTP_USERNAME = get_required_env("SMTP_USERNAME")
SMTP_PASSWORD = get_required_env("SMTP_PASSWORD")
BACKEND_URL = get_required_env("BACKEND_URL")
EMAIL_FROM = get_required_env("EMAIL_FROM")
