from flask import Flask, request, render_template, make_response, redirect, flash, url_for, jsonify
import datetime
from dateutil import relativedelta 
from saver import enterBonData as enterBon, enterItem, getList, getItems, deleteItem, getBon
from flask_wtf import FlaskForm 
from wtforms import TextField, DecimalField, IntegerField, SubmitField, RadioField, validators, ValidationError
from wtforms.fields.html5 import DateField
from stats import update, getAutocompleteList, getProductStats, getSingleProductStats, abrechnung, singleProductGraph
import json

pathToStatic="C:\\Users\\max\\Documents\\piStuff\\server\\static\\"
#pathToStatic="/home/pi/server/static/"
app = Flask(__name__)
app.secret_key = 'development key'

class BonForm(FlaskForm):
    buyer = RadioField('Buyer', choices=[('Max', 'Max'), ('Martha', 'Martha')], default='Max')
    shop = TextField("shop", [validators.required("Enter Shop")], id='shop',  render_kw={'autofocus': True})
    total = DecimalField("Total Price", [validators.required("Enter Price")])
    date = DateField('date', format='%Y-%m-%d')
    submit = SubmitField('Send')

class ItemForm(FlaskForm):
    productName = TextField("productName", [validators.required("Enter product name")], id='productName',  render_kw={'autofocus': True})
    price = DecimalField("Individual Price", [validators.required("Enter Price")])
    amount = IntegerField('amount', [validators.optional()])
    submit = SubmitField('Send')

class ReckoningForm(FlaskForm):
    start = DateField('Month', format='%Y-%m-%d')
    submit = SubmitField('Rechne Ab')
    #end = DateField('End Date', format='%Y-%m-%d')

@app.route('/')
def index():
    bons = getList()
    return render_template("index.html", bons=bons)


@app.route('/enterBon', methods=['GET', 'POST'])
def enterBonForm():
    form = BonForm()   

    if request.method == 'GET':
        return render_template("enterBon.html", form=form, shopList=getAutocompleteList('shop', 'bons'))

    else:
        if not form.validate_on_submit():
            flash('All fields are required.')
            print('rip')
            return redirect('/enterBon')

        buyer = form.buyer.data
        shop = form.shop.data
        total = float(form.total.data)

        date = form.date.data
        if date == '':
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        purchaseId = enterBon(total, shop, buyer, date)

        return redirect(url_for('enterItemForm',purchaseId = purchaseId[0]))

@app.route('/enterItem/<int:purchaseId>', methods=['GET', 'POST'])
def enterItemForm(purchaseId):
    form = ItemForm()
    if request.method == 'GET':
        items = getItems(purchaseId)
        productList = getAutocompleteList('productName', 'products')
        itemTotal = sum([x[1] * x[2] for x in items])
        return render_template("enterItem.html", items=items, form=form, purchaseId=purchaseId, productList=productList, itemTotal=itemTotal)
    else:
        if not form.validate_on_submit():
            flash('All fields are required.')
            return redirect(url_for('enterItemForm',purchaseId = purchaseId))
        productName = form.productName.data
        price = float(form.price.data)
        amount = form.amount.data
        
        if amount is None:
            amount = 1
        
        # TODO errorhandling
        enterItem(purchaseId, productName, price, amount)
        return redirect(url_for('enterItemForm',purchaseId = purchaseId))

@app.route('/enterItem/<int:purchaseId>/<int:itemId>', methods=['POST'])
def deleteItemForm(purchaseId, itemId):
    deleteItem(purchaseId, itemId)
    return redirect(url_for('enterItemForm',purchaseId = purchaseId))

@app.route('/stats')
def stats():
    with open(pathToStatic + "cornflakes.json", 'r') as f:
        cornflake_data = json.load(f) 
    with open(pathToStatic + "total.json", 'r') as f:
        total_data = json.load(f) 
    with open(pathToStatic + "month.json", 'r') as f:
        month_data = json.load(f) 
    with open(pathToStatic + "totaldist.json", 'r') as f:
        totaldist_data = json.load(f) 

    return render_template("stats.html", cornflake_data=cornflake_data, total_data=total_data, month_data=month_data, totaldist_data=totaldist_data)

@app.route('/updateStats')
def updateStats():
    update()
    return redirect(url_for('stats'))

@app.route('/products')
def productsIndex():
    products = getProductStats()
    return render_template("productsIndex.html", products=products)

@app.route('/products/<productName>')
def productDetails(productName):
    product = getSingleProductStats(productName)
    productgraph_data = singleProductGraph(productName)
    return render_template("productDetails.html", product=product, productName=productName, productgraph_data=productgraph_data)

@app.route('/bon/<int:purchaseId>')
def bonInfo(purchaseId):
    bon = getBon(purchaseId)
    items = getItems(purchaseId)
    return render_template("purchaseDetails.html", bon=bon, items=items)

@app.route('/reckoning', methods=['GET', 'POST'])
def reckoning():
    form = ReckoningForm()

    if(request.method=='GET'):
        return render_template("abrechnungIndex.html", form=form)
    else:
        if(form.start.data==None):
            print('whyy')
            return redirect(url_for('reckoning'))
        start = form.start.data
        end = start + relativedelta.relativedelta(months=1)

        start = start.strftime('%Y-%m-01')
        end = end.strftime('%Y-%m-01')
        print(start)
        print(end)
        reckon = abrechnung(start, end)
        return render_template('abrechnung.html',reckon=reckon)
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')