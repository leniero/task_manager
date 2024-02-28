import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Check if 'tasks.txt' exists and create if not
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as task_file:
        pass  # Just to create the file if it doesn't exist

# Check if 'user.txt' exists and create if not
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as user_file:
        user_file.write("admin;adm1n\n")  # Default admin account

def load_users():
    with open("user.txt", 'r') as user_file:
        users = {}
        for line in user_file:
            if line.strip():
                parts = line.strip().split(';')
                if len(parts) >= 2:  # Ensure there are at least two parts
                    username = parts[0]
                    password = parts[1]
                    users[username] = password
        return users

def load_tasks():
    with open("tasks.txt", 'r') as task_file:
        tasks = []
        for line in task_file:
            if line.strip():
                task_details = line.strip().split(';',4)    # Ensure there are at least four parts
                tasks.append(task_details)
        return tasks

def save_tasks(tasks):
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(";".join(task) + "\n") 

def reg_user(users):
    username = input("Enter new username: ")
    if username in users:
        print("Username already exists.")
        return
    password = input("Enter new password: ")
    confirm_password = input("Confirm new password: ")
    if password != confirm_password:
        print("Passwords do not match.")
        return
    users[username] = password
    with open("user.txt", "a") as user_file:
        user_file.write(f"{username};{password}\n") 
    print("User registered successfully.")

def add_task(tasks):
    # Get the details of the new task from the user
    user = input("Enter the username of the person responsible for the task: ")
    title = input("Enter the title of the task: ")
    description = input("Enter the description of the task: ")
    due_date = input("Enter the due date of the task (YYYY-MM-DD): ")
    
    # Validate the due date format
    try:
        datetime.strptime(due_date, DATETIME_STRING_FORMAT)
    except ValueError:
        print("This is the incorrect date string format. It should be YYYY-MM-DD")
        return
    
    # Create the task as a list of strings
    new_task = [user, title, description, due_date, 'No']
    
    # Append the new task to the list of tasks
    tasks.append(new_task)
    
    # Save the updated tasks to the file
    save_tasks(tasks)
    print("Task added successfully.")
    
def edit_task(task):
    print("Do you want to mark this task as complete or edit it? (complete/edit)")
    action = input().lower()
    if action == "complete":
        task[4] = "Yes"
        print("Task marked as complete.")
    elif action == "edit":
        # Allow editing the task
        new_user = input("Enter new user for the task: ")
        new_title = input("Enter new title for the task: ")
        new_description = input("Enter new description for the task: ")
        new_due_date = input("Enter new due date (YYYY-MM-DD): ")

        # Validate the new due date format
        try:
            datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
        except ValueError:
            print("This is the incorrect date string format. It should be YYYY-MM-DD")
            return

        # Update the task with the new details
        task[0] = new_user
        task[1] = new_title
        task[2] = new_description
        task[3] = new_due_date
        print("Task updated.")
    else:
        print("Invalid action.")


def view_all(tasks):
    # Find maximum length of each column for formatting
    user_length = max(len(task[0]) for task in tasks) if tasks else 4
    title_length = max(len(task[1]) for task in tasks) if tasks else 5
    desc_length = max(len(task[2]) for task in tasks) if tasks else 11
    due_length = max(len(task[3]) for task in tasks) if tasks else 8
    comp_length = max(len(task[4]) for task in tasks) if tasks else 9

    header = f"{'ID':<3} {'User':<{user_length}} {'Title':<{title_length}} {'Description':<{desc_length}} {'Due Date':<{due_length}} {'Completed':<{comp_length}}"
    print(header)
    print('-' * len(header))

    for i, task in enumerate(tasks, 1):
        user, title, description, due_date, completed = task
        print(f"{i:<3} {user:<{user_length}} {title:<{title_length}} {description:<{desc_length}} {due_date:<{due_length}} {completed:<{comp_length}}")

    # Allow the admin to select a task to edit
    task_number = int(input("\nEnter task number to edit, or -1 to return: "))
    if task_number == -1:
        return
    if 1 <= task_number <= len(tasks):
        edit_task(tasks[task_number - 1])
        save_tasks(tasks)  # Save the updated tasks list


def view_mine(tasks, username):
    user_tasks = [task for task in tasks if task[0] == username]
    
    if not user_tasks:
        print("You have no tasks.")
        return

    # Find maximum length of each column for formatting
    user_length = max(len(task[0]) for task in user_tasks) if user_tasks else 4
    title_length = max(len(task[1]) for task in user_tasks) if user_tasks else 5
    desc_length = max(len(task[2]) for task in user_tasks) if user_tasks else 11
    due_length = max(len(task[3]) for task in user_tasks) if user_tasks else 8
    comp_length = max(len(task[4]) for task in user_tasks) if user_tasks else 9

    header = f"{'ID':<3} {'User':<{user_length}} {'Title':<{title_length}} {'Description':<{desc_length}} {'Due Date':<{due_length}} {'Completed':<{comp_length}}"
    print(header)
    print('-' * len(header))

    for i, task in enumerate(user_tasks, 1):
        user, title, description, due_date, completed = task
        print(f"{i:<3} {user:<{user_length}} {title:<{title_length}} {description:<{desc_length}} {due_date:<{due_length}} {completed:<{comp_length}}")

    # Allow user to select a task to edit or mark as complete
    task_number = int(input("Enter task number to edit or mark as complete, or -1 to return: "))
    if task_number == -1:
        return
    if 1 <= task_number <= len(user_tasks):
        selected_task = user_tasks[task_number - 1]
        edit_task(selected_task)  # Call the edit_task function
        save_tasks(tasks)  # Save the changes
    else:
        print("Invalid task number.")

def display_statistics(users, tasks):
    # Always generate fresh reports before displaying statistics
    generate_reports(users, tasks)

    # Display the contents of the report files
    print("\nTask Overview:")
    with open("task_overview.txt", "r") as file:
        print(file.read())

    print("User Overview:")
    with open("user_overview.txt", "r") as file:
        print(file.read())
        

def generate_reports(users, tasks):
    # Calculate task report details
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task[4] == "Yes")
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in tasks if task[4] == "No" and datetime.strptime(task[3], DATETIME_STRING_FORMAT) < datetime.now())

    # Write task overview report
    with open("task_overview.txt", "w") as task_file:
        task_file.write(f"Total number of tasks: {total_tasks}\n")
        task_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        task_file.write(f"Total number of incomplete tasks: {incomplete_tasks}\n")
        task_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        task_file.write(f"Percentage of tasks incomplete: {incomplete_tasks/total_tasks:.2%}\n")
        task_file.write(f"Percentage of tasks overdue: {overdue_tasks/total_tasks:.2%}\n")

    # Write user overview report
    with open("user_overview.txt", "w") as user_file:
        user_file.write(f"Total number of users: {len(users)}\n")
        for user in users:
            user_tasks = [task for task in tasks if task[0] == user]
            tasks_completed = sum(1 for task in user_tasks if task[4] == "Yes")
            user_file.write(f"\nUser: {user}\n")
            user_file.write(f"Total tasks assigned: {len(user_tasks)}\n")
            user_file.write(f"Percentage of tasks completed: {tasks_completed/len(user_tasks):.2%}\n") if user_tasks else user_file.write("Percentage of tasks completed: N/A\n")

    print("Reports generated successfully.")


# Main program starts here
users = load_users()
tasks = load_tasks()

# Login functionality
logged_in_user = None
while not logged_in_user:
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username] == password:
        logged_in_user = username
        print("Login successful!")
    else:
        print("Invalid username or password.")

# Main menu loop
while True:
    print("\nPlease select one of the following options:")
    if logged_in_user == "admin":
        # Admin-specific options
        print("gr - Generate reports")
        print("ds - Display statistics")
        print("r - Register user")
        print("a - Add task")
        print("va - View all tasks")
    print("vm - View my tasks")  # This option should be available to all users
    print("e - Exit")
    
    option = input(": ").lower()    

    # Now handle the input based on the user type
    if option == "r" and logged_in_user == "admin":
        reg_user(users)
    elif option == "a" and logged_in_user == "admin":
        add_task(tasks)
    elif option == "va" and logged_in_user == "admin":
        view_all(tasks)
    elif option == "vm":
        view_mine(tasks, logged_in_user)
    elif option == "gr" and logged_in_user == "admin":
        generate_reports(users, tasks)
    elif option == "ds" and logged_in_user == "admin":
        display_statistics(users, tasks)
    elif option == "e":
        print("Goodbye!")
        break
    else:
        print("Invalid option, please try again.")
