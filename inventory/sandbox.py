import csv
with open('NZ_NVJ_Apparel_SKUs_sheet.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print(row)