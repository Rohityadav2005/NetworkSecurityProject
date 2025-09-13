import os
import sys
from dotenv import load_dotenv
load_dotenv()

MONGO_DOT_URL = os.getenv("MONGO_DB_URI")
print(MONGO_DOT_URL)

