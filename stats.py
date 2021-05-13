import sqlite3
import matplotlib

import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import calendar
import datetime
import json
from os import path
import db
import statistics

def setup():
    session = Session()
    return session


def parseDate(date):
    tmp = date.replace('-', '')
    dateParsed = int(tmp)
    return dateParsed

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


def dateFrame(start=None, end=None, resolution=7, byMonths=False):
    if start == None:
        start = datetime.datetime.now().strftime("%Y-01-01")
    if end == None:
        eyear = int(datetime.datetime.now().strftime("%Y"))+1
        end = "{}-01-01".format(eyear)
    

    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")

    delta = end - start
    frame = []
    if byMonths:
        for i in range(0, int(delta.days/30)):
            frame.append(add_months(start, i).strftime("%Y-%m-%d"))
    else:
        for i in range(0, delta.days + 1, resolution):
            frame.append((start + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
    return frame


def totalGraph(start=None, end=None, resolution=7):
    frame = dateFrame(start, end, resolution, byMonths=True)
    values = []
    for s, e in zip(frame, frame[1:]):
        values.append(abrechnung(s, e)[0])
    c = {'labels': [datetime.datetime.strptime(f, "%Y-%m-%d").strftime("%m.%Y") for f in frame[:-1]], 'values': values}
    with open(path.join(baseDir, "resources", "total.json"), 'w') as f:
        json.dump(c, f)

def cornflakesGraph(start=None, end=None, resolution=15):
    frame = dateFrame(start, end, resolution=resolution,  byMonths=True)
    values = []

    conn = setup()
    c = conn.cursor()
    for s, e in zip(frame, frame[1:]):
        c.execute('select items.amount, items.price from items join products on items.itemid = products.productid where productname=? and items.purchaseId in (select purchaseid from bons where  date(?) <= date and date < date(?))', ('Cornflakes', s, e))
        cornflakes = c.fetchall()
        cSum = 0.
        for flake in cornflakes:
            cSum = cSum + (int(flake[0])*float(flake[1]))
        values.append(cSum)
    
    close(conn)

    c = {'labels': [datetime.datetime.strptime(f, "%Y-%m-%d").strftime("%m.%Y") for f in frame[:-1]], 'values': values}
    with open(path.join(baseDir, "resources", "cornflakes.json"), 'w') as f:
        json.dump(c, f)

def singleProductGraph(productName, start=None, end=None, resolution=15):
    frame = dateFrame(start, end, resolution=resolution,  byMonths=True)
    values = []

    conn = setup()
    c = conn.cursor()
    for s, e in zip(frame, frame[1:]):
        c.execute('select items.amount, items.price from items join products on items.itemid = products.productid where productname=? and items.purchaseId in (select purchaseid from bons where  date(?) <= date and date < date(?))', (productName, s, e))
        cornflakes = c.fetchall()
        cSum = 0.
        for flake in cornflakes:
            cSum = cSum + (int(flake[0])*float(flake[1]))
        values.append(cSum)
    
    close(conn)

    c = {'labels': [datetime.datetime.strptime(f, "%Y-%m-%d").strftime("%m.%Y") for f in frame[:-1]], 'values': values}
    
    return c

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def scatterPlotFrequency(productName):
    purchases = db.getProductPurchasesOrdered(productName)
    datapoints = []


    for pred, succ in zip(purchases, purchases[1:]):
        print(f"{succ['date'] - pred['date']}, {pred['amount']}, {succ['amount']}")
        timedelta = (succ['date'] - pred['date'])/pred['amount']
        timedelta = timedelta/datetime.timedelta(days=1)
        datapoints.extend([timedelta] * pred['amount'])
        
    datapoints = np.array(datapoints)
    datapoints = reject_outliers(datapoints)
    plt.hist(x=datapoints, bins="auto", alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    
    print(f"mean: {statistics.mean(datapoints)}")
    print(f"deviation: { statistics.stdev(datapoints)}")
    plt.show()


if __name__ == '__main__':
    scatterPlotFrequency("Cornflakes")