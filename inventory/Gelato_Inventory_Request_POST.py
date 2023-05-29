import requests
url = 'https://postman-echo.com/post'

data = {
  "version": "1.0",
  "SKU": [
    "001-HOODIE-YEL-XL",
    "002-HOODIE-YEL-L",
    "003-HOODIE-YEL-M"
  ]
}

headers = {"Content-Type":"application/json"}

r = requests.post(url, data, headers, timeout=5)

