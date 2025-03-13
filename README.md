# Inventory Management System (IMS)

A Flask-based Inventory Management System for tracking products, customers, and sales with receipt generation capabilities.

## Features

- Product Inventory Management
  - Add, edit, and delete inventory items
  - Track stock levels, prices, and product details
  - Product categorization and search
  - Detailed product information including brand, owner, part numbers
- Customer Management
  - Customer profiles with company information
  - Customer purchase history tracking
  - Customer type categorization (Wholesale, etc.)
- Sales Management
  - Generate unique receipt numbers
  - Multiple payment methods support
  - Track deposits and delivery status
  - Reference number generation
  - Sales history storage
- Additional Features
  - Interactive product detail views
  - Sales receipt generation
  - CSRF protection
  - Customer purchase statistics

## Technology Stack

- Python 3.x
- Flask 2.0.1
- Flask-WTF 1.0.0 (for CSRF protection)
- python-dotenv 0.19.0
- bson 0.5.10
- HTML/CSS
- JavaScript

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
project/
├── main.py                 # Main application file with routes and logic
├── static/                 # Static files (CSS, JS, images)
│   ├── style.css          # Main stylesheet
│   └── js/
│       └── checkout.js    # JavaScript for checkout functionality
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── inventory.html    # Inventory management
│   ├── products.html     # Product listing
│   ├── product_detail.html # Individual product view
│   ├── add_inventory.html # Add new inventory
│   ├── edit_inventory.html # Edit inventory items
│   ├── customers.html    # Customer management
│   ├── add_customer.html # Add new customer
│   ├── customer_history.html # Customer purchase history
│   ├── sales.html       # Sales management
│   └── sales_storage.html # Sales history
└── requirements.txt      # Project dependencies

## Configuration

The application uses the following configuration:
- Flask Secret Key (for session management and CSRF protection)
- Debug mode enabled for development

## Development Notes

Currently, the application uses in-memory data structures (Python lists) for storing:
- Inventory items
- Customer information
- Sales records
- Purchase history

For production use, it's recommended to:
1. Implement a proper database (the code includes commented MongoDB integration hints)
2. Set up proper environment variables
3. Configure a secure secret key

## Running in Development

The application runs in debug mode by default when started with:
```bash
python main.py
```

## Security Features

- CSRF protection enabled using Flask-WTF
- Secure receipt number generation
- Unique reference number generation for sales