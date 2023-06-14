import csv

SKUlist = []

# Receive the webhook requests and emit a SocketIO event back to the client
@app.route('/consumetasks', methods=['POST'])
def consume_tasks():
    if request.method == 'POST':
        data = request.json
        if data:
           print("Received Data = ", data)
           roomid =  app.config['uid']
           var = json.dumps(data)
           send_message(event='msg', namespace='/collectHooks', room=roomid, message=var)
    return 'OK'

def sendStockStatus():
    with open('NZ_NVJ_Apparel_SKUs_sheet.csv', newline='') as csvFile:
        stockReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in stockReader:
             SKUlist.append(row[0])
