import os
from dotenv import find_dotenv, load_dotenv


env_file = find_dotenv(".env.dev")
load_dotenv(env_file)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    DB_TABLE_NAME = os.environ.get("DB_TABLE_NAME", "test")
    TEST_DATA_PATH = os.environ.get("TEST_DATA_PATH", "./")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DB_URI", "sqlite:///" + os.path.join(basedir, "db.sqlite3")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
