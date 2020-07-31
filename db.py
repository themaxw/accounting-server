import statistics
import datetime

from config import baseDir, users, blacklist
from os import path
from collections import defaultdict
import sqlalchemy
from sqlalchemy import create_engine, ForeignKey, ForeignKeyConstraint, func, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker, relationship
engine = create_engine('sqlite:///resources/purchases')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Bon(Base):
    __tablename__ = 'bons'

    purchaseId = Column(Integer, primary_key=True, nullable=False)
    total = Column(Float)
    shop = Column(String)
    buyer = Column(String)
    date = Column(Date)

    def __repr__(self):
        return "<Bon(total='{}', shop='{}', buyer='{}', date='{}')>".format(
            self.total, self.shop, self.buyer, self.date)


class Product(Base):
    __tablename__ = 'products'

    productId = Column(Integer, primary_key=True, nullable=False)
    productName = Column(String)
    price = Column(Float)
    shop = Column(String)

    def __repr__(self):
        return "<Product(productId='{}', name='{}', price='{}', shop='{}')>".format(
            self.productId, self.productName, self.price, self.shop)


class Item(Base):
    __tablename__ = 'items'

    purchaseId = Column(Integer, ForeignKey(Bon.purchaseId), primary_key=True)
    itemId = Column(Integer, ForeignKey(Product.productId), primary_key=True)
    price = Column(Float)
    amount = Column(Integer)

    bon = relationship("Bon", back_populates="items")
    product = relationship("Product", back_populates="items")

    def __repr__(self):
        return "<Item(purchaseId='{}', itemId='{}', price='{}', amount='{}')>".format(
            self.purchaseId, self.itemId, self.price, self.amount)


Bon.items = relationship("Item", order_by=Item.itemId, back_populates="bon")
Product.items = relationship(
    "Item", order_by=Item.purchaseId, back_populates="product")


def insertBon(total, shop, buyer, date=None):
    """[summary]

    Arguments:
        total {float} -- [description]
        shop {str} -- [description]
        buyer {str} -- [description]

    Keyword Arguments:
        date {str} -- [description] (default: {None})

    Returns:
        int -- purchaseId
    """
    if date is None or date == "":
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    b = Bon(total=total, shop=shop, buyer=buyer,
            date=datetime.date.fromisoformat(date))
    session = Session()
    session.add(b)
    session.commit()
    return b.purchaseId


def insertItem(purchaseId, productName, price, amount):
    """[summary]

    Arguments:
        purchaseId {int} -- [description]
        productName {str} -- [description]
        price {float} -- [description]
        amount {int} -- [description]
    """
    session = Session()
    shop = session.query(Bon.shop).filter(
        Bon.purchaseId == purchaseId).scalar()
    price = round(price, 2)
    if amount == None:
        amount = 1
    try:
        p = session.query(Product).filter(
            Product.productName == productName, Product.shop == shop).scalar()
        productId, oldPrice = p.productId, p.price
        if price != oldPrice:
            p.price = price
            session.commit()
            session = Session()

    except AttributeError as e:
        p = Product(price=price, productName=productName, shop=shop)
        session.add(p)
        session.commit()
        productId = p.productId
        session = Session()
    item = Item(purchaseId=purchaseId, itemId=productId,
                price=price, amount=amount)
    session.add(item)
    session.commit()

    session = Session()
    return item


def getBonList():
    session = Session()
    bons = session.query(Bon).order_by(Bon.date.desc()).all()

    return bons


def getProductList():
    session = Session()
    products = session.query(Product).all()
    # TODO make this more elegant and efficient, maybe with fancy query?
    mergeDict = {}
    for p in products:
        total = sum([x.price*x.amount for x in p.items])
        amt = sum([x.amount for x in p.items])
        if p.productName in mergeDict:
            mergeDict[p.productName]['amount'] = mergeDict[p.productName]['amount'] + amt
            mergeDict[p.productName]['total'] = mergeDict[p.productName]['total'] + total
        else:
            mergeDict[p.productName] = {'amount': amt, 'total': total}
    products = [(key, mergeDict[key]['total'], mergeDict[key]['amount'])
                for key in mergeDict]

    return sorted(products, key=lambda x: x[1], reverse=True)


def getItems(purchaseId):
    session = Session()
    items = session.query(Item).filter(Item.purchaseId == purchaseId).all()

    return items


def getProduct(productName):
    session = Session()
    product = session.query(Product).filter(
        Product.productName == productName).all()
    products = []
    for p in product:
        pDict = p.__dict__

        pDict['avg'] = statistics.mean(
            [price for i in p.items for price in [i.price]*i.amount])
        pDict['total'] = sum([i.price*i.amount for i in p.items])
        products.append(pDict)

    return products


def getBon(purchaseId):
    session = Session()
    bon = session.query(Bon).filter(Bon.purchaseId == purchaseId).one()

    return bon


def delItem(purchaseId, itemId):
    session = Session()
    item = session.query(Item).filter(
        Item.purchaseId == purchaseId, Item.itemId == itemId).one()
    retItem = item.__dict__
    session.delete(item)
    session.commit()
    return retItem


def delBon(purchaseId):
    session = Session()
    bon = session.query(Bon).filter(Bon.purchaseId == purchaseId).one()
    retBon = bon.__dict__
    for i in bon.items:
        session.delete(i)
    session.delete(bon)
    session.commit()
    return retBon


def getAutocompleteShops():
    session = Session()
    shops = list(set(session.query(Bon.shop).all()))
    shops.sort()

    return [s[0] for s in shops]


def getAutocompleteItems(shop):
    # TODO make efficient pl0x
    session = Session()
    productsWithPrice = session.query(
        Product.productName, Product.price).filter(Product.shop == shop).all()
    productsWithoutPrice = session.query(
        Product.productName).filter(Product.shop != shop).all()
    pwp = (p[0] for p in productsWithPrice)
    pwop = set((p[0] for p in productsWithoutPrice)).difference(pwp)
    for p in pwop:
        productsWithPrice.append((p, None))
    productsWithPrice.sort(key=lambda x: str(x[0]))

    return [{'productName': p[0], 'price':p[1]} for p in productsWithPrice]


def getAbrechnung(dateBegin, dateEnd):

    session = Session()
    bons = session.query(Bon).filter(
        Bon.date.between(dateBegin, dateEnd)).all()
    paidPerPerson = dict([(u, 0) for u in users])
    excludedPerPerson = dict([(u, 0) for u in users])

    for b in bons:
        excluded = 0
        for i in b.items:
            if i.product.productName in blacklist:
                excluded += i.price * i.amount
        excludedPerPerson[b.buyer] += excluded
        paidPerPerson[b.buyer] += b.total - excluded

    returnList = []
    sharePerPerson = sum(paidPerPerson.values())/len(users)

    for person, paid in paidPerPerson.items():
        returnList.append({
            'person': person,
            'paid': round(paid, 2),
            'diff': round(sharePerPerson-paid, 2),
            'excl': round(excludedPerPerson[person],  2)
        })

    return returnList


if __name__ == "__main__":
    print(getAbrechnung("2020-04-01", "2020-06-01"))
