import os
import json
from datetime import datetime
from tabulate import tabulate

# Path to the file where user credentials will be stored
USER_DATA_FILE = 'users.txt'
TASKS_DATA_FILE = 'tasks.json'

def load_users():
    """Load users from the data file."""
    users = {}
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                for line in file:
                    username, passcode = line.strip().split(',')
                    users[username] = passcode
        except IOError as e:
            print(f"Error reading file: {e}")
    return users


def save_user(username, passcode):
    """Save a new user to the data file."""
    try:
        with open(USER_DATA_FILE, 'a') as file:
            file.write(f'{username},{passcode}\n')
    except IOError as e:
        print(f"Error writing to file: {e}")

def load_tasks(username):
    """Load tasks for a specific user."""
    if os.path.exists(TASKS_DATA_FILE):
        try:
            with open(TASKS_DATA_FILE, 'r') as file:
                tasks = json.load(file)
                return tasks.get(username, [])
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading tasks file: {e}")
    return []

def save_task(username, title, due_date, category):
    """Save a new task for a specific user."""
    tasks = load_tasks(username)
    tasks.append({'title': title, 'due_date': due_date, 'category': category})
    all_tasks = {}
    if os.path.exists(TASKS_DATA_FILE):
        try:
            with open(TASKS_DATA_FILE, 'r') as file:
                all_tasks = json.load(file)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading tasks file: {e}")
    all_tasks[username] = tasks
    try:
        with open(TASKS_DATA_FILE, 'w') as file:
            json.dump(all_tasks, file, indent=4)
    except IOError as e:
        print(f"Error writing to tasks file: {e}")


def register_user():
    """Register a new user."""
    users = load_users()
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists. Please choose another.")
        return
    passcode = input("Enter a passcode: ")
    save_user(username, passcode)
    print("Registration successful!")


def login_user():
    """Log in an existing user."""
    users = load_users()
    username = input("Enter your username: ")
    passcode = input("Enter your passcode: ")
    if username in users and users[username] == passcode:
        print("Login successful!")
        return username
    else:
        print("Invalid username or passcode.")
        return None


def add_task(username):
    """Add a new task for the logged-in user."""
    title = input("Enter task title: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    category = input("Enter category: ")

    # Validate due date format
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    save_task(username, title, due_date,category)
    print("Task added successfully!")

# Sort and Filter Tasks
def sort_tasks(tasks, sort_by='due_date'):
    """Sort tasks based on the specified column."""
    return sorted(tasks, key=lambda x: x[sort_by])

def show_tasks(username, sort_by='due_date'):
    """Show all tasks for the logged-in user in a tabular format with sorting."""
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks for you. Please add one.")
        return

    #####
    # Ensure sort_by is a valid key
    valid_keys = {'title', 'due_date', 'category'}
    if sort_by not in valid_keys:
        print(f"Invalid sort key. Using default ('due_date').")
        sort_by = 'due_date'
    # Sort tasks based on the sort_by key
    tasks = sorted(tasks, key=lambda x: x.get(sort_by, ''))

    # Display tasks in a tabular format
    print(f"Number of tasks: {len(tasks)}")
    # # Counter for tasks
    # tasks = sort_tasks(tasks, sort_by='due_date')
    # print(f"Number of tasks: {len(tasks)}")

    table = [[task['title'], task['due_date'], task.get('category', '')] for task in tasks]
    headers = ["Title", "Due Date", "Category"]
    print(tabulate(table, headers=headers, tablefmt='grid'))

    # # Display tasks in a tabular format
    # table = []
    # for task in tasks:
    #     table.append([task['title'], task['due_date']])
    #
    # headers = ["Title", "Due Date"]
    # print(tabulate(table, headers=headers, tablefmt='grid'))
    # # print(f"\nTasks for {username}:")
    # # for idx, task in enumerate(tasks, start=1):
    # #     print(f"{idx}. {task['title']} (Due Date: {task['due_date']})")

# Add a search functionality to filter tasks by title:
def search_tasks(username):
    """Search tasks by title."""
    tasks = load_tasks(username)
    search_query = input("Enter the title to search: ").lower()
    filtered_tasks = [task for task in tasks if search_query in task['title'].lower()]

    if not filtered_tasks:
        print("No tasks found matching the search criteria.")
        return

    print(f"Number of tasks found: {len(filtered_tasks)}")

    # Display filtered tasks
    table = []
    for task in filtered_tasks:
        table.append([task['title'], task['due_date']])

    headers = ["Title", "Due Date"]
    print(tabulate(table, headers=headers, tablefmt='grid'))


def check_reminders(username):
    """Check and remind the user of tasks with due dates soon."""
    tasks = load_tasks(username)
    upcoming_tasks = []
    today = datetime.now()
    for task in tasks:
        due_date = datetime.strptime(task['due_date'], "%Y-%m-%d")
        if due_date <= today:
            upcoming_tasks.append(task)

    if upcoming_tasks:
        print("\nUpcoming Tasks:")
        for task in upcoming_tasks:
            print(f"- {task['title']} (Due: {task['due_date']})")
    else:
        print("No tasks are due today.")


def main():
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
                    print("3. Search Tasks")
                    print("4. Check Reminders")
                    print("5. Logout")
                    task_choice = input("Choose an option (1/2/3/4/5): ")
                    if task_choice == '1':
                        add_task(username)
                    elif task_choice == '2':
                        sort_by = input("Sort by (title/due_date/category): ").strip() or 'due_date'
                        show_tasks(username, sort_by)
                        # show_tasks(username)
                    elif task_choice == '3':
                        search_tasks(username)
                    elif task_choice == '4':
                        check_reminders(username)
                    elif task_choice == '5':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Please choose 1, 2, 3, 4 or 5.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == '__main__':
    main()

