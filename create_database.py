import pyodbc

def create_database():
    """Manually create and reset the EmployeeDB database"""
    
    conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=master;Trusted_Connection=yes"
    
    try:
        conn = pyodbc.connect(conn_str)
        conn.autocommit = True
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'EmployeeDB'")
        if cursor.fetchone():
            print("✓ EmployeeDB database already exists")
        else:
            print("Creating EmployeeDB database...")
            cursor.execute("CREATE DATABASE EmployeeDB")
            print("✓ EmployeeDB database created successfully")
        
        conn.close()
        
        conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=EmployeeDB;Trusted_Connection=yes"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Drop and recreate table to ensure correct schema
        print("Dropping existing employees table if it exists...")
        cursor.execute("IF EXISTS (SELECT * FROM sysobjects WHERE name='employees' AND xtype='U') DROP TABLE employees")
        
        print("Creating employees table...")
        cursor.execute('''
            CREATE TABLE employees (
                ID INT PRIMARY KEY,
                Name NVARCHAR(100) NOT NULL,
                Email NVARCHAR(100) NOT NULL,
                Department NVARCHAR(50) NOT NULL,
                Designation NVARCHAR(50) NOT NULL
            )
        ''')
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_employees_Department' AND object_id = OBJECT_ID('employees'))
            CREATE INDEX IX_employees_Department ON employees(Department)
        ''')
        conn.commit()
        print("✓ Employees table and index created successfully")
        
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Inserting sample data...")
            sample_data = [
                (1, 'John Doe', 'john.doe@example.com', 'IT', 'Software Engineer'),
                (2, 'Jane Smith', 'jane.smith@example.com', 'HR', 'HR Manager'),
                (3, 'Bob Johnson', 'bob.johnson@example.com', 'Finance', 'Accountant'),
                (4, 'Alice Brown', 'alice.brown@example.com', 'IT', 'DevOps Engineer'),
                (5, 'Charlie Wilson', 'charlie.wilson@example.com', 'Marketing', 'Marketing Coordinator'),
                (6, 'Diana Prince', 'diana.prince@example.com', 'HR', 'Recruiter'),
                (7, 'Peter Parker', 'peter.parker@example.com', 'IT', 'Web Developer'),
                (8, 'Mary Johnson', 'mary.johnson@example.com', 'Finance', 'Financial Analyst'),
                (9, 'David Miller', 'david.miller@example.com', 'Marketing', 'Content Creator'),
                (10, 'Sarah Connor', 'sarah.connor@example.com', 'IT', 'Data Scientist')
            ]
            
            for emp in sample_data:
                cursor.execute("INSERT INTO employees (ID, Name, Email, Department, Designation) VALUES (?, ?, ?, ?, ?)", emp)
            
            conn.commit()
            print(f"✓ {len(sample_data)} sample employees inserted")
        else:
            print(f"✓ Database already contains {count} employees")
        
        conn.close()
        print("\n" + "="*50)
        print("DATABASE SETUP COMPLETE!")
        print("You can now run: python app.py")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure SQL Server is running")
        print("2. Check that your Windows user has permissions")
        print("3. Try running as Administrator")

if __name__ == "__main__":
    create_database()