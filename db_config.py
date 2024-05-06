from motor.motor_asyncio import AsyncIOMotorClient
import logging

uri = "mongodb+srv://admin:1234@cluster0.4ahsat4.mongodb.net/"
client = None


async def get_db():
    global client
    if client is None:
        try:
            client = AsyncIOMotorClient(uri)
            await client.server_info()  # Asynchronous server information check
            logging.info("Database is connected successfully.")
        except Exception as e:
            logging.error("Could not connect to the database. Error:", e)
            raise  # Re-raise the exception for proper error handling
    return client.voicense_db  # Access the "voicense_db" database Re-raise the exception for proper error handling
