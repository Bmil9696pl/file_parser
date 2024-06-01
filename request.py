import requests

url = 'http://localhost:8000/parse/'
file_path = '/Users/bartlomiejmilecki/Documents/vscode/spotOn/example.json'

with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

print(response.json())