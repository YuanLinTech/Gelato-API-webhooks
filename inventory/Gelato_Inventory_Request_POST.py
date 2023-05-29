import requests

def handler(pd: "pipedream"):
    url = "https://jsonplaceholder.typicode.com/todos/1"
    body = {
        "version": "1.0",
        "SKU": [
            "001-HOODIE-YEL-XL",
            "002-HOODIE-YEL-L",
            "003-HOODIE-YEL-M"
        ]
    }
    header = {"Content-Type":"application/json"}
    r = requests.post(url, json=body, headers=header)
    data = r.json()
    # print(pd.steps["trigger"]["context"]["id"])
    # Return data for use in future steps
    return data