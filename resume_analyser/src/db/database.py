
import motor
from .config import MONGODB_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.college
