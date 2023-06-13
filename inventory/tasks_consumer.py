import csv

SKUlist = []
def sendStockStatus():
    with open('NZ_NVJ_Apparel_SKUs_sheet.csv', newline='') as csvFile:
        stockReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in stockReader:
             SKUlist.append(row[0])
