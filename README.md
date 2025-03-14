# Inventory Management System (IMS)

A modern Flask-based Inventory Management System with MongoDB integration, focused on product tracking, customer management, and sales processing.

## Core Features

### Inventory Management
- Add, edit, and delete products with detailed information
- Image upload support with validation (JPG, PNG up to 5MB)
- Real-time stock level tracking
- Advanced product search functionality
- Automated product ID generation
- Track costs, prices, and profit margins

### Customer Management
- Comprehensive customer profiles
- Company and contact information storage
- Purchase history tracking
- Customer type categorization
- Email validation and verification

### Sales Processing
- Generate unique receipt numbers automatically
- Multiple payment method support
- Deposit and delivery tracking
- Reference number generation
- Real-time sales history
- Automatic status updates (paid/pending)

### Security Features
- CSRF protection
- Secure file upload handling
- Input validation and sanitization
- MongoDB injection prevention
- Error handling and logging

## Technical Stack

### Backend
- Python 3.8+
- Flask 2.3.3
- MongoDB 4.x
- PyMongo 4.5.0

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Font Awesome Icons

### Security & Forms
- Flask-WTF 1.1.1
- Werkzeug 2.3.7
- Email validation

### Development & Deployment
- Python-dotenv 1.0.0
- Gunicorn 21.2.0
- DNSPython 2.4.2

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Unix/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   Create a .env file with:
   ```
   FLASK_APP=main.py
   FLASK_ENV=development
   SECRET_KEY=your-secure-secret-key
   MONGO_URI=mongodb://localhost:27017/
   ```

5. Initialize MongoDB:
   - Install MongoDB Community Edition
   - Start MongoDB service
   - Database will be auto-initialized on first run

6. Run the application:
   ```bash
   # Development
   python main.py

   # Production
   gunicorn main:app
   ```

## Project Structure

```
project/
├── main.py                 # Application entry point and route definitions
├── static/                 # Static assets
│   ├── style.css          # Global styles
│   ├── js/                # JavaScript modules
│   │   └── checkout.js    # Sales processing logic
│   └── uploads/           # Product images storage
├── templates/             # HTML templates
│   ├── base.html         # Base template with common elements
│   ├── inventory.html    # Product inventory management
│   ├── products.html     # Product catalog display
│   ├── customers.html    # Customer management
│   └── sales.html        # Sales processing interface
└── requirements.txt      # Project dependencies
```

## Configuration Options

### Application Settings
- `FLASK_ENV`: Set to 'development' or 'production'
- `SECRET_KEY`: Used for session security
- `MONGO_URI`: MongoDB connection string
- `UPLOAD_FOLDER`: Product image storage location
- `MAX_FILE_SIZE`: Maximum upload file size (5MB)
- `ALLOWED_EXTENSIONS`: Permitted file types (jpg, png, jpeg)

### Database Collections
- `inventory`: Product information
- `customers`: Customer records
- `sales`: Sales transactions
- `purchase_history`: Customer purchase records

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints where applicable
- Document functions and complex logic
- Handle exceptions appropriately

### Database Operations
- Use PyMongo's built-in security features
- Implement proper indexing for performance
- Validate data before insertion
- Handle MongoDB connection errors gracefully

### Security Practices
- Validate all user inputs
- Sanitize data before display
- Use CSRF tokens for forms
- Implement proper file upload validation
- Secure session management

## Production Deployment

1. Configure MongoDB:
   - Enable authentication
   - Set up proper indexes
   - Configure backup strategy

2. Server Setup:
   - Use Gunicorn with Nginx
   - Enable HTTPS
   - Configure proper logging
   - Set up monitoring

3. Environment:
   - Set FLASK_ENV to 'production'
   - Use strong SECRET_KEY
   - Configure proper MONGO_URI
   - Set up error logging

## Troubleshooting

Common issues and solutions:

1. MongoDB Connection:
   - Check MongoDB service status
   - Verify connection string
   - Ensure proper network access

2. File Uploads:
   - Verify upload directory permissions
   - Check file size limits
   - Validate file types

3. Performance Issues:
   - Monitor MongoDB queries
   - Check database indexes
   - Review application logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the coding standards
4. Write/update tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues and feature requests, please use the GitHub issue tracker.