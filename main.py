from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash, send_from_directory
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from bson import ObjectId
from datetime import datetime
import random
import string
import os
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os.path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
csrf = CSRFProtect(app)

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['IMS']

# Collections
inventory_collection = db.inventory
customers_collection = db.customers
sales_collection = db.sales
purchase_history_collection = db.purchase_history

# File upload configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_reference_number():
    """Generate a unique reference number for sales"""
    prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
    timestamp = datetime.now().strftime('%Y%m%d')
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{timestamp}{suffix}"

@app.route('/')
@app.route('/inventory')
def inventory_page():
    inventory = list(inventory_collection.find())
    return render_template('inventory.html', inventory=inventory, active='inventory')

@app.route('/products')
def products():
    inventory = list(inventory_collection.find())
    return render_template('products.html', inventory=inventory, active='products')

@app.route('/customers')
def customers_page():
    customers = list(customers_collection.find())
    return render_template('customers.html', customers=customers, active='customers')

@app.route('/customer/<customer_id>/history')
def customer_history(customer_id):
    customer = customers_collection.find_one({'_id': ObjectId(customer_id)})
    if not customer:
        return redirect(url_for('customers_page'))
    
    # Get customer's purchase history
    customer_purchases = list(purchase_history_collection.find({'customer_id': ObjectId(customer_id)}))
    
    # Calculate statistics
    total_purchases = len(customer_purchases)
    total_spent = sum(p['total'] for p in customer_purchases)
    last_purchase_date = max(p['date'] for p in customer_purchases).strftime('%b %d, %Y') if customer_purchases else 'No purchases'
    
    return render_template('customer_history.html', 
                         customer=customer,
                         purchases=customer_purchases,
                         total_purchases=total_purchases,
                         total_spent=total_spent,
                         last_purchase_date=last_purchase_date,
                         active='customers')

@app.route('/get_next_receipt_number')
def get_next_receipt_number():
    global current_receipt_number
    current_receipt_number += 1
    return jsonify({'receipt_number': current_receipt_number})

@app.route('/sales', methods=['GET', 'POST'])
def sales_page():
    global current_receipt_number
    if request.method == 'POST':
        if request.is_json:
            sale_data = request.get_json()
            
            # Generate a unique reference if one isn't provided
            if not sale_data.get('reference_no'):
                sale_data['reference_no'] = generate_reference_number()
            
            # Format the sale data for storage
            formatted_sale = {
                'receipt_number': sale_data.get('receipt_number'),
                'customer': sale_data.get('customer'),
                'email': sale_data.get('email'),
                'receipt_date': sale_data.get('receipt_date'),
                'payment_method': sale_data.get('payment_method'),
                'reference_no': sale_data.get('reference_no'),
                'deposit_to': sale_data.get('deposit_to'),
                'subtotal': float(sale_data.get('subtotal', 0)),
                'discount': float(sale_data.get('discount', 0)),
                'total': float(sale_data.get('total', 0)),
                'delivered': float(sale_data.get('delivered', 0)),
                'deposited': float(sale_data.get('deposited', 0)),
                'items': sale_data.get('items', []),
                'created_at': datetime.now(),
                'status': 'paid' if float(sale_data.get('delivered', 0)) >= float(sale_data.get('total', 0)) else 'pending'
            }
            
            # Insert into MongoDB
            sales_collection.insert_one(formatted_sale)
            
            return jsonify({
                'status': 'success',
                'message': 'Sale recorded successfully',
                'reference': formatted_sale['reference_no']
            })
            
    current_receipt_number += 1
    return render_template('sales.html', active='sales', receipt_number=current_receipt_number)

@app.route('/sales_storage', methods=['GET', 'POST'])
def sales_storage():
    sales = list(sales_collection.find())
    return render_template('sales_storage.html', active='sales', sales=sales)

@app.route('/product/<product_id>')
def product_detail(product_id):
    product = inventory_collection.find_one({'_id': ObjectId(product_id)})
    customers = list(customers_collection.find())
    return render_template('product_detail.html', product=product, customers=customers)

@app.route('/edit_inventory/<item_id>', methods=['GET', 'POST'])
def edit_inventory(item_id):
    if request.method == 'GET':
        item = inventory_collection.find_one({'_id': ObjectId(item_id)})
        return render_template('edit_inventory.html', item=item)
    
    elif request.method == 'POST':
        inventory_collection.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': request.form.to_dict()}
        )
        return redirect(url_for('inventory_page'))

@app.route('/delete_inventory/<item_id>')
def delete_inventory(item_id):
    inventory_collection.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('inventory_page'))

@app.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    form = FlaskForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                inventory_data = request.form.to_dict()
                
                # Handle file upload
                if 'productImage' in request.files:
                    file = request.files['productImage']
                    if file and file.filename != '':
                        if allowed_file(file.filename):
                            # Create a unique filename
                            filename = secure_filename(file.filename)
                            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                            
                            # Ensure upload directory exists
                            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                            
                            # Save the file
                            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                            file.save(file_path)
                            print(f"Saved file to: {file_path}")
                            
                            # Store just the filename (no directory) in the database
                            inventory_data['photo'] = filename
                            print(f"Stored filename in DB: {inventory_data['photo']}")
                        else:
                            flash('Invalid file type. Only PNG, JPG, and JPEG are allowed.')
                            return render_template('add_inventory.html', active='inventory', form=form)
                    else:
                        inventory_data['photo'] = 'product1.jpg'  # Default image
                else:
                    inventory_data['photo'] = 'product1.jpg'  # Default image

                # Convert numeric fields
                numeric_fields = {
                    'stock': int,
                    'min_stock': int,
                    'price': float,
                    'landing_cost': float
                }
                
                for field, convert in numeric_fields.items():
                    if field in inventory_data and inventory_data[field]:
                        try:
                            inventory_data[field] = convert(inventory_data[field])
                        except ValueError:
                            inventory_data[field] = 0
                
                # Store cost field from landing_cost
                if 'landing_cost' in inventory_data:
                    inventory_data['cost'] = inventory_data['landing_cost']
                
                # Insert into MongoDB
                result = inventory_collection.insert_one(inventory_data)
                
                if result.inserted_id:
                    flash('Product added successfully!')
                    return redirect(url_for('inventory_page'))
                else:
                    flash('Failed to add inventory item.')
                    return render_template('add_inventory.html', active='inventory', form=form)
                    
            except Exception as e:
                print(f"Error adding inventory: {str(e)}")
                flash(f'An error occurred while adding the inventory item: {str(e)}')
                return render_template('add_inventory.html', active='inventory', form=form)
                
    return render_template('add_inventory.html', active='inventory', form=form)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        customer_data = request.form.to_dict()
        customer_data['purchases'] = []  # Initialize empty purchases list
        customers_collection.insert_one(customer_data)
        return redirect(url_for('customers_page'))
    return render_template('add_customer.html', active='customers')

if __name__ == '__main__':
    # Initialize collections with sample data if empty
    if inventory_collection.count_documents({}) == 0:
        inventory_collection.insert_one({
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
        })

    if customers_collection.count_documents({}) == 0:
        customers_collection.insert_one({
            'name': 'John Smith',
            'company': 'Tech Corp',
            'email': 'john@example.com',
            'number': '123-456-7890',
            'type': 'Wholesale',
            'purchases': []
        })

    app.run(debug=True)