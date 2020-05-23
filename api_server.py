from flask import Flask
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse
from flask_cors import CORS
import db

app = Flask(__name__)
api = Api(app)


fields_product_gist = {
    "productName": fields.String,
    "price": fields.Float
}
fields_item = {
    "price": fields.Float,
    "amount": fields.Integer,
    "product": fields.Nested(fields_product_gist),
    "itemId": fields.Integer
}
fields_item_gist = {
    "price": fields.Float,
    "amount": fields.Integer,
    "purchaseId": fields.Integer
}
fields_bon = {
    'purchaseId': fields.Integer,
    'buyer': fields.String,
    'shop': fields.String,
    'total': fields.Float,
    'date': fields.String,
    'items': fields.List(fields.Nested(fields_item))
}
fields_bon_gist = {
    'purchaseId': fields.Integer,
    'buyer': fields.String,
    'shop': fields.String,
    'total': fields.Float,
    'date': fields.String
}

fields_product = {
    "productId": fields.Integer,
    'shop': fields.String,
    'price': fields.Float,
    'productName': fields.String,
    'avg': fields.Float,
    'total': fields.Float,
    'items': fields.List(fields.Nested(fields_item_gist))
}

bon_parser = reqparse.RequestParser()
bon_parser.add_argument("buyer", required=True)
bon_parser.add_argument("shop", required=True)
bon_parser.add_argument("total", type=float, required=True)
bon_parser.add_argument("date", default=None)

item_parser = reqparse.RequestParser()
item_parser.add_argument("productName", required=True)
item_parser.add_argument("amount", type=int, default=None)
item_parser.add_argument("price", type=float, required=True)


class BonList(Resource):
    @marshal_with(fields_bon_gist)
    def get(self):
        bons = db.getBonList()
        return bons


class ProductList(Resource):
    def get(self):
        products = db.getProductList()
        return products


class Bon(Resource):
    @marshal_with(fields_bon)
    def get(self, purchaseId):
        b = db.getBon(purchaseId)
        return b

    @marshal_with(fields_item)
    def post(self, purchaseId):
        
        args = item_parser.parse_args()
        item = db.insertItem(purchaseId, args['productName'],
                      args['price'], args['amount'])
        return item, 201
    @marshal_with(fields_bon)
    def delete(self, purchaseId):
        bon = db.delBon(purchaseId)
        return bon, 200


class NewBon(Resource):
    def post(self):
        args = bon_parser.parse_args()
        print(args)
        purchaseId = db.insertBon(
            args['total'], args['shop'], args['buyer'], args['date'])
        return {"purchaseId": purchaseId}


class Item(Resource):
    @marshal_with(fields_item)
    def delete(self, purchaseId, itemId):
        item = db.delItem(purchaseId, itemId)
        return item, 200


class Product(Resource):
    @marshal_with(fields_product)
    def get(self, productName):
        p = db.getProduct(productName)
        return p

class AutocompleteShops(Resource):
    def get(self):
        s = db.getAutocompleteShops()
        return s

class AutocompleteItems(Resource):
    def get(self, shop):
        i = db.getAutocompleteItems(shop)
        return i


def init():
    api.add_resource(BonList, "/api/bons")
    api.add_resource(ProductList, "/api/products")
    api.add_resource(Bon, "/api/bon/<int:purchaseId>")
    api.add_resource(NewBon, "/api/bon")
    api.add_resource(Item, "/api/bon/<int:purchaseId>/item/<int:itemId>")
    api.add_resource(Product, "/api/products/<productName>")
    api.add_resource(AutocompleteShops, "/api/auto/shops")
    api.add_resource(AutocompleteItems, "/api/auto/items/<shop>")
    

if __name__ == "__main__":
    CORS(app)
    init()
    app.run(host="0.0.0.0", debug=True)
