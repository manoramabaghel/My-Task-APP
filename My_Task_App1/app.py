from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key


# Database Schema:
import sqlite3

def create_database():
    conn = sqlite3.connect('tasks_app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            category TEXT,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()


def get_db_connection():
    conn = sqlite3.connect('tasks_app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE username = ? ORDER BY due_date ASC', (session['username'],)).fetchall()
    conn.close()

    return render_template('index.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username
            return redirect(url_for('index'))
        flash('Invalid username or passcode')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username already exists.')
            conn.close()
            return redirect(url_for('register'))
        conn.close()

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    due_date = request.form['due_date']

    if not title or not due_date:
        flash('Title and due date are required.')
        return redirect(url_for('index'))

    try:
        datetime.strptime(due_date, '%Y-%m-%d')
    except ValueError:
        flash('Invalid due date format. Use YYYY-MM-DD.')
        return redirect(url_for('index'))

    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (username, title, due_date) VALUES (?, ?, ?)', (session['username'], title, due_date))
    conn.commit()
    conn.close()

    flash('Task added successfully!')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
