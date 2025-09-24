import pickle
import subprocess
#test
data = b"cos\nsystem\n(S'ls'\ntR."
try:
    obj = pickle.loads(data) 
except Exception as e:
    print(f"Deserialization error: {e}")
  
user_input = "ls"  # simulate untrusted input
subprocess.call(user_input, shell=True)  # unsafe: shell=True
