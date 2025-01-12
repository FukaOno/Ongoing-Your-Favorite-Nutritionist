import requests

url = "https://api.nal.usda.gov/fdc/v1/food/534358"
headers = {
    "accept": "application/json",
    "X-Api-Key": ERHfvD18nmDcTiMrS4u9Ol5VzNH126WDgbjdI6fR  
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())  # Display the food data
else:
    print(f"Error: {response.status_code}, Message: {response.json()}")
