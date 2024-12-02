from pymongo import MongoClient
from urllib.parse import quote_plus

# Encode the password to be URL-safe
password = quote_plus('1215Hexa@')

# Construct the MongoDB URI
uri = f"mongodb+srv://anshbhatia85656:{password}@cluster0.zaz2u.mongodb.net/"

# Create a MongoClient
client = MongoClient(uri)

# Test the connection
try:
    client.server_info()  # This raises an exception if the server is not reachable
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
