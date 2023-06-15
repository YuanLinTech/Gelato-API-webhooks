import csv
from flask import request
from init_consumer import app, socketio
import json, uuid

# Create a unique session ID and store it within the application configuration file 
def initialize_params():
    if not hasattr(app.config,'uid'):
        sid = str(uuid.uuid4())
        app.config['uid'] = sid
        print("initialize_params - Session ID stored =", sid)

# Receive the webhook requests and emit a SocketIO event back to the client
def send_message(data):
    status_code = 0
    initialize_params()
    if request.method == 'POST':
        roomid = app.config['uid']
        var = json.dumps(data)
        socketio.emit(event = 'Send_stock_status', message = var, namespace = '/collectHooks', room = roomid)
        status_code = 200
    else:
        status_code = 405 # Method not allowed
    return status_code
    
# Retrieve the stock status of the products sent through the webhook requests and return them back to the client.   
def sendStockStatus():
    SKUlist = []
    stockSheet = {}
    with open('NZ_NVJ_Apparel_SKUs_sheet.csv', newline='') as csvFile:
        stockReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in stockReader:
            SKUlist.append(row[0])
    if request.method == 'POST':
        stockInfo = request.json
        stockDict = json.loads(stockInfo)
        for stock in stockDict['SKU']:
            if stock in SKUlist:
                stockSheet.update({'SKU':stock})
                stockSheet.update({'Stock_status':'In Stock'})
            else:
                stockSheet.update({'SKU':stock})
                stockSheet.update({'Stock_status':'Out of Stock'})
    send_message(stockSheet)
    return stockSheet
