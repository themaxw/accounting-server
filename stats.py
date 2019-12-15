import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
import matplotlib.dates as dates
import numpy as np
import calendar
import datetime
import json
from os import path
from config import baseDir, blacklist, staticDir


def setup():
    conn = sqlite3.connect(path.join(baseDir, 'resources', 'purchases'))
    return conn

def close(conn):
    #conn.commit()
    conn.close()

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

def abrechnung(start='2018-01-01', end='2030-01-01'):    
    conn = setup()
    c = conn.cursor()

    c.execute('select * from bons where date(?)<= date and date < date(?)', (start, end))
    bons = c.fetchall()
    
    if len(bons) == 0:
        return 0, 0

    c.execute('select items.amount, items.price from items join products on items.itemid = products.productid where productname=? and items.purchaseId in (select purchaseid from bons where  date(?) <= date and date < date(?))', ('Cornflakes', start, end))
    cornflakes = c.fetchall()
    cSum = 0
    for flake in cornflakes:
        cSum = cSum + (int(flake[0])*float(flake[1]))

    bonsNp = np.asarray(bons)
    total = np.sum(bonsNp[:,1].astype(np.float)) -cSum

    bonsMax = [bon for bon in bons if bon[3]=='Max']
    if len(bonsMax)==0:
        return total, 0

    bonsMaxNp = np.asarray(bonsMax)
    totalMax = np.sum(bonsMaxNp[:,1].astype(np.float)) -cSum
    maxDiff = totalMax - (total/2)
    a = 'Max {} {} Euronen.'.format('zahlt ' if maxDiff<0 else 'kriegt ', "%.2f" % abs(maxDiff))
    print(a)
    return total, totalMax, a

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
    

def update():
    totalGraph()
    cornflakesGraph()
    getMonthSpendings()
    getTotalSpendings()

def getAutocompleteList(field, table):
    conn = setup()
    c = conn.cursor()
    print(field, table)
    if table == 'bons':
        c.execute("select {} from bons".format(field))
    elif table == 'products':
        c.execute("select {} from products".format(field))
    else:   
        c.execute("select {} from items".format(field))

    items = c.fetchall()
    tmp = {}
    for i in items:
        i = i[0]
        if i in tmp.keys():
            tmp[i] = tmp[i]+1
        else:
            tmp[i] = 1
    close(conn)
    return sorted(list(tmp.keys()), key=lambda x: tmp[x], reverse=True)

def getProductStats():
    
    products = [p for p in getAutocompleteList('productName', 'products') if p not in blacklist]

    conn = setup()
    c = conn.cursor()
    pList = []
    for product in products:
        if product in blacklist:
            continue

        c.execute("select price, amount from items where itemid in (select productid from products where productName=?)", (product, ))
        tmp = c.fetchall()
        total = sum([float(t[0])*int(t[1]) for t in tmp])
        amt = sum([int(t[1]) for t in tmp])
        pList.append((product, total, amt))


    close(conn)
    return sorted(pList, key=lambda x: x[1],reverse=True)

def getMonthSpendings(start:str = None, nProducts:int = 15):

    if start == None:
        start = datetime.datetime.now().strftime("%Y-%m-01")
    end = add_months(datetime.datetime.strptime(start, "%Y-%m-%d"), 1)

    conn = setup()
    c = conn.cursor()
    
    c.execute('select products.productName, items.price, items.amount from items join products on items.itemid = products.productid where items.purchaseId in (select purchaseid from bons where  date(?) <= date and date < date(?))', (start, end))
    spendings = c.fetchall()
    d = {}
    for s in spendings:
        if s[0] in blacklist:
            continue

        if s[0] in d:
            d[s[0]] =  d[s[0]] + s[1]*s[2]

        else:
            d[s[0]] =  s[1]*s[2]

    sortedSpendings = sorted(d.items(), key=lambda kv: kv[1], reverse=True)
    jsonlist = {'labels': [], 'values': []}
    for k in sortedSpendings[:nProducts]:
        jsonlist['labels'].append(k[0])
        jsonlist['values'].append(k[1])
    jsonlist['labels'].append('Sonstige')
    jsonlist['values'].append(sum([p[1] for p in sortedSpendings[nProducts:]]))

    close(conn)
    with open(path.join(baseDir, "resources", "month.json"), 'w') as f:
        json.dump(jsonlist, f)

def getTotalSpendings(nProducts = 15):
    
    productlist = getProductStats()
    
    jsonlist = {'labels': [], 'values': []}
    for p in productlist[:nProducts]:
        jsonlist['labels'].append(p[0])
        jsonlist['values'].append(p[1])
    jsonlist['labels'].append('Sonstige')
    jsonlist['values'].append(sum([p[1] for p in productlist[nProducts:]]))

    with open(path.join(baseDir, "resources", "totaldist.json"), 'w') as f:
        json.dump(jsonlist, f)



def getSingleProductStats(productName):
    conn = setup()
    c = conn.cursor()

    c.execute("select productid, shop, price from products where productName=?", (productName, ))
    ids = c.fetchall()
    stats = []
    for i in ids:
        c.execute("select bons.date, items.price, items.amount from items join bons on items.purchaseId=bons.purchaseId where items.itemId = ?", (i[0], ))
        items = c.fetchall()
        total = sum([float(t[1])*int(t[2]) for t in items])
        avgPrice = total/sum([int(t[2]) for t in items])
        stats.append((i[1], avgPrice, total, items))
    close(conn)
    return stats

if __name__ == '__main__':
    getMonthSpendings("2019-10-01")




