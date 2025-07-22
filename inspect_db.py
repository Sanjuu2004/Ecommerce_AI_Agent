import sqlite3

conn = sqlite3.connect("database/ecommerce.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Show columns for each table
for table in tables:
    print(f"\nSchema for table: {table[0]}")
    cursor.execute(f"PRAGMA table_info({table[0]});")
    for col in cursor.fetchall():
        print(col)

conn.close()
