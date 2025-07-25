import os
def build_sqlalchemy_uri():
    user = os.environ.get("DATABASE_USER")
    password = os.environ.get("DATABASE_PASSWORD")
    host = os.environ.get("DB_HOST")
    name = os.environ.get("DB_NAME")
    return f"mysql+pymysql://{user}:{password}@{host}:3306/{name}"