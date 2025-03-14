from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash, send_from_directory
from flask_wtf import FlaskForm
from bson import ObjectId
from datetime import datetime
import random
import string
import os
import json
from werkzeug.utils import secure_filename
from pymongo import MongoClient 
import os.path

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# MongoDB Configuration with enhanced error handling
try:
    client = MongoClient('mongodb://localhost:27017/', 
                        serverSelectionTimeoutMS=5000,
                        connectTimeoutMS=5000,
                        socketTimeoutMS=5000)
    print("Attempting to connect to MongoDB...")
    # Test connection with timeout
    client.admin.command('ping')
    print("MongoDB connection successful")
    db = client['IMS']
    
    # Verify collections exist
    sales_collection = db.sales
    test_doc = sales_collection.find_one()
    if test_doc:
        print(f"Successfully accessed sales collection. Found {sales_collection.count_documents({})} documents")
    
    inventory_collection = db.inventory
    customers_collection = db.customers
    purchase_history_collection = db.purchase_history
except Exception as e:
    print(f"MongoDB Connection Error: {e}")
    print("Error details:", str(e))
    # Mock collections for error handling
    class MockCollection:
        def __init__(self): 
            self.docs = []
            print("Using mock collection due to MongoDB connection failure")
        def find(self, *args, **kwargs): 
            cursor = type('Cursor', (), {'sort': lambda *a, **k: []})
            return cursor
        def find_one(self, *args, **kwargs): return None if not self.docs else self.docs[0]
        def insert_one(self, doc): self.docs.append(doc)
        def update_one(self, *args, **kwargs): pass
        def delete_one(self, *args, **kwargs): pass
        def count_documents(self, *args, **kwargs): return len(self.docs)
    
    inventory_collection = MockCollection()
    customers_collection = MockCollection()
    sales_collection = MockCollection()
    purchase_history_collection = MockCollection()

# File upload configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Context processor for template variables
@app.context_processor
def utility_processor():
    return {
        'now': datetime.now()
    }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file):
    file.seek(0, 2)  # Seek to end of file
    size = file.tell()
    file.seek(0)  # Reset file pointer
    return size <= MAX_FILE_SIZE

def generate_reference_number():
    """Generate a unique reference number for sales"""
    while True:
        prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
        timestamp = datetime.now().strftime('%Y%m%d')
        suffix = ''.join(random.choices(string.digits, k=4))
        ref_num = f"{prefix}{timestamp}{suffix}"
        # Check if reference number already exists
        if not sales_collection.find_one({'reference_no': ref_num}):
            return ref_num

def get_next_receipt_number():
    """Get the next available receipt number from the database"""
    try:
        last_sale = sales_collection.find_one(sort=[("receipt_number", -1)])
        if last_sale and 'receipt_number' in last_sale:
            try:
                return int(last_sale['receipt_number']) + 1
            except (ValueError, TypeError):
                return 1000
        return 1000
    except Exception as e:
        print(f"Error getting receipt number: {e}")
        return 1000

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(413)
def too_large(error):
    return 'File is too large', 413

# Basic routes
@app.route('/')
@app.route('/inventory')
def inventory_page():
    try:
        inventory = list(inventory_collection.find())
        return render_template('inventory.html', inventory=inventory, active='inventory')
    except Exception as e:
        flash(f'Error loading inventory: {str(e)}')
        return render_template('inventory.html', inventory=[], active='inventory')

@app.route('/products')
def products():
    try:
        inventory = list(inventory_collection.find())
        return render_template('products.html', inventory=inventory, active='products')
    except Exception as e:
        flash(f'Error loading products: {str(e)}')
        return render_template('products.html', inventory=[], active='products')

@app.route('/product/<product_id>')
def product_detail(product_id):
    try:
        product = inventory_collection.find_one({'_id': ObjectId(product_id)})
        if not product:
            flash('Product not found')
            return redirect(url_for('products'))
        customers = list(customers_collection.find())
        return render_template('product_detail.html', product=product, customers=customers)
    except Exception as e:
        flash(f'Error loading product details: {str(e)}')
        return redirect(url_for('products'))

@app.route('/customers')
def customers_page():
    try:
        customers = list(customers_collection.find())
        return render_template('customers.html', customers=customers, active='customers')
    except Exception as e:
        flash(f'Error loading customers: {str(e)}')
        return render_template('customers.html', customers=[], active='customers')

@app.route('/customer/<customer_id>/history')
def customer_history(customer_id):
    try:
        customer = customers_collection.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            flash('Customer not found')
            return redirect(url_for('customers_page'))
        purchases = list(purchase_history_collection.find({'customer_id': ObjectId(customer_id)}))
        total_purchases = len(purchases)
        total_spent = sum(p.get('total', 0) for p in purchases)
        last_purchase = max((p.get('date') for p in purchases), default=None)
        last_purchase_date = last_purchase.strftime('%b %d, %Y') if last_purchase else 'No purchases'
        
        return render_template('customer_history.html', 
                             customer=customer,
                             purchases=purchases,
                             total_purchases=total_purchases,
                             total_spent=total_spent,
                             last_purchase_date=last_purchase_date,
                             active='customers')
    except Exception as e:
        flash(f'Error loading customer history: {str(e)}')
        return redirect(url_for('customers_page'))

@app.route('/get_next_receipt_number')
def get_next_receipt_number_route():
    return jsonify({'receipt_number': get_next_receipt_number()})

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    form = FlaskForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            customer_data = request.form.to_dict()
            required_fields = ['company', 'email', 'phone']
            if not all(customer_data.get(field) for field in required_fields):
                flash('Company name, email, and phone number are required.')
                return render_template('add_customer.html', active='customers', form=form)
                
            customer_data['purchases'] = []
            customer_data['created_at'] = datetime.now()
            
            result = customers_collection.insert_one(customer_data)
            if result.inserted_id:
                flash('Customer added successfully!')
                return redirect(url_for('customers_page'))
            else:
                flash('Error adding customer.')
                return render_template('add_customer.html', active='customers', form=form)
        except Exception as e:
            flash(f'An error occurred while adding the customer: {str(e)}')
            return render_template('add_customer.html', active='customers', form=form)
            
    return render_template('add_customer.html', active='customers', form=form)

@app.route('/edit_customer/<customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    form = FlaskForm()
    try:
        customer = customers_collection.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            flash('Customer not found')
            return redirect(url_for('customers_page'))

        if request.method == 'POST' and form.validate_on_submit():
            updated_data = request.form.to_dict()
            
            # Handle numeric fields
            if 'credit_limit' in updated_data:
                try:
                    updated_data['credit_limit'] = float(updated_data['credit_limit'])
                except ValueError:
                    updated_data['credit_limit'] = 0.0

            # Validate required fields
            required_fields = ['company', 'email', 'phone']
            if not all(updated_data.get(field) for field in required_fields):
                flash('Company name, email, and phone number are required.')
                return render_template('edit_customer.html', customer=customer, form=form)

            result = customers_collection.update_one(
                {'_id': ObjectId(customer_id)},
                {'$set': updated_data}
            )

            if result.modified_count > 0:
                flash('Customer updated successfully!')
                return redirect(url_for('customers_page'))
            else:
                flash('No changes were made to the customer.')

        return render_template('edit_customer.html', customer=customer, form=form)
        
    except Exception as e:
        flash(f'Error updating customer: {str(e)}')
        return redirect(url_for('customers_page'))

@app.route('/delete_customer/<customer_id>')
def delete_customer(customer_id):
    try:
        customer = customers_collection.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            flash('Customer not found')
            return redirect(url_for('customers_page'))
        
        # Check if customer has any purchase history
        if purchase_history_collection.count_documents({'customer_id': ObjectId(customer_id)}) > 0:
            flash('Cannot delete customer with purchase history.')
            return redirect(url_for('customers_page'))
        
        result = customers_collection.delete_one({'_id': ObjectId(customer_id)})
        if result.deleted_count > 0:
            flash('Customer deleted successfully!')
        else:
            flash('Failed to delete customer.')
            
    except Exception as e:
        flash(f'Error deleting customer: {str(e)}')
        
    return redirect(url_for('customers_page'))

@app.route('/edit_inventory/<item_id>', methods=['GET', 'POST'])
def edit_inventory(item_id):
    form = FlaskForm()
    try:
        product = inventory_collection.find_one({'_id': ObjectId(item_id)})
        if not product:
            flash('Product not found')
            return redirect(url_for('inventory_page'))

        if request.method == 'POST' and form.validate_on_submit():
            updated_data = request.form.to_dict()
            
            # Handle numeric fields
            numeric_fields = {
                'stock': int,
                'min_stock': int,
                'price': float,
                'landing_cost': float
            }
            
            for field, convert in numeric_fields.items():
                if field in updated_data:
                    try:
                        updated_data[field] = convert(updated_data[field])
                    except ValueError:
                        updated_data[field] = 0

            # Store cost field from landing_cost
            if 'landing_cost' in updated_data:
                updated_data['cost'] = updated_data.pop('landing_cost')

            # Handle file upload
            if 'productImage' in request.files:
                file = request.files['productImage']
                if file and file.filename != '':
                    if not allowed_file(file.filename):
                        flash('Invalid file type. Only PNG, JPG, and JPEG are allowed.')
                        return render_template('edit_inventory.html', product=product, form=form)
                    
                    if not validate_file_size(file):
                        flash('File size exceeds maximum limit of 5MB.')
                        return render_template('edit_inventory.html', product=product, form=form)
                    
                    # Generate unique filename
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    
                    # Save new file
                    file.save(file_path)
                    updated_data['photo'] = filename
                    
                    # Delete old file if it exists and is not the default
                    if product.get('photo') and product['photo'] != 'product1.jpg':
                        old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], product['photo'])
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)

            # Update document
            result = inventory_collection.update_one(
                {'_id': ObjectId(item_id)},
                {'$set': updated_data}
            )

            if result.modified_count > 0:
                flash('Product updated successfully!')
                return redirect(url_for('inventory_page'))
            else:
                flash('No changes were made to the product.')

        return render_template('edit_inventory.html', product=product, form=form)
        
    except Exception as e:
        flash(f'Error updating product: {str(e)}')
        return redirect(url_for('inventory_page'))

@app.route('/delete_inventory/<item_id>')
def delete_inventory(item_id):
    try:
        product = inventory_collection.find_one({'_id': ObjectId(item_id)})
        if not product:
            flash('Product not found')
            return redirect(url_for('inventory_page'))
        
        # Delete product image if it exists and is not the default
        if product.get('photo') and product['photo'] != 'product1.jpg':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], product['photo'])
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete product from database
        result = inventory_collection.delete_one({'_id': ObjectId(item_id)})
        
        if result.deleted_count > 0:
            flash('Product deleted successfully!')
        else:
            flash('Failed to delete product.')
            
    except Exception as e:
        flash(f'Error deleting product: {str(e)}')
        
    return redirect(url_for('inventory_page'))

@app.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    form = FlaskForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            inventory_data = request.form.to_dict()
            
            # Handle numeric fields
            numeric_fields = {
                'stock': int,
                'min_stock': int,
                'price': float,
                'landing_cost': float
            }
            
            for field, convert in numeric_fields.items():
                if field in inventory_data:
                    try:
                        inventory_data[field] = convert(inventory_data[field])
                    except ValueError:
                        inventory_data[field] = 0

            # Store cost field from landing_cost
            if 'landing_cost' in inventory_data:
                inventory_data['cost'] = inventory_data.pop('landing_cost')

            # Handle file upload
            if 'productImage' in request.files:
                file = request.files['productImage']
                if file and file.filename != '':
                    if not allowed_file(file.filename):
                        flash('Invalid file type. Only PNG, JPG, and JPEG are allowed.')
                        return render_template('add_inventory.html', form=form)

                    if not validate_file_size(file):
                        flash('File size exceeds maximum limit of 5MB.')
                        return render_template('add_inventory.html', form=form)

                    filename = secure_filename(file.filename)
                    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    inventory_data['photo'] = filename
                else:
                    inventory_data['photo'] = 'product1.jpg'
            else:
                inventory_data['photo'] = 'product1.jpg'
            
            result = inventory_collection.insert_one(inventory_data)
            if result.inserted_id:
                flash('Product added successfully!')
                return redirect(url_for('inventory_page'))
            else:
                flash('Failed to add product.')
                
        except Exception as e:
            flash(f'Error adding product: {str(e)}')

    return render_template('add_inventory.html', form=form)

@app.route('/sales', methods=['GET', 'POST'])
def sales_page():
    if request.method == 'POST':
        try:
            sale_data = request.json
            if not sale_data:
                return jsonify({'error': 'No data provided'}), 400

            # Validate required fields
            required_fields = ['customer', 'items']
            if not all(field in sale_data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Get customer details
            customer = customers_collection.find_one({'company': sale_data['customer']})
            if not customer:
                return jsonify({'error': 'Invalid customer'}), 400

            # Validate and process items
            for item in sale_data['items']:
                product = inventory_collection.find_one({'name': item['product']})
                if not product:
                    return jsonify({'error': f'Product not found: {item["product"]}'}), 400
                if product['stock'] < item['quantity']:
                    return jsonify({'error': f'Insufficient stock for {item["product"]}'}), 400
                
                # Update inventory stock
                inventory_collection.update_one(
                    {'_id': product['_id']},
                    {'$inc': {'stock': -item['quantity']}}
                )

            # Add additional sale details
            sale_data['receipt_number'] = get_next_receipt_number()
            sale_data['reference_no'] = generate_reference_number()
            sale_data['created_at'] = datetime.now()
            sale_data['customer_id'] = str(customer['_id'])
            sale_data['status'] = 'paid' if float(sale_data.get('delivered', 0)) >= float(sale_data['total']) else 'pending'

            # Save the sale
            result = sales_collection.insert_one(sale_data)
            if not result.inserted_id:
                return jsonify({'error': 'Failed to save sale'}), 500

            # Create purchase history
            purchase_history_collection.insert_one({
                'customer_id': ObjectId(customer['_id']),
                'sale_id': result.inserted_id,
                'date': datetime.now(),
                'items': sale_data['items'],
                'total': sale_data['total'],
                'reference_no': sale_data['reference_no'],
                'status': sale_data['status']
            })

            return jsonify({
                'success': True,
                'message': 'Sale recorded successfully',
                'reference': sale_data['reference_no']
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # GET request - render sales form
    try:
        customers = list(customers_collection.find())
        inventory = list(inventory_collection.find())
        for customer in customers:
            customer['_id'] = str(customer['_id'])
        return render_template('sales.html',
                            active='sales',
                            customers=customers,
                            inventory=inventory,
                            receipt_number=get_next_receipt_number())
    except Exception as e:
        flash(f'Error loading sales page: {str(e)}')
        return render_template('sales.html', active='sales')

@app.route('/sales/history')
def sales_history():
    try:
        formatted_sales = []
        sales = list(sales_collection.find().sort('created_at', -1))
        
        for sale in sales:
            try:
                # Format the sale data with proper error handling
                formatted_sale = {
                    'receipt_number': sale.get('receipt_number', ''),
                    'receipt_date': sale.get('receipt_date', datetime.now().strftime('%Y-%m-%d')),
                    'customer': sale.get('customer', ''),
                    'items': sale.get('items', []),  # Include items
                    'total': "{:.2f}".format(float(sale.get('total', 0))),
                    'delivered': "{:.2f}".format(float(sale.get('delivered', 0))),
                    'deposited': "{:.2f}".format(float(sale.get('deposited', 0))),
                    'status': sale.get('status', 'pending'),
                    'reference_no': sale.get('reference_no', '')
                }
                formatted_sales.append(formatted_sale)
            except Exception as format_err:
                print(f"Error formatting sale {sale.get('_id')}: {str(format_err)}")
                continue
        
        return render_template('sales_storage.html', sales=formatted_sales, active='sales')
    except Exception as e:
        print(f"Error in sales_history: {str(e)}")
        flash(f'Error loading sales: {str(e)}')
        return render_template('sales_storage.html', sales=[], active='sales')

@app.route('/sales/<sale_id>')
def sale_details(sale_id):
    try:
        sale = sales_collection.find_one({'_id': ObjectId(sale_id)})
        if not sale:
            return jsonify({'error': 'Sale not found'}), 404
            
        sale['_id'] = str(sale['_id'])
        return jsonify(sale)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sales/print/<reference_no>')
def print_receipt(reference_no):
    try:
        # Find sale by reference number instead of ID
        sale = sales_collection.find_one({'reference_no': reference_no})
        if not sale:
            flash('Sale not found')
            return redirect(url_for('sales_history'))
        
        # Format date if it exists
        if 'receipt_date' in sale:
            sale['formatted_date'] = datetime.strptime(sale['receipt_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        else:
            sale['formatted_date'] = datetime.now().strftime('%B %d, %Y')
        
        return render_template('print_receipt.html',
                             sale=sale,
                             subtotal=f"${sale.get('subtotal', 0):.2f}",
                             discount=f"${sale.get('discount', 0):.2f}",
                             total=f"${sale.get('total', 0):.2f}",
                             delivered=f"${sale.get('delivered', 0):.2f}",
                             deposited=f"${sale.get('deposited', 0):.2f}")
    except Exception as e:
        print(f"Error generating receipt: {str(e)}")
        flash(f'Error generating receipt: {str(e)}')
        return redirect(url_for('sales_history'))

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
            'phone': '123-456-7890',
            'type': 'Wholesale',
            'purchases': []
        })

    try:
        app.run(debug=True, use_reloader=True, threaded=True)
    except OSError as e:
        if e.winerror == 10038:  # Socket error
            print("Restarting server due to socket error...")
            import time
            time.sleep(1)  # Wait a second before restarting
            app.run(debug=True, use_reloader=True, threaded=True)
        else:
            raise