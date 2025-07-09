Internal Employee Dashboard
A secure, API-driven Flask web application for uploading and managing employee data, with CSRF protection, modular structure, and bonus features simulating Key Vault and Azure Blob Storage.
Features

Secure Authentication: CSRF-protected login with admin / admin123.
Excel Upload: Upload .xlsx files with ID, Name, Email, Department, Designation, validated and stored in SQL Server.
Employee Search: Select2 dropdown for department filtering with AJAX-driven employee list (name and email).
REST API: /api/employees?department=<dept> endpoint for JSON data.
Bonus Features:
Mock Key Vault using .env for secure database configuration.
Simulated Azure Blob Storage with local BlobStorage folder.

Enhancements:
Random session secret key.
Unique and numeric ID validation.
Email format validation.
Empty database handling in search page.
Database index for performance.

Prerequisites

Python: 3.7+
SQL Server: SQL Server 2022, Express, or LocalDB
ODBC Driver: ODBC Driver 17 for SQL Server
Windows: For Trusted Connection authentication
Internet: For CDN resources (jQuery, Select2)

Installation

Clone or Download:

Clone the repository or download the project files.

Install SQL Server (if not installed):

Download SQL Server Express or LocalDB.
Start SQL Server:net start MSSQLSERVER

Install ODBC Driver 17 for SQL Server.

Set Up Python Environment:

Create and activate a virtual environment:python -m venv venv
.\venv\Scripts\activate # Windows

Install dependencies:pip install -r requirements.txt

Configure Environment:

Create .env in the project root with:DB_SERVER=localhost
DB_NAME=EmployeeDB
DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_TRUSTED_CONNECTION=yes

Run connection test to verify server:python test_sql_server_connection.py

Update DB_SERVER in .env if needed (e.g., localhost\SQLEXPRESS).

Set Up Database:

Create database and table:python create_database.py

This creates EmployeeDB, employees table, index, and sample data.
Alternatively, run sql_script.sql in SQL Server Management Studio (SSMS):USE master;
IF NOT EXISTS (SELECT _ FROM sys.databases WHERE name = 'EmployeeDB')
BEGIN
CREATE DATABASE EmployeeDB;
END
USE EmployeeDB;
IF NOT EXISTS (SELECT _ FROM sysobjects WHERE name='employees' AND xtype='U')
BEGIN
CREATE TABLE employees (
ID INT PRIMARY KEY,
Name NVARCHAR(100) NOT NULL,
Email NVARCHAR(100) NOT NULL,
Department NVARCHAR(50) NOT NULL,
Designation NVARCHAR(50) NOT NULL
);
CREATE INDEX IX_employees_Department ON employees(Department);
END

Generate Sample Excel File:

Run:python generate_employees.py

Creates employees.xlsx with 10 sample records.

Usage

Start the Application:
python app.py

Access at http://localhost:5000.

Login:

Use admin / admin123.
CSRF-protected form ensures security.
Invalid credentials show an error message.

Upload Employee Data:

Go to /upload.
Upload employees.xlsx (must have ID, Name, Email, Department, Designation).
Validates unique/numeric ID and email format.
Files are saved to BlobStorage (simulating Azure Blob Storage).
Success message confirms upload (e.g., “Successfully uploaded 10 employees”).

Search Employees:

Go to /search.
Select a department from the dropdown (populated via /api/departments).
View employees (name and email) for the selected department.
Empty database shows “No departments available” message.

API Access:

GET /api/employees?department=IT: Returns JSON with employees in the IT department.
GET /api/employees: Returns all employees.
Requires authentication (401 for unauthenticated requests).

File Structure
project/
├── app.py # Modular Flask app with blueprints
├── config.py # Configuration with mock Key Vault
├── .env # Secure database credentials
├── requirements.txt # Dependencies
├── sql_script.sql # SQL Server setup
├── create_database.py # Database setup with sample data
├── test_sql_server_connection.py # Connection tester
├── generate_employees.py # Sample Excel generator
├── employees.xlsx # Sample Excel file
├── templates/
│ ├── base.html # Base template with styles
│ ├── login.html # CSRF-protected login
│ ├── upload.html # CSRF-protected upload
│ └── search.html # Search with Select2
├── Uploads/ # Temporary file storage
└── BlobStorage/ # Simulated Azure Blob Storage

Configuration
Database Settings (.env)
DB_SERVER=localhost
DB_NAME=EmployeeDB
DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_TRUSTED_CONNECTION=yes

Authentication

Username: admin
Password: admin123

API Endpoints

GET /api/departments: Returns distinct departments.
GET /api/employees?department=<dept>: Returns employees filtered by department.
GET /api/employees: Returns all employees.

Testing Results
Tested on July 9, 2025:

Environment: Windows 10, Python 3.9, SQL Server 2022 (localhost), ODBC Driver 17.
Login: Authenticated with admin / admin123; CSRF token validated; invalid credentials showed error.
Upload: Uploaded employees.xlsx with 10 records; validated ID (unique/numeric) and Email; files saved to BlobStorage; confirmed in SSMS (SELECT \* FROM employees).
Search: Dropdown populated with IT, HR, Finance, Marketing; selecting IT showed 4 employees with names and emails; empty database showed “No departments available”.
API: GET /api/employees?department=IT returned JSON with 4 employees; GET /api/employees returned all 10; unauthorized requests returned 401.
Bonus: Database config loaded from .env; Excel files stored in BlobStorage with unique UUIDs.

Screenshots
Include for submission:

screenshots/login.png: Login page with CSRF-protected form.
screenshots/upload.png: Upload page with success message.
screenshots/search.png: Search page showing IT employees.

Troubleshooting

Database Connection:

Ensure SQL Server is running: net start MSSQLSERVER.
Verify ODBC Driver 17: python test_sql_server_connection.py.
Grant permissions in SSMS:USE EmployeeDB;
GRANT ALL ON employees TO [YourWindowsUser];

Excel Errors:

Ensure employees.xlsx has required columns.
Check for unique ID and valid email formats.

Port Conflict:

Change port in app.py:app.run(debug=True, port=5001)

Empty Dropdown:

Upload employees.xlsx to populate database.
Verify in SSMS: SELECT \* FROM employees.

Security Notes

CSRF protection via Flask-WTF.
Random secret key for sessions.
Database credentials in .env (mock Key Vault).
Hardcoded credentials for demo; use proper authentication in production.
Uploads and BlobStorage should be secured in production.

Enhancements for Upper Hand

Modular Design: Blueprints for clean routing.
Security: CSRF protection, secure secret key, .env for credentials.
Validation: Unique/numeric ID, email format checks.
Usability: Empty database message in search.
Performance: Index on Department.
Bonus: Mock Key Vault and Azure Blob Storage simulation.

License
For internal use and demonstration purposes.
