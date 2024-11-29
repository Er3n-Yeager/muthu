import motor.motor_asyncio
from info import DATABASE_URI 
# Connect to your MongoDB database
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI )
db = client["Notes"]  # Specify you database name
premium_users_collection = db["premium_users"]  # Collection for premium users

# Function to get all premium user IDs

# Function to add a new premium user
# premium_users_db.py
  # Import your MongoDB collection

async def add_premium_user(user_id):
    """Adds a user ID to the premium users collection."""
    try:
        # Check if the user ID already exists to avoid duplicates
        existing_user = await premium_users_collection.find_one({"user_id": user_id})
        if not existing_user:
            # Insert the user ID without specifying an `_id` to avoid conflicts
            await premium_users_collection.insert_one({"user_id": user_id})
    except Exception as e:
        raise e

async def get_premium_users():
    """Fetches all premium user IDs from the collection."""
    try:
        # Retrieve all documents from the premium users collection
        users = await premium_users_collection.find().to_list(length=None)
        # Extract the user IDs from the documents
        return [user["user_id"] for user in users]
    except Exception as e:
        raise e
