# workspace testing
import requests

url = "http://127.0.0.1:3000/uploadFrequency/Z7ZgpCJ05TPmWHc0mkBx"

# Replace 'file_path' with the actual path to the file you want to upload
file_path = rf"TestData\test1LHC.wav"
file_name = "test1LHC.wav"

headers = {
  'X-API-Key': 'DEFAULT_KEY',
  'Content-Type': 'multipart/form-data'
}

# Open the file in binary mode and read its contents
with open(file_path, 'rb') as file:
    files = {'file': (file_name, file)}

    # Send the request with the file
    response = requests.post(url, files=files , headers=headers)

print(response.text)
