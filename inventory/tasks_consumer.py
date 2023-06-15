import csv
from flask import request
from init_consumer import app, socketio
import json

# Receive the webhook requests and emit a SocketIO event back to the client
def send_message(data, roomid):
    status_code = 0
    if request.method == 'POST':
        var = json.dumps(data)
        socketio.emit(event = 'Send_stock_status', message = var, namespace = '/collectHooks', room = roomid)
        status_code = 200
    else:
        status_code = 405 # Method not allowed
    return status_code
    
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
                stockSheet.update({'stock_status':'In Stock'})
            else:
                stockSheet.update({'SKU':stock})
                stockSheet.update({'stock_status':'Out of Stock'})
    return stockSheet
