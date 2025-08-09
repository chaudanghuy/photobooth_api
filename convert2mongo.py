import sqlite3
from pymongo import MongoClient

# === CONFIG ===
SQLITE_DB_PATH = "db.sqlite3"  # Path to your SQLite file
MONGO_URI = "mongodb+srv://photobooth:2j1cN7oFmtEIZWtL@ahihi.ccg1k.mongodb.net/?retryWrites=true&w=majority&appName=Ahihi"
MONGO_DB_NAME = "photobooth"  # Name for your MongoDB database

# === Connect to SQLite ===
sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
sqlite_cursor = sqlite_conn.cursor()

# === Connect to MongoDB ===
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

# === Get all tables from SQLite ===
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

for table_name_tuple in tables:
    table_name = table_name_tuple[0]
    print(f"Processing table: {table_name}")

    # Fetch all rows from this table
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()

    # Get column names
    col_names = [description[0] for description in sqlite_cursor.description]

    # Prepare data for MongoDB
    documents = []
    for row in rows:
        doc = dict(zip(col_names, row))
        documents.append(doc)

    if documents:
        mongo_collection = mongo_db[table_name]
        mongo_collection.insert_many(documents)
        print(f"Inserted {len(documents)} rows into MongoDB collection '{table_name}'.")

# Close connections
sqlite_conn.close()
mongo_client.close()

print("Migration completed successfully!")
