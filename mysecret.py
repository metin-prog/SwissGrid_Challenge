import requests
import sqlite3

# Connect to an in-memory database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create a simple table
cursor.execute("CREATE TABLE users (id INTEGER, username TEXT)")

# Simulate untrusted user input
user_input = "1 OR 1=1"

# SECURITY VULNERABILITY: SQL Injection
query = f"SELECT * FROM users WHERE id = {user_input}"
cursor.execute(query)
results = cursor.fetchall()

print(f"Query results: {results}")
