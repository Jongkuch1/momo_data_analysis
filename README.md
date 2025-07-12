# MoMo Data Analysis Dashboard

A comprehensive full-stack application for analyzing MTN Mobile Money (MoMo) SMS transaction data. This project processes XML SMS data, categorizes transactions, stores them in a database, and provides an interactive web dashboard for analysis and visualization.

## 🎯 Project Overview

This application demonstrates enterprise-level full-stack development skills by:
- Processing and cleaning SMS data from XML format
- Categorizing transactions into 9 different types
- Storing structured data in a relational database
- Providing a RESTful API for data access
- Creating an interactive dashboard with visualizations

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   XML Data      │───▶│  Data Processor │───▶│   SQLite DB     │
│   (SMS Messages)│    │   (Python)      │    │  (Transactions) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Web Dashboard  │◀───│   Flask API     │◀───│   Database      │
│ (HTML/CSS/JS)   │    │   (REST API)    │    │   Queries       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Transaction Categories

The system categorizes SMS messages into the following transaction types:

1. **Incoming Money** - Money received from other users
2. **Payments to Code Holders** - Payments made to merchants/services
3. **Transfers to Mobile Numbers** - Money sent to phone numbers
4. **Bank Deposits** - Money deposited to bank accounts
5. **Airtime Bill Payments** - Airtime purchases
6. **Cash Power Bill Payments** - Electricity bill payments
7. **Third Party Transactions** - Transactions initiated by third parties
8. **Agent Withdrawals** - Cash withdrawals from agents
9. **Bank Transfers** - Direct bank transfers
10. **Internet/Voice Bundle Purchases** - Data and voice bundle purchases

## 🛠️ Technologies Used

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Web framework for API development
- **SQLite** - Lightweight database for data storage
- **xml.etree.ElementTree** - XML parsing
- **Regular Expressions** - Pattern matching for data extraction

### Frontend
- **HTML5** - Structure and markup
- **CSS3** - Styling with responsive design
- **JavaScript (ES6+)** - Interactive functionality
- **Chart.js** - Data visualization library

## 📁 Project Structure

```
momo-data-analysis/
├── backend/
│   ├── data_processor.py      # Main data processing script
│   ├── api.py                 # Flask REST API
│   ├── requirements.txt       # Python dependencies
│   └── momo_transactions.db   # SQLite database (generated)
├── frontend/
│   ├── index.html            # Main dashboard page
│   ├── styles.css            # CSS styling
│   └── script.js             # JavaScript functionality
├── data/
│   └── sms_data.xml          # Sample XML data file
├── docs/
│   └── report.pdf            # Project documentation
└── README.md                 # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone/Download the Project
```bash
# If using Git
git clone <repository-url>
cd momo-data-analysis

# Or download and extract the ZIP file
```

### Step 2: Set Up Python Environment
```bash
# Navigate to backend directory
cd backend

# Install required packages
pip install -r requirements.txt
```

### Step 3: Process the Data
```bash
# Run the data processor to parse XML and populate database
python data_processor.py
```

### Step 4: Start the API Server
```bash
# Start the Flask API server
python api.py
```
The API will be available at `http://localhost:5000`

### Step 5: Open the Dashboard
1. Navigate to the `frontend` directory
2. Open `index.html` in your web browser
3. The dashboard will automatically connect to the API and load data

## 📊 Dashboard Features

### Statistics Overview
- Total number of transactions
- Total transaction amount
- Average transaction value
- Largest single transaction

### Interactive Visualizations
- **Pie Chart**: Transaction distribution by type
- **Bar/Line Chart**: Monthly transaction volume and amounts

### Data Management
- **Search**: Find transactions by text content
- **Filters**: Filter by type, date range, and amount range
- **Detailed View**: Click any transaction to see full details

### Responsive Design
- Mobile-friendly interface
- Adaptive layouts for different screen sizes
- Touch-friendly controls

## 🔧 API Endpoints

### GET /api/transactions
Retrieve transactions with optional filtering
- **Parameters**: `type`, `start_date`, `end_date`, `min_amount`, `max_amount`, `limit`
- **Response**: Array of transaction objects

### GET /api/statistics
Get aggregated statistics
- **Response**: Object with overall stats, type breakdown, and monthly data

### GET /api/transaction/{id}
Get detailed information for a specific transaction
- **Response**: Single transaction object with all fields

### GET /api/search
Search transactions by text
- **Parameters**: `q` (search query)
- **Response**: Array of matching transactions

## 📈 Database Schema

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT,
    transaction_type TEXT NOT NULL,
    amount REAL,
    fee REAL DEFAULT 0,
    sender TEXT,
    recipient TEXT,
    phone_number TEXT,
    agent_name TEXT,
    agent_phone TEXT,
    bank_name TEXT,
    reference TEXT,
    meter_number TEXT,
    bundle_type TEXT,
    bundle_size TEXT,
    validity_period TEXT,
    date_time TEXT,
    raw_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎥 Video Demonstration

**[📹 Watch 5-Minute Demo Video]. 

The video demonstration covers:
- System overview and MTN-styled dashboard
- Database design and transaction categorization
- Live demonstration of search, filter, and visualization features
- Code walkthrough of key components and API integration

## ⚡ Quick Start

**Option 1: Instant Demo**
```bash
# View MTN-styled dashboard immediately
Open frontend/demo.html in your browser
```

**Option 2: Full Application**
```bash
# Windows users - double click
run.bat

# Or manually
cd backend && python data_processor.py && python api.py
```

## 🧪 Testing the Application

### Sample Data
The project includes sample XML data with 20 diverse transaction examples covering all supported transaction types.

### Manual Testing
1. Verify data processing by checking the generated database
2. Test API endpoints using browser or tools like Postman
3. Interact with dashboard features (search, filter, detail view)
4. Test responsive design on different screen sizes

## 🔍 Key Implementation Details

### Data Processing Logic
- Uses regular expressions for pattern matching
- Handles missing or malformed data gracefully
- Logs unprocessed messages for review
- Normalizes amounts and dates

### Error Handling
- Comprehensive try-catch blocks
- Logging for debugging and monitoring
- User-friendly error messages in the UI
- Graceful degradation when API is unavailable

### Performance Considerations
- Efficient database queries with proper indexing
- Lazy loading of transaction details
- Optimized chart rendering
- Responsive pagination for large datasets

## 📝 Development Approach

### Design Decisions
1. **SQLite Database**: Chosen for simplicity and portability
2. **Flask API**: Lightweight and perfect for this scale
3. **Vanilla JavaScript**: No framework dependencies, better performance
4. **Chart.js**: Reliable and feature-rich visualization library

### Challenges Overcome
1. **Data Inconsistency**: SMS messages have varying formats
2. **Pattern Recognition**: Complex regex patterns for accurate categorization
3. **UI Responsiveness**: Ensuring good UX across devices
4. **API Integration**: Handling asynchronous operations smoothly

## 🚀 Future Enhancements

- Real-time data processing with WebSocket connections
- Advanced analytics with machine learning insights
- Export functionality (PDF, Excel)
- User authentication and role-based access
- Integration with actual MoMo API for live data

## 👥 Authors

**Jongkuch Isaac Chol Anyar**
- 📧 Email: j.anyar@alustudent.com
- 🐙 GitHub: https://github.com/Jongkuch1/
- 💼 LinkedIn: https://www.linkedin.com/in/jongkuch-anyar-36535131b/
- 🎓 Institution: African Leadership University

## 🎨 MTN Branding

This dashboard features authentic MTN styling:
- **Colors**: MTN Yellow (#FFCB05) and professional black
- **Typography**: Corporate fonts and spacing
- **Branding**: MTN logo and "Everywhere you go" tagline
- **Design**: Professional mobile money interface

## 📄 License

This project is developed for educational purposes as part of a summative assignment.

---

**Note**: This application is a demonstration project and should not be used with real financial data without proper security measures and compliance considerations.# momo_data_analysis
