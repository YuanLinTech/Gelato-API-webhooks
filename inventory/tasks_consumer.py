import csv
from flask import request
from init_consumer import app, socketio
import json

# Receive the webhook requests and emit a SocketIO event back to the client
def send_message(data):
    status_code = 0
    if request.method == 'POST':
        roomid = app.config['uid']
        msg = json.dumps(data)
        event = "Send_stock_status"
        socketio.emit(event, msg, namespace = '/collectHooks', room = roomid)
        status_code = 200
    else:
        status_code = 405 # Method not allowed
    return status_code
    
# Retrieve the stock status of the products sent through the webhook requests and return them back to the client.   
def sendStockStatus():
    request_data = request.get_json()
    stockList = [] # List of products in stock
    stockInfo = [] # List of products sent in the request
    stockSheet = {} # Dictionary of products sent in the request and their stock status
    with open("NZ_NVJ_Apparel_SKUs_sheet.csv", newline='') as csvFile:
        stockReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in stockReader:
            stockList.append(row[0])
    
    if request_data:
        if 'SKU' in request_data:
            stockInfo = request_data['SKU']
            for stock in stockInfo:
                if stock in stockList:
                    stockSheet.update({str(stock):"In Stock"})
                else:
                    stockSheet.update({str(stock):"Out of Stock"})
    send_message(stockSheet)
    print(stockSheet)
    return stockSheet
