import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = str(
    os.environ.get("SQLALCHEMY_DATABASE_URL", "fake_sqlalchemy_database_url")
)

# SQLALCHEMY_DATABASE_URL = str(
#     os.environ.get("SQLALCHEMY_DATABASE_URL", "fake_sqlalchemy_database_url")
# )
