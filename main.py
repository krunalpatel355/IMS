from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId

app = Flask(__name__)

# Sample data - In production, use a proper database
inventory = [
    {
        'id': 1,
        'name': 'Widget A',
        'brand': 'BrandX',
        'stock': 100,
        'price': 29.99,
        'photo': 'product1.jpg',
        'owner': 'John Doe',
        'cost': 20.00,
        'rising': 'Yes',
        'application': 'Industrial',
        'part_number': 'WA-001',
        'description': 'High-quality industrial widget'
    }
]

customers = [
    {
        'id': 1,
        'name': 'John Smith',
        'email': 'john@example.com',
        'number': '123-456-7890',
        'purchases': ['Widget A']
    }
]

sales = []

@app.route('/')
@app.route('/inventory')
def inventory_page():
    return render_template('inventory.html', inventory=inventory, active='inventory')

@app.route('/products')
def products():
    return render_template('products.html', inventory=inventory, active='products')

@app.route('/customers')
def customers_page():
    return render_template('customers.html', customers=customers, active='customers')

@app.route('/sales')
def sales_page():
    return render_template('sales.html', sales=sales, active='sales')

@app.route('/product/<int:id>')
def product_detail(id):
    product = next((item for item in inventory if item['id'] == id), None)
    return render_template('product_detail.html', product=product, customers=customers)

@app.route('/edit_inventory/<item_id>', methods=['GET', 'POST'])
def edit_inventory(item_id):
    if request.method == 'GET':
        # Assuming you're using PyMongo, the code would be like:
        # item = mongo.db.inventory.find_one({'_id': ObjectId(item_id)})
        # For now, using the sample data:
        item = next((item for item in inventory if str(item['id']) == item_id), None)
        return render_template('edit_inventory.html', item=item)
    
    elif request.method == 'POST':
        # Here you would update the MongoDB document
        # mongo.db.inventory.update_one(
        #     {'_id': ObjectId(item_id)},
        #     {'$set': request.form.to_dict()}
        # )
        return redirect(url_for('inventory_page'))
    
@app.route('/delete_inventory/<item_id>')
def delete_inventory(item_id):
    # mongo.db.inventory.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('inventory_page'))

@app.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    return render_template('add_inventory.html', active='inventory')


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    return render_template('add_customer.html', active='customers')

@app.route('/sales_storage', methods=['GET', 'POST'])
def sales_storage():
    return render_template('sales_storage.html', active='sales')


if __name__ == '__main__':
    app.run(debug=True)