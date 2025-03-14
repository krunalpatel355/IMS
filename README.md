# Project Bolt 🚀

[![Made with Flask](https://img.shields.io/badge/Made%20with-Flask-blue.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green.svg)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<div align="center">
  <h3>A Modern Inventory Management System</h3>
  <p>Streamline your business operations with our powerful and intuitive IMS solution.</p>
</div>

<br>

## ✨ Features

<table>
  <tr>
    <td>📦 <b>Inventory Management</b></td>
    <td>🛒 <b>Sales Processing</b></td>
    <td>👥 <b>Customer Management</b></td>
  </tr>
  <tr>
    <td>
      • Real-time stock tracking<br>
      • Low stock alerts<br>
      • Product categorization
    </td>
    <td>
      • Quick checkout process<br>
      • Digital receipts<br>
      • Payment tracking
    </td>
    <td>
      • Customer profiles<br>
      • Purchase history<br>
      • Contact management
    </td>
  </tr>
</table>

## 🛠️ Built With

- **Backend Framework**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **Additional Tools**:
  - Flask-WTF for form handling
  - BeautifulSoup for data parsing
  - Requests for HTTP operations

## 🛠️ Technical Stack

- **Backend**: 
  - Flask 2.0.1 with Flask-WTF for form handling
  - MongoDB 4.4+ for database
  - Python 3.7+ environment
- **Frontend**: 
  - HTML5, CSS3, JavaScript (Vanilla)
  - Font Awesome for icons
  - Responsive design with CSS Grid/Flexbox
- **Security**:
  - CSRF protection
  - File upload validation
  - Input sanitization
  - Error handling
- **Performance**:
  - Automated link performance monitoring
  - Response time tracking
  - Health checks
  - Error logging system

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- MongoDB 4.4+
- Git

### Installation

1. Clone the repository
```bash
git clone <repository-url>
```

2. Navigate to project directory
```bash
cd project-bolt-sb1-jw5tfp2t/project
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Start the application
```bash
python main.py
```

5. Access the application at `http://127.0.0.1:5000`

## 📁 Project Structure

```plaintext
project/
├── main.py              # Core application logic
├── templates/           # HTML templates
├── static/             # Static assets (CSS, JS, images)
├── logs/              # Application logs
└── requirements.txt    # Python dependencies
```

## 💡 Key Features In-Depth

### Inventory Management
- Add, edit, and delete inventory items
- Track stock levels in real-time
- Set minimum stock alerts
- Upload product images
- Track product performance

### Sales Management
- Process sales transactions
- Generate digital receipts
- Track payment status
- Monitor sales history
- Export sales reports

### Customer Management
- Maintain customer profiles
- Track purchase history
- Manage customer communications
- Set customer-specific pricing

## 📦 Extended Features

### Advanced Inventory Management
- Stock level alerts
- Product categorization
- Image upload with validation
- Price trend tracking
- Quick sale functionality
- Detailed product metrics

### Comprehensive Customer Management
- Multiple customer types (Retail, Wholesale, Distributor, Corporate)
- Credit limit management
- Payment terms configuration
- Purchase history tracking
- Customer-specific pricing

### Sales & Receipt System
- Digital receipt generation
- Multiple payment methods
- Sales history tracking
- Reference number generation
- Batch processing capability

## 🔍 Performance Monitoring

Monitor your system's performance with built-in tools:
- Link performance tracking
- Response time monitoring
- Error logging and alerts
- System health checks

## 🔧 Development Setup

1. Set up MongoDB:
```bash
# Start MongoDB service
mongod --dbpath /path/to/data/db
```

2. Set environment variables:
```bash
# Create .env file
SECRET_KEY=your-secret-key
MONGODB_URI=mongodb://localhost:27017/IMS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run tests:
```bash
pytest
```

5. Start development server:
```bash
python main.py
```

## 📚 API Documentation

### Inventory Endpoints
- `GET /inventory` - List all inventory items
- `POST /add_inventory` - Add new inventory item
- `GET/POST /edit_inventory/<item_id>` - Edit inventory item
- `GET /product/<product_id>` - Get product details

### Customer Endpoints
- `GET /customers` - List all customers
- `POST /add_customer` - Add new customer
- `GET/POST /edit_customer/<customer_id>` - Edit customer details
- `GET /customer/<customer_id>/history` - Get customer history

### Sales Endpoints
- `GET /sales` - List all sales
- `POST /quick_sale` - Process quick sale
- `GET /sales/print/<reference_no>` - Generate sale receipt

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📫 Contact & Support

- **Email**: [support@projectbolt.com](mailto:support@projectbolt.com)
- **Issues**: Submit issues through our [GitHub Issues](https://github.com/yourusername/project-bolt/issues)
- **Documentation**: [Project Wiki](https://github.com/yourusername/project-bolt/wiki)

---

<div align="center">
  <p>Made with ❤️ by Team Bolt</p>
  <p>© 2023 Project Bolt. All rights reserved.</p>
</div>
