from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb+srv://admin:1234@cluster0.4ahsat4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(uri)


async def get_db():
    global client
    if client is None:
        try:
            client = AsyncIOMotorClient(uri)
            await client.server_info()
            print("Database is connected successfully.")
        except Exception as e:
            print("Could not connect to the database. Error:", e)
            raise
    return client.voicense_db
