import requests
# test
login = {'username': 'mart', 'password': 'copy,wearechecking'}

response = requests.post("https://example.com", data=login)
print(response.text)
