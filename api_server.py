from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with, reqparse, abort
from db import getList, getItems, getBon, getProduct, insertBon, insertItem, delBon, delItem




fields_product_gist = {
    "productName": fields.String,
    "price": fields.Float
}
fields_item = {
    "price": fields.Float,
    "amount": fields.Integer,
    "product": fields.Nested(fields_product_gist)
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
    "productId" : fields.Integer,
    'shop': fields.String,
    'price': fields.Float,
    'name': fields.String,
    'items': fields.List(fields.Nested(fields_item_gist))
}

bon_parser = reqparse.RequestParser()
bon_parser.add_argument("buyer", required=True)
bon_parser.add_argument("shop", required=True)
bon_parser.add_argument("total", type=float, required=True)
bon_parser.add_argument("date", default=None)

item_parser = reqparse.RequestParser()
item_parser.add_argument("productName", required=True)
item_parser.add_argument("amount", type=int, required=True)
item_parser.add_argument("price", type=float, required=True)

class List(Resource):
    @marshal_with(fields_bon_gist)
    def get(self):
        bons = getList()
        return bons
    
class Bon(Resource):
    @marshal_with(fields_bon)
    def get(self, purchaseId):
        b = getBon(purchaseId)
        return b

    def post(self, purchaseId):
        args = item_parser.parse_args()
        insertItem(purchaseId, args['productName'], args['price'], args['amount'])
        return '', 201

    def delete(self, purchaseId):
        delBon(purchaseId)
        return '', 200

class NewBon(Resource):
    def post(self):
        args = bon_parser.parse_args()
        purchaseId = insertBon(args['total'], args['shop'], args['buyer'], args['date'])
        return {"purchaseId": purchaseId}

class Item(Resource):
    def delete(self, purchaseId, itemId):
        delItem(purchaseId, itemId)
        return '', 200

class Product(Resource):
    @marshal_with(fields_product)
    def get(self, productName):
        p = getProduct(productName)
        return p 



def init(app):
    api = Api(app)
    api.add_resource(List, "/api/list")
    api.add_resource(Bon, "/api/bon/<int:purchaseId>")
    api.add_resource(NewBon, "/api/bon")
    api.add_resource(Item, "/api/bon/<int:purchaseId>/item/<int:itemId>")
    api.add_resource(Product, "/api/product/<str:productName>")

if __name__ == "__main__":
    app = Flask(__name__)
    init(app)
    app.run(debug=True)