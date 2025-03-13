# Inventory Management System (IMS)

A Flask-based Inventory Management System for tracking products, customers, and sales.

## Features

- Product Inventory Management
- Customer Management
- Sales Tracking
- Product Details and Search
- Interactive Dashboard
- Sales Receipt Generation

## Technology Stack

- Python 3.x
- Flask
- MongoDB
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
├── main.py              # Main application file
├── static/              # Static files (CSS, JS, images)
│   └── style.css       
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── inventory.html  # Inventory management
│   ├── products.html   # Product details
│   ├── customers.html  # Customer management
│   └── sales.html      # Sales management
└── requirements.txt    # Project dependencies
```

## Environment Variables

Create a `.env` file in the root directory and add:

```
FLASK_APP=main.py
FLASK_ENV=development
MONGO_URI=your_mongodb_connection_string
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request