import pyodbc
import sys

def test_sql_server_connection():
    """Test different SQL Server connection options"""
    
    connection_options = [
        {
            'name': 'LocalDB (mssqllocaldb)',
            'server': '(localdb)\\mssqllocaldb',
            'conn_str': "DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\mssqllocaldb;DATABASE=master;Trusted_Connection=yes"
        },
        {
            'name': 'LocalDB (ProjectsV13)',
            'server': '(localdb)\\ProjectsV13',
            'conn_str': "DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\ProjectsV13;DATABASE=master;Trusted_Connection=yes"
        },
        {
            'name': 'SQL Server Express',
            'server': 'localhost\\SQLEXPRESS',
            'conn_str': "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes"
        },
        {
            'name': 'Default SQL Server',
            'server': 'localhost',
            'conn_str': "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=master;Trusted_Connection=yes"
        }
    ]
    
    print("Testing SQL Server connections...")
    print("=" * 50)
    
    working_connection = None
    
    for option in connection_options:
        try:
            print(f"Testing {option['name']}...")
            conn = pyodbc.connect(option['conn_str'])
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"✓ SUCCESS: {option['name']}")
            print(f"  Server: {option['server']}")
            print(f"  Version: {version[:50]}...")
            
            working_connection = option
            conn.close()
            break
            
        except Exception as e:
            print(f"✗ FAILED: {option['name']}")
            print(f"  Error: {str(e)[:100]}...")
        
        print()
    
    if working_connection:
        print("=" * 50)
        print("RECOMMENDED CONFIGURATION:")
        print(f"Update your .env with this server setting:")
        print(f"DB_SERVER={working_connection['server']}")
        
        try:
            conn = pyodbc.connect(working_connection['conn_str'])
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sys.databases WHERE name = 'EmployeeDB'")
            if cursor.fetchone():
                print("✓ EmployeeDB database already exists")
            else:
                print("Creating EmployeeDB database...")
                cursor.execute("CREATE DATABASE EmployeeDB")
                conn.commit()
                print("✓ EmployeeDB database created successfully")
            
            conn.close()
            
        except Exception as e:
            print(f"Error creating database: {e}")
    else:
        print("=" * 50)
        print("No working SQL Server connection found!")
        print("\nTroubleshooting steps:")
        print("1. Install SQL Server LocalDB or Express")
        print("2. Start LocalDB: sqllocaldb start mssqllocaldb")
        print("3. Install ODBC Driver 17 for SQL Server")
        print("4. Check Windows Authentication is enabled")

def list_available_drivers():
    """List available ODBC drivers"""
    print("\nAvailable ODBC Drivers:")
    print("=" * 30)
    drivers = pyodbc.drivers()
    for driver in drivers:
        if 'SQL Server' in driver:
            print(f"✓ {driver}")

if __name__ == "__main__":
    print("SQL Server Setup and Connection Test")
    print("=" * 50)
    
    try:
        list_available_drivers()
        print()
        test_sql_server_connection()
    except ImportError:
        print("pyodbc not installed. Please run: pip install pyodbc")
        sys.exit(1)