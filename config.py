import os
from dotenv import load_dotenv

load_dotenv()


DB_PARAMS = {
    'dbname': os.getenv("DBNAME_PG"),
    'user': os.getenv("USER_PG"),
    'password': os.getenv("PASSWORD_PG"),
    'host': os.getenv("HOST_PG"),
    'port': os.getenv("PORT_PG"),
}