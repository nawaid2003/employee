import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, jsonify, flash, send_file
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired
import pandas as pd
import pyodbc
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import logging
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
app.config['UPLOAD_FOLDER'] = 'Uploads'
app.config['BLOB_FOLDER'] = 'BlobStorage'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

csrf = CSRFProtect(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['BLOB_FOLDER'], exist_ok=True)

auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

DB_CONFIG = {
    'server': os.getenv('DB_SERVER', 'localhost'),
    'database': os.getenv('DB_NAME', 'EmployeeDB'),
    'driver': os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}'),
    'trusted_connection': os.getenv('DB_TRUSTED_CONNECTION', 'yes')
}

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class UploadForm(FlaskForm):
    file = FileField('Excel File', validators=[DataRequired()])

def get_db_connection(use_master=False):
    try:
        database = 'master' if use_master else DB_CONFIG['database']
        conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={database};Trusted_Connection={DB_CONFIG['trusted_connection']}"
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        return None

def init_db():
    conn = get_db_connection(use_master=True)
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{DB_CONFIG['database']}') CREATE DATABASE {DB_CONFIG['database']}")
            conn.commit()
            logging.info(f"Database {DB_CONFIG['database']} ready")
        except Exception as e:
            logging.error(f"Database creation error: {e}")
        finally:
            conn.close()
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('employees') AND name = 'Email') ALTER TABLE employees ADD Email NVARCHAR(100) NOT NULL DEFAULT ''")
            cursor.execute("IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('employees') AND name = 'Designation') ALTER TABLE employees ADD Designation NVARCHAR(50) NOT NULL DEFAULT ''")
            
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='employees' AND xtype='U')
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
            logging.info("Database table and index initialized successfully")
        except Exception as e:
            logging.error(f"Table initialization error: {e}")
        finally:
            conn.close()
    else:
        logging.error("Could not connect to database for table creation")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard.upload'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/employer')
def employer():
    if 'logged_in' not in session or 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('employer.html')

@dashboard_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'logged_in' not in session or 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and file.filename.endswith('.xlsx'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            blob_filename = f"{uuid.uuid4()}_{filename}"
            blob_filepath = os.path.join(app.config['BLOB_FOLDER'], blob_filename)
            file.save(filepath)
            
            try:
                df = pd.read_excel(filepath)
                
                required_columns = ['ID', 'Name', 'Email', 'Department', 'Designation']
                if not all(col in df.columns for col in required_columns):
                    flash(f'Excel file must contain columns: {", ".join(required_columns)}', 'danger')
                    return redirect(request.url)
                
                df = df[required_columns].dropna()
                
                if not df['ID'].apply(lambda x: isinstance(x, (int, float)) and x == int(x)).all():
                    flash('All ID values must be integers', 'danger')
                    return redirect(request.url)
                
                if df['ID'].duplicated().any():
                    flash('ID values must be unique', 'danger')
                    return redirect(request.url)
                
                if not df['Email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$').all():
                    flash('Invalid email format in Excel file', 'danger')
                    return redirect(request.url)
                
                conn = get_db_connection()
                if not conn:
                    flash('Database connection error', 'danger')
                    return redirect(request.url)
                
                cursor = conn.cursor()
                try:
                    cursor.execute('DELETE FROM employees')
                    for _, row in df.iterrows():
                        cursor.execute(
                            'INSERT INTO employees (ID, Name, Email, Department, Designation) VALUES (?, ?, ?, ?, ?)',
                            int(row['ID']), str(row['Name']), str(row['Email']), str(row['Department']), str(row['Designation'])
                        )
                    conn.commit()
                    flash(f'Successfully uploaded {len(df)} employees', 'success')
                    
                    os.rename(filepath, blob_filepath)
                    logging.info(f"File saved to blob storage: {blob_filepath}")
                    
                except pyodbc.IntegrityError as e:
                    logging.error(f"Database integrity error: {e}")
                    flash(f'Error saving data to database: Integrity constraint violation (e.g., duplicate ID)', 'danger')
                except pyodbc.DataError as e:
                    logging.error(f"Database data error: {e}")
                    flash(f'Error saving data to database: Invalid data format (e.g., string too long)', 'danger')
                except Exception as e:
                    logging.error(f"Database insert error: {e}")
                    flash(f'Error saving data to database: {str(e)}', 'danger')
                finally:
                    conn.close()
                
            except Exception as e:
                logging.error(f"File processing error: {e}")
                flash('Error processing Excel file', 'danger')
            
            if os.path.exists(filepath):
                os.remove(filepath)
        else:
            flash('Please upload an Excel file (.xlsx)', 'danger')
    
    return render_template('upload.html', form=form)

@dashboard_bp.route('/search')
def search():
    if 'logged_in' not in session or 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('search.html')

@dashboard_bp.route('/download_template')
def download_template():
    template_data = [
        {'ID': 1, 'Name': 'John Doe', 'Email': 'john.doe@example.com', 'Department': 'IT', 'Designation': 'Software Engineer'}
    ]
    df = pd.DataFrame(template_data)
    template_path = os.path.join(app.config['UPLOAD_FOLDER'], 'employees_template.xlsx')
    df.to_excel(template_path, index=False)
    return send_file(template_path, as_attachment=True, download_name='employees_template.xlsx')

@main_bp.route('/api/employees')
def get_employees():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    department = request.args.get('department')
    is_employer = request.args.get('employer', 'false').lower() == 'true'
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if is_employer:
                if department:
                    cursor.execute('SELECT ID, Name, Department FROM employees WHERE Department = ? ORDER BY Name', department)
                else:
                    cursor.execute('SELECT ID, Name, Department FROM employees ORDER BY Name')
                employees = [{'id': row[0], 'name': row[1], 'department': row[2]} for row in cursor.fetchall()]
            else:
                if department:
                    cursor.execute('SELECT ID, Name, Email, Department, Designation FROM employees WHERE Department = ? ORDER BY Name', department)
                else:
                    cursor.execute('SELECT ID, Name, Email, Department, Designation FROM employees ORDER BY Name')
                employees = [{'id': row[0], 'name': row[1], 'email': row[2], 'department': row[3], 'designation': row[4]} for row in cursor.fetchall()]
            return jsonify({'employees': employees})
        except Exception as e:
            logging.error(f"Database query error: {e}")
            return jsonify({'error': 'Database error'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection error'}), 500

@main_bp.route('/api/departments')
def get_departments():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT DISTINCT Department FROM employees ORDER BY Department')
            departments = [row[0] for row in cursor.fetchall()]
            return jsonify({'departments': departments})
        except Exception as e:
            logging.error(f"Database query error: {e}")
            return jsonify({'error': 'Database error'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Database connection error'}), 500

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO)
    init_db()
    app.run(debug=True)