from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import os
import uuid
from database import init_db, get_db
from utils import calculate_similarity
import PyPDF2
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize database
init_db()

# Add default admin user
def init_admin_user():
    db = get_db()
    admin_user = db.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin_user:
        db.execute('INSERT INTO users (username, password_hash, role, credits) VALUES (?, ?, ?, ?)',
                   ('admin', 'admin', 'admin', 100))  # Default admin credentials
        db.commit()
        print("Default admin user created.")

init_admin_user()  # Call this function to create the default admin user

def reset_credits():
    db = get_db()
    db.execute("UPDATE users SET credits = 20")
    db.commit()
    print("User credits reset at midnight.")

scheduler = BackgroundScheduler()
scheduler.add_job(reset_credits, 'cron', hour=0, minute=0)  # Runs at midnight
scheduler.start()

atexit.register(lambda: scheduler.shutdown())
# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin') or session.get('username') != 'admin':
            flash('You do not have permission to access this page.')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'regular'  # Default role is 'regular'
        
        db = get_db()
        existing_user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if existing_user:
            flash('User already exists! Please choose a different username.', 'error')
            return redirect(url_for('register'))
        
        db.execute('INSERT INTO users (username, password_hash, role, credits) VALUES (?, ?, ?, ?)',
                   (username, password, role, 20))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user:
            if user['password_hash'] == password:  # Assuming passwords are stored as plaintext (not recommended)
                session['username'] = user['username']
                session['role'] = user['role']
                return redirect(url_for('profile'))
            else:
                flash('Incorrect password.', 'error')
        else:
            flash("Username doesn't exist. Please register.", 'error')

    return render_template('login.html')

# User profile
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (session['username'],)).fetchone()
    scans = db.execute('SELECT * FROM documents WHERE user_id = ?', (session['username'],)).fetchall()
    return render_template('profile.html', user=user, scans=scans)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if user['credits'] <= 0:
        flash('You have no credits left. Please wait until midnight or request more credits.')
        return redirect(url_for('request_credits'))
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename:
            try:
                # Check user credits
                db = get_db()
                user = db.execute('SELECT * FROM users WHERE username = ?', (session['username'],)).fetchone()
                if user['credits'] <= 0:
                    flash('You have no credits left. Please request more credits.')
                    return redirect(url_for('profile'))

                # Generate a unique filename to avoid conflicts
                unique_filename = str(uuid.uuid4()) + "_" + file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)

                # Extract text from the file
                if unique_filename.endswith('.pdf'):
                    with open(filepath, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        content = ""
                        for page in reader.pages:
                            content += page.extract_text()
                else:
                    with open(filepath, 'r') as f:
                        content = f.read()

                # Insert the document into the database
                cursor = db.cursor()
                cursor.execute('INSERT INTO documents (user_id, file_name, original_name, content) VALUES (?, ?, ?, ?)',
                               (session['username'], unique_filename, file.filename, content))
                db.commit()

                # Deduct 1 credit from the user and increment credits_used
                db.execute('''
                    UPDATE users
                    SET credits = credits - 1,
                        credits_used = credits_used + 1
                    WHERE username = ?
                ''', (session['username'],))
                db.commit()

                flash('Document uploaded successfully!')
                return redirect(url_for('matches', doc_id=cursor.lastrowid))
            except Exception as e:
                print(f"Error uploading file: {e}")
                flash(f'Error uploading file: {str(e)}')
                return redirect(url_for('upload'))
        else:
            flash('No file selected or invalid file!')
            return redirect(url_for('upload'))
    return render_template('upload.html')

# Document matching
@app.route('/matches/<int:doc_id>')
def matches(doc_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    db = get_db()
    current_doc = db.execute('SELECT * FROM documents WHERE id = ?', (doc_id,)).fetchone()
    all_docs = db.execute('SELECT * FROM documents WHERE user_id != ?', (session['username'],)).fetchall()

    similar_docs = []
    for doc in all_docs:
        similarity = calculate_similarity(current_doc['content'], doc['content'])
        if similarity > 0.7:  # Adjust threshold as needed
            similar_docs.append({
                'file_name': doc['original_name'],
                'similarity': similarity
            })

    return render_template('matches.html', similar_docs=similar_docs)

# Request additional credits
@app.route('/request_credits', methods=['GET', 'POST'])
def request_credits():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO credit_requests (user_id, status) VALUES (?, ?)',
                   (session['username'], 'pending'))
        db.commit()
        flash('Credit request submitted successfully!')
        return redirect(url_for('profile'))
    return render_template('request_credits.html')

# Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':  # Only allow default admin
            db = get_db()
            user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if user:
                session['username'] = user['username']
                session['role'] = user['role']
                session['is_admin'] = True
                flash('Admin login successful!')
                return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials or insufficient permissions!')
    return render_template('admin_login.html')

@app.route('/admin/manage-users')
@admin_required
def manage_users():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    return render_template('manage_users.html', users=users)

@app.route('/admin/edit-user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        flash('User not found!')
        return redirect(url_for('manage_users'))

    if request.method == 'POST':
        new_username = request.form['username']
        new_role = request.form['role']
        new_credits = request.form['credits']

        db.execute('UPDATE users SET username = ?, role = ?, credits = ? WHERE id = ?',
                   (new_username, new_role, new_credits, user_id))
        db.commit()
        flash('User updated successfully!')
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', user=user)

@app.route('/admin/manage-credit-requests')
@admin_required
def manage_credit_requests():
    db = get_db()
    credit_requests = db.execute('SELECT * FROM credit_requests').fetchall()
    return render_template('manage_credit_requests.html', credit_requests=credit_requests)

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db = get_db()

    # Fetch basic data
    users = db.execute('SELECT * FROM users').fetchall()
    credit_requests = db.execute('SELECT * FROM credit_requests').fetchall()

    # Track the number of scans per user per day
    scans_per_user_per_day = db.execute('''
        SELECT user_id, DATE(upload_date) AS date, COUNT(*) AS scan_count
        FROM documents
        GROUP BY user_id, DATE(upload_date)
    ''').fetchall()

    # Identify the most common scanned document names
    common_document_names = db.execute('''
        SELECT original_name, COUNT(*) AS scan_count
        FROM documents
        GROUP BY original_name
        ORDER BY scan_count DESC
    ''').fetchall()

    # View top users by scans
    top_users_by_scans = db.execute('''
        SELECT user_id, COUNT(*) AS total_scans
        FROM documents
        GROUP BY user_id
        ORDER BY total_scans DESC
    ''').fetchall()

    # Generate credit usage statistics
    credit_usage = db.execute('''
        SELECT username, credits_used
        FROM users
    ''').fetchall()

    return render_template('admin_dashboard.html',
                           users=users,
                           credit_requests=credit_requests,
                           scans_per_user_per_day=scans_per_user_per_day,
                           common_document_names=common_document_names,
                           top_users_by_scans=top_users_by_scans,
                           credit_usage=credit_usage)

# Approve Credit Request
@app.route('/admin/approve_request/<int:request_id>')
@admin_required
def approve_request(request_id):
    db = get_db()
    request = db.execute('SELECT * FROM credit_requests WHERE id = ?', (request_id,)).fetchone()
    db.execute('UPDATE credit_requests SET status = ? WHERE id = ?', ('approved', request_id))
    db.execute('UPDATE users SET credits = credits + 20 WHERE username = ?', (request['user_id'],))
    db.commit()
    flash('Credit request approved!')
    return redirect(url_for('admin_dashboard'))

# Deny Credit Request
@app.route('/admin/deny_request/<int:request_id>')
@admin_required
def deny_request(request_id):
    db = get_db()
    db.execute('UPDATE credit_requests SET status = ? WHERE id = ?', ('denied', request_id))
    db.commit()
    flash('Credit request denied!')
    return redirect(url_for('admin_dashboard'))

# Analytics Dashboard
@app.route('/admin/analytics')
@admin_required
def analytics_dashboard():
    db = get_db()
    scans_per_user_per_day = db.execute('''
        SELECT user_id, DATE(upload_date) AS date, COUNT(*) AS scan_count
        FROM documents
        GROUP BY user_id, DATE(upload_date)
    ''').fetchall()
    common_topics = db.execute('''
        SELECT topic, COUNT(*) AS scan_count
        FROM documents
        GROUP BY topic
        ORDER BY scan_count DESC
    ''').fetchall()
    top_users_by_scans = db.execute('''
        SELECT user_id, COUNT(*) AS total_scans
        FROM documents
        GROUP BY user_id
        ORDER BY total_scans DESC
    ''').fetchall()
    credit_usage = db.execute('''
        SELECT username, credits_used, credits_remaining
        FROM users
    ''').fetchall()
    return render_template('analytics_dashboard.html',
                           scans_per_user_per_day=scans_per_user_per_day,
                           common_topics=common_topics,
                           top_users_by_scans=top_users_by_scans,
                           credit_usage=credit_usage)

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session.pop('is_admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)