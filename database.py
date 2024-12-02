import urllib.parse
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB username and password
username = "anshbhatia85656"
password = "1215Hexa@"  # Password containing special characters

# URL encode the username and password
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)
MONGO_URI = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.zaz2u.mongodb.net/?retryWrites=true&w=majority&ssl=true"
# Create an async MongoDB client
client = AsyncIOMotorClient(MONGO_URI)

# Access the database and collection
database = client["student_management"]
students_collection = database["students"]

# Helper function to initialize and return the DB collection
async def get_students_collection():
    return students_collection


# Create an async MongoDB client
try:
    client = AsyncIOMotorClient(MONGO_URI)
    # Test if the connection works by attempting to get the list of databases
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    raise Exception("Could not connect to MongoDB")


