# Send_HTTP_POST_Request

import requests

def handler(pd: "pipedream"):
    url = "https://jsonplaceholder.typicode.com/todos/1"
    body = pd.steps["trigger"]["event"]["body"]["SKU"]
    header = {"Content-Type":"application/json"}
    r = requests.post(url, json=body, headers=header, timeout=5)
    product_skus = pd.steps["trigger"]["event"]["body"]["SKU"]
    # print(pd.steps["trigger"]["context"]["id"])
    # Return data for use in future steps
    return product_skus