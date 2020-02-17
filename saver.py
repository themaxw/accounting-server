import sqlite3
import datetime
#from appJar import gui
from config import baseDir, users
from os import path

import sqlalchemy
from sqlalchemy import create_engine

def insertBon(c, total, shop, buyer, date=None):
	if date is None:
		date = datetime.datetime.now().strftime("%Y-%m-%d")
	c.execute("INSERT INTO bons(Total, Shop, Buyer, Date) VALUES(?,?,?,?)", (total, shop, buyer, date))
	c.execute("select last_insert_rowid()")
	return c.fetchone()

def enterBon(c):
	name = ''
	while name not in users:
		name = input("name: ")
	shop = input("shop: ")
	total = float(input("total: "))
	date = input("date (YYYY-MM-DD): ")
	if date == "":
		date = None

	purchaseId = insertBon(c, total, shop, name, date)
	print(purchaseId)

def setup():
	print(path.join(baseDir, 'resources', 'purchases'))
	conn = sqlite3.connect(path.join(baseDir, 'resources', 'purchases'))
	return conn

def close(conn):
	conn.commit()
	conn.close()

def enterBonData(total, shop, buyer, date):
	conn = setup()
	c = conn.cursor()
	#check inputs
	purchaseId = insertBon(c, total, shop, buyer, date)
	close(conn)
	return purchaseId

def enterItem(purchaseId, productName, price, amount):
	conn = setup()
	c = conn.cursor()
	c.execute("select shop from bons where purchaseId = ?", (purchaseId,))
	shop = c.fetchone()[0]
	print(shop)

	c.execute("select exists (select ProductId from products where productName = ? and Shop = ?)", (productName, shop))
	if c.fetchone()[0] == 0:
		c.execute("insert into products(productName, Price, Shop) VALUES (?, ?, ?)", (productName, price, shop) )
		c.execute("select last_insert_rowid()")

		productId = c.fetchone()[0]
	else:
		c.execute("select ProductId from products where productName = ? and Shop = ? LIMIT 1", (productName, shop))
		productId = c.fetchone()[0]

	c.execute("select exists (select purchaseId from items where purchaseId = ? and ItemId = ?)", (purchaseId, productId))
	if c.fetchone()[0] == 1:
		c.execute("select amount from items where purchaseId = ? and ItemId = ?", (purchaseId, productId))
		oldAmount = c.fetchone()[0]
		c.execute("Update items set amount=? where purchaseId = ? and ItemId = ?", (oldAmount+amount, purchaseId, productId))
	else:
		c.execute("insert into items(purchaseId, ItemId, Price, Amount) VALUES (?,?,?,?)", (purchaseId, productId, price, amount))
	close(conn)
	return purchaseId

def getList():
	conn = setup()
	c = conn.cursor()
	c.execute("select * from bons")
	bons = c.fetchall()
	close(conn)
	bons.sort(key=lambda bon: bon[4], reverse=True)
	return bons

def getItems(purchaseId):
	conn = setup()
	c = conn.cursor()
	c.execute("select products.productName, items.Price, items.amount, items.ItemId from items inner join products on items.ItemId = products.productId where items.purchaseId = ?", (purchaseId, ))
	items = c.fetchall()
	close(conn)
	return items

def deleteItem(purchaseId, itemId):
	conn = setup()
	c = conn.cursor()
	c.execute("delete from items where purchaseId=? and itemId=?", (purchaseId, itemId))
	close(conn)

def getBon(purchaseId):
	conn = setup()
	c = conn.cursor()
	c.execute("select * from bons where purchaseId = ?", (purchaseId,))
	bon = c.fetchall()
	close(conn)
	return bon[0]



if __name__ == '__main__':
	print(getList())
