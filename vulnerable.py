import requests

# testing  
response = requests.get("https://example.com")
print(response.text)

# testing
aws_access_key = "AKIAIOSFODNN7EXAMPLE"
aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

print(f"Using AWS key: {aws_access_key}")
