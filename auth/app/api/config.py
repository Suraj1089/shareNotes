# secret keys
import os 
# SECRET_KEY = "7ed9af7637a82337a725d23f4fff51af2cfb6ff178304d1c55614b24df4c9926"

# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')