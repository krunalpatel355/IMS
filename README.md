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
- Flask 2.3.3
- Flask-WTF 1.1.1
- Python-dotenv 1.0.0
- MongoDB support (via pymongo 4.5.0)
- Gunicorn 21.2.0 for production deployment
- HTML/CSS
- JavaScript

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

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

4. Create a .env file in the project root:
```
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

5. Run the application:
```bash
# Development
python main.py

# Production
gunicorn main:app
```

The application will be available at `http://localhost:5000` (development) or `http://localhost:8000` (production)

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

The application uses environment variables for configuration:
- `FLASK_APP`: Specifies the main application file
- `FLASK_ENV`: Set to 'development' or 'production'
- `SECRET_KEY`: Used for session management and CSRF protection
- `MONGO_URI`: (Optional) MongoDB connection string if using MongoDB

## Development Notes

The application currently uses in-memory data structures but is prepared for MongoDB integration:
- Collections are defined for: Inventory, Customers, Sales, and History
- MongoDB connection strings can be configured via environment variables
- Commented code includes MongoDB integration patterns

For production deployment:
1. Set up a MongoDB database
2. Configure proper environment variables
3. Use a strong SECRET_KEY
4. Deploy behind a reverse proxy (nginx recommended)
5. Enable HTTPS
6. Set up proper logging

## Security Features

- CSRF protection via Flask-WTF
- Secure session management
- Input validation and sanitization
- File upload restrictions
- Unique ID generation for receipts and references

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.