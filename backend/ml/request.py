import requests
import os

url = "http://127.0.0.1:8083/rank_shops/"
file_path = "mock_shop_feedback.csv"

with open(file_path, "rb") as file:
    files = {"file": file}
    response = requests.post(url, files=files)

print(response.json())