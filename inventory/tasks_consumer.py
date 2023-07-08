import csv
from flask import request, stream_with_context
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
@app.route('/consumetasks', methods=['POST'])
def sendStockStatus():
    stockList = [] # List of products in stock
    with open("NZ_NVJ_Apparel_SKUs_sheet.csv", newline='') as csvFile:
        stockReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in stockReader:
            stockList.append(row[0])
    
    # stockSheet = {} # Dictionary of products sent in the request and their stock status

    def generateStockStatus():
        request_data = request.get_json()
        stockSheet = {} # Dictionary of products sent in the request and their stock status
        if request_data:
            if 'SKU' in request_data:
                stockRequest = request_data['SKU'] # List of products sent in the request
                for stock in stockRequest:
                    if stock in stockList:
                        stockStatus = "In Stock"
                        stockSheet.update({str(stock):stockStatus})
                    else:
                        stockStatus = "Out of Stock"
                        stockSheet.update({str(stock):stockStatus})

                    send_message(stockSheet)
                    yield str(stock)
                    yield stockStatus
                        
    return stream_with_context(generateStockStatus())