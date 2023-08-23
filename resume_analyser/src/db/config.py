import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent.parent
MONGODB_URL = os.environ.get("MONGODB_URL")
