import sqlite3

def create_database():
    """Create the database and tables if they do not exist."""
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
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password_hash):
    """Add a new user to the database."""
    conn = sqlite3.connect('tasks_app.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()

def get_user(username):
    """Get a user from the database."""
    conn = sqlite3.connect('tasks_app.db')
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def add_task(username, title, due_date):
    """Add a new task to the database."""
    conn = sqlite3.connect('tasks_app.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (username, title, due_date) VALUES (?, ?, ?)', (username, title, due_date))
    conn.commit()
    conn.close()

def get_tasks(username):
    """Get all tasks for a user from the database."""
    conn = sqlite3.connect('tasks_app.db')
    c = conn.cursor()
    c.execute('SELECT title, due_date FROM tasks WHERE username = ?', (username,))
    tasks = c.fetchall()
    conn.close()
    return tasks
def validate_due_date(due_date):
    """Check if the due date is in the correct format (YYYY-MM-DD)."""
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def register_user():
    """Register a new user with hashed password."""
    username = input("Enter a username: ")
    if get_user(username):
        print("Username already exists. Please choose another.")
        return
    password = input("Enter a passcode: ")
    password_hash = hash_password(password)
    add_user(username, password_hash)
    print("Registration successful!")

def login_user():
    """Log in an existing user."""
    users = load_users()
    username = input("Enter your username: ")
    password = input("Enter your passcode: ")
    stored_password_hash = get_user(username)
    if stored_password_hash and check_password(stored_password_hash, password):
        print("Login successful!")
        return username
    else:
        print("Invalid username or passcode.")
        return None


def main():
    create_database()

    while True:
        print("\nWelcome to My Tasks App")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == '1':
            register_user()
        elif choice == '2':
            username = login_user()
            if username:
                while True:
                    print("\nTask Management")
                    print("1. Add Task")
                    print("2. Show Tasks")
                    print("3. Logout")
                    task_choice = input("Choose an option (1/2/3): ")

                    if task_choice == '1':
                        title = input("Enter task title: ")
                        due_date = input("Enter due date (YYYY-MM-DD): ")
                        if validate_due_date(due_date):
                            add_task(username, title, due_date)
                            print("Task added successfully!")
                        else:
                            print("Invalid date format. Please use YYYY-MM-DD.")
                    elif task_choice == '2':
                        tasks = get_tasks(username)
                        if not tasks:
                            print("No tasks found.")
                        else:
                            print(f"\nTasks for {username}:")
                            for idx, (title, due_date) in enumerate(tasks, start=1):
                                print(f"{idx}. {title} (Due: {due_date})")
                    elif task_choice == '3':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Please choose 1, 2, or 3.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == '__main__':
    main()
