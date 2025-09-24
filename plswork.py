import pickle
import subprocess
import sqlite3

insecure_serialized = b"cos\nsystem\n(S'echo vulnerable_deserialize'\ntR."
try:
    obj = pickle.loads(insecure_serialized)
    print("Deserialized object:", obj)
except Exception as e:
    print("Deserialization failed:", e)


user_command = "echo vulnerable_shell; rm -rf /tmp/nonexistent || true"

subprocess.call(user_command, shell=True)


conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT);")
cur.execute("INSERT INTO users (username) VALUES ('alice'), ('bob');")

user_input = "1 OR 1=1"  

query = f"SELECT * FROM users WHERE id = {user_input};"
print("Running query:", query)
cur.execute(query)
rows = cur.fetchall()
print("Query result count:", len(rows))
