import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"🔍 DATABASE_URL = {DATABASE_URL}")  # Debug temporal
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "BONOSECRETO123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
