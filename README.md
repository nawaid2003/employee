# Employee Management System

A comprehensive Flask-based web application that fulfills both the **Employee Filter App** (basic level) and **Internal Employee Dashboard** (experienced level) requirements from Modus ETP's assignment.

## 🎯 Assignment Completion Summary

### ✅ Basic Level Requirements (Employee Filter App)

- **Login Page** (`/login`) - Flask session-based authentication with hardcoded credentials
- **Upload Page** (`/upload`) - Excel file upload with pandas/openpyxl processing
- **Filter Page** (`/filter`) - Select2 dropdown with AJAX-based department filtering
- **Database Integration** - SQL Server with pyodbc for data storage
- **Data Fields** - ID, Name, Department extraction and storage

### ✅ Experienced Level Requirements (Internal Employee Dashboard)

- **Secure Login** (`/login`) - CSRF-protected authentication form
- **Enhanced Upload** (`/upload`) - Extended fields (ID, Name, Email, Department, Designation)
- **Advanced Search** (`/search`) - Department filtering with comprehensive employee display
- **REST API** (`/api/employees`) - JSON endpoint with department filtering
- **Bonus Features**:
  - Mock Azure Key Vault simulation via environment variables
  - Blob Storage simulation with local file storage
  - Template download functionality

## 🚀 Features

### Core Functionality

- **Dual Interface**: Choose between basic "Employer Application" and advanced "Employee Dashboard"
- **Secure Authentication**: CSRF-protected login system
- **Excel Processing**: Upload `.xlsx` files with comprehensive data validation
- **Department Filtering**: Real-time AJAX-based search and filtering
- **RESTful API**: JSON endpoints for programmatic access

### Advanced Features

- **Modern UI**: Bootstrap 5 with responsive design and animations
- **Data Validation**: Unique ID validation, email format checking, numeric ID enforcement
- **Template Download**: Pre-formatted Excel template for data uploads
- **Blob Storage**: UUID-based file storage simulation
- **Error Handling**: Comprehensive error management and logging
- **Empty State Handling**: Graceful handling of empty database scenarios

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.9+)
- **Database**: SQL Server 2022 with ODBC Driver 17
- **Frontend**: Bootstrap 5, jQuery, Select2
- **Data Processing**: pandas, openpyxl
- **Security**: CSRF protection, session management
- **File Storage**: Local blob storage simulation

## 📋 Prerequisites

- Python 3.9 or higher
- SQL Server 2022 (localhost)
- ODBC Driver 17 for SQL Server
- Windows OS (for Trusted_Connection)

## 🔧 Installation & Setup

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd employee-management-system
pip install -r requirements.txt
```

### 2. Database Setup

Run one of the following options:

**Option A: Python Script**

```bash
python create_database.py
```

**Option B: SQL Server Management Studio**

```sql
-- Execute sql_script.sql in SSMS
```

### 3. Environment Configuration

Create a `.env` file with:

```env
DB_SERVER=localhost
DB_NAME=EmployeeDB
DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_TRUSTED_CONNECTION=yes
```

### 4. Generate Sample Data (Optional)

```bash
python generate_employees.py
```

This creates a sample `employees.xlsx` file with test data.

### 5. Run the Application

```bash
python app.py
```

Access the application at: `http://localhost:5000`

## 📱 Usage Guide

### Getting Started

1. **Home Page**: Choose between "Employer Application" (basic) or "Employee Dashboard" (advanced)
2. **Login**: Use credentials `admin` / `admin123`
3. **Upload**: Upload Excel files or download the template
4. **Search**: Filter employees by department
5. **API Access**: Use programmatic endpoints for integration

### User Interfaces

#### Employer Application (`/employer`)

- Simplified interface for basic filtering
- Displays: ID, Name, Department
- AJAX-powered department selection

#### Employee Dashboard (`/dashboard/*`)

- **Upload** (`/dashboard/upload`): Full Excel upload functionality
- **Search** (`/dashboard/search`): Comprehensive employee search
- Displays: ID, Name, Email, Department, Designation

### API Endpoints

#### Get Employees

```bash
# Get all employees
curl -u admin:admin123 http://localhost:5000/api/employees

# Filter by department
curl -u admin:admin123 "http://localhost:5000/api/employees?department=IT"

# Employer mode (limited fields)
curl -u admin:admin123 "http://localhost:5000/api/employees?department=IT&employer=true"
```

#### Get Departments

```bash
curl -u admin:admin123 http://localhost:5000/api/departments
```

## 📊 Database Schema

### Employees Table

```sql
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) UNIQUE,
    department NVARCHAR(50) NOT NULL,
    designation NVARCHAR(100)
);

-- Indexes for performance
CREATE INDEX idx_employees_department ON employees(department);
CREATE INDEX idx_employees_email ON employees(email);
```

## 🗂️ Project Structure

```
employee-management-system/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables
├── sql_script.sql             # Database setup script
├── create_database.py         # Database creation utility
├── generate_employees.py      # Sample data generator
├── employees.xlsx             # Sample Excel data
├── templates/
│   ├── base.html             # Bootstrap layout
│   ├── index.html            # Landing page
│   ├── login.html            # Login form
│   ├── upload.html           # Upload interface
│   ├── search.html           # Dashboard search
│   └── employer.html         # Employer filtering
├── BlobStorage/              # Simulated blob storage
├── uploads/                  # File uploads
└── app.log                   # Application logs
```

## 🧪 Testing Results

**Test Environment**: Windows 10, Python 3.9, SQL Server 2022

### ✅ Test Results

- **Authentication**: Login successful, CSRF protection verified
- **File Upload**: Successfully uploaded `employees.xlsx` (10 records)
- **Database**: Data verified in SQL Server Management Studio
- **Search Functionality**: Department filtering working correctly
- **API Endpoints**: All endpoints responding with correct data
- **Blob Storage**: Files saved with UUID naming convention
- **UI/UX**: Bootstrap styling and animations functional

## 🔍 Troubleshooting

### Common Issues

**Database Connection Issues**

```bash
# Ensure SQL Server is running
net start MSSQLSERVER

# Check connection
python test_sql_server_connection.py
```

**Permission Issues**

```sql
-- Grant necessary permissions in SSMS
USE EmployeeDB;
GRANT SELECT, INSERT, UPDATE, DELETE ON employees TO [YourWindowsUser];
```

**Excel File Issues**

```bash
# Regenerate sample data if needed
python generate_employees.py
```

**Application Logs**
Check `app.log` for detailed error information and debugging.

## 🎯 Assignment Fulfillment

This project successfully addresses all requirements from both difficulty levels:

### Basic Level ✅

- Flask session-based authentication
- Excel file upload and processing
- SQL Server integration with pyodbc
- Department filtering with AJAX
- Clean, modular code structure

### Experienced Level ✅

- CSRF-protected authentication
- Enhanced data fields processing
- RESTful API with authentication
- Mock Key Vault and Blob Storage
- Professional UI with Bootstrap 5

### Additional Enhancements

- Responsive design for mobile compatibility
- Comprehensive error handling
- Data validation and sanitization
- Template download functionality
- Performance optimizations with database indexing
