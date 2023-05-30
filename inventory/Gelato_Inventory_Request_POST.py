# Send_HTTP_POST_Request

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
    r = requests.post(url, json=body, headers=header, timeout=5)
    product_skus = pd.steps["trigger"]["event"]["body"]["SKU"]
    # print(pd.steps["trigger"]["context"]["id"])
    # Return data for use in future steps
    return product_skus

# Return_stock_status
def get_stock_status(product_SKUs):
    stock_status = {}
    for sku in product_SKUs:
        stock_status[sku] = 'In Stock'
    return stock_status

def handler(pd: "pipedream"):
    product_skus = pd.steps["Send_HTTP_POST_Request"]["$return_value"]
    stock_status = get_stock_status(product_skus)
    response = {'stock_status': stock_status}
    return response
