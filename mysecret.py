import requests

url = "https://httpbin.org/get"
response = requests.get(url)

print("Response status:", response.status_code)
print("Response body:", response.text[:100])