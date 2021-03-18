import requests

url = "http://34.121.67.167/pets-service/service-path-3"

payload={}
headers = {
  'Host': 'app.pets'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
