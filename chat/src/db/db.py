import motor.motor_asyncio


# connect to mongodb database
async def connect(uri: str):
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client.chat
    return db

# close connection to mongodb database
async def close(client):
    client.close()