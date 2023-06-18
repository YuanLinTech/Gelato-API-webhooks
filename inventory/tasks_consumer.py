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
    SKUlist = []
    stockSheet = {}
    with open("NZ_NVJ_Apparel_SKUs_sheet.csv", newline='') as csvFile:
        stockReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in stockReader:
            SKUlist.append(row[0])
    if request.method == 'POST':
        stockInfo = request.json
        stockStr = str(stockInfo) # Since "stockInfo" is a dict, it has to be converted into a JSON string to be parsed.
        stockStr = stockStr.replace("\'", "\"") # As JSON only allows enclosing strings with double quotes, use this statement to replace single \' with \"
        stockDict = json.loads(stockStr) # Convert JSON string to dictionary
        for stock in stockDict["SKU"]:
            if stock in SKUlist:
                stockSheet.update({str(stock):"In Stock"})
            else:
                stockSheet.update({str(stock):"Out of Stock"})
    send_message(stockSheet)
    # print(stockSheet)
    return stockSheet
