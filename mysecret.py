import requests
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE users (id INTEGER, username TEXT)")

user_input = "1 OR 1=1"

query = f"SELECT * FROM users WHERE id = {user_input}"
cursor.execute(query)
results = cursor.fetchall()

print(f"Query results: {results}")
