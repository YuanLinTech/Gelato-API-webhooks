import csv
from flask import request
from init_consumer import app, socketio
import json

# Receive the webhook requests and emit a SocketIO event back to the client
def send_message(data, roomid):
    if request.method == 'POST':
        var = json.dumps(data)
        socketio.emit(event = 'Send_stock_status', message = var, namespace = '/collectHooks', room = roomid)
    return 'OK'

def sendStockStatus():
    with open('NZ_NVJ_Apparel_SKUs_sheet.csv', newline='') as csvFile:
        stockReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        SKUlist = []
        for row in stockReader:
             SKUlist.append(row[0])
