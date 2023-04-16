# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component

    task_components = t_str.split(";")
    curr_t['id'] = task_components[0]  # Added a unique ID for each task
    curr_t['username'] = task_components[1]
    curr_t['title'] = task_components[2]
    curr_t['description'] = task_components[3]
    curr_t['due_date'] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(
        task_components[5], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[6] == "Yes" else False

    task_list.append(curr_t)


# ====Login Section====
'''This code reads usernames and password from the user.txt file to
    allow a user to login.
'''
# If no user.txt file, write one with a default acuser_tasks
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password


# Function to register new user
def reg_user():
    while True:
        # get new username and check if it doesn't already exist. print error message if it does
        new_username = input('\nNew Username: ')
        with open('user.txt', 'r') as user_file:
            user_data = user_file.readlines()
            usernames = [user.split(';')[0] for user in user_data]
            if new_username in usernames:
                print('Username already exists. Choose a different username.')
                continue

        # get new users password
        new_password = input('New password: ')
        # get password confirmation
        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            break

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")


# function to add task
def add_task(id, task_username, task_title, task_description, task_due_date):
    # Current date.
    curr_date = date.today()

    # Add the data provided to the file task.txt and
    # Include 'No' to indicate if that the task is not complete.
    # Also added a unique ID to identify each task

    task_id = str(len(open('tasks.txt').readlines()) + 1)
    new_task = {
        "id": task_id,
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['id'],
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")
    return


# function to view all task
def view_all():
    for t in task_list:
        disp_str = f"\nTask ID: \t {t['id']}\n"
        disp_str += f"Task Title: \t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


# function to view all of the current users task
def view_mine():
    # display all of current users tasks in a readable format
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"\nTask ID:\t {t['id']}\n"
            disp_str += f"Task title:\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    # Ask user to view specif task (or enter '-1' to return to main menu)
    while True:
        try:
            view = int(
                input('Enter task ID to view specific task (or -1 to return to main menu): '))
            if view == -1:
                return
        except ValueError:
            print('Invalid input! Enter a numeric value.')
            continue

        for t in task_list:
            if t['id'] == str(view):
                disp_str = f"\nTask ID:\t {t['id']}\n"
                disp_str += f"Task title:\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)

        # give the user the option to mark specified task as completed or edit task
        command = input(
            'Mark task as complete or edit task? (complete/edit): ').lower()

        # ----- mark task as completed
        if command == 'complete' or command == 'c':
            for t in task_list:
                if t['id'] == str(view) and t['completed'] == False:
                    t['completed'] = True
                else:
                    print('Task already completed!')
                    return

            with open('tasks.txt', 'w') as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [t['id'],
                                 t['username'],
                                 t['title'],
                                 t['description'],
                                 t['due_date'].strftime(
                                     DATETIME_STRING_FORMAT),
                                 t['assigned_date'].strftime(
                                     DATETIME_STRING_FORMAT),
                                 "Yes" if t['completed'] else "No"]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))

            print("Task marked as complete!")
            return

        # ---- edit task
        # - take in new task details and update 'task.txt' file if file is not already completed
        elif command == 'edit' or command == 'e':
            for t in task_list:
                # check if the task is not already completed then let user edit task
                if t['username'] == curr_user and t['id'] == str(view) and t['completed'] == False:
                    while True:
                        # take new new username for task and check if it exists
                        new_user_task = input(
                            'Enter username you wish to assign task to: ').lower()
                        if new_user_task not in username_password.keys():
                            print(
                                "User does not exist. Please enter a valid username")
                            continue
                        else:
                            break
                        # take in new due date for task in correct format
                    while True:
                        try:
                            new_task_due_date = input(
                                "Due date of task (YYYY-MM-DD): ")
                            datetime.strptime(new_task_due_date,
                                              DATETIME_STRING_FORMAT)
                            break
                        except ValueError:
                            print(
                                "Invalid datetime format. Please use the format specified")

                    # update task details in text.txt file
                    with open("tasks.txt", "r+") as file:
                        tasks_data = file.readlines()
                        tasks_data_updated = []
                        for t in tasks_data:
                            if t[0] == str(view):
                                new_t = t.split(';')
                                new_t[1] = new_user_task
                                new_t[4] = new_task_due_date
                                new_t = ';'.join(new_t)
                                t = new_t
                            tasks_data_updated.append(t)

                        file.seek(0)
                        file.writelines(tasks_data_updated)
                        print('task updated!\n')
                        return

                # print message letting the user know the task is already complete
                elif t['username'] == curr_user and t['id'] == str(view) and t['completed'] == True:
                    print('Task already completed!\n')

        # return to main menu
        elif view == -1:
            return

        else:
            print('Invalid input!')
            return


def generate_reports():
    # ----- generate task report and output data
    # total amount of tasks
    total_tasks = len(task_list)
    # amount of completed tasks
    completed_tasks = 0
    for t in task_list:
        if t['completed']:
            completed_tasks += 1
    # amount of uncompleted tasks
    uncompleted_tasks = 0
    for t in task_list:
        if t['completed'] == False:
            uncompleted_tasks += 1
    # amount of tasks that haven't been completed and are overdue
    overdue_tasks = 0
    for t in task_list:
        if t['due_date'] < datetime.today() and t['completed'] == False:
            overdue_tasks += 1
    # percentage of uncompleted tasks
    uncompleted_tasks_percentage = round(
        (uncompleted_tasks / total_tasks) * 100, 2)
    # percentage of overdue tasks
    overdue_tasks_percentage = round(
        (overdue_tasks / total_tasks) * 100, 2)
    # generate 'task_overview.txt' file and output data in readable format
    with open('task_overview.txt', 'w') as t_overview_file:
        t_overview_file.write(f'''Total number of tasks: {total_tasks}
Total number of completed tasks: {completed_tasks}
Total number of uncompleted tasks: {uncompleted_tasks}
Total number of overdue tasks: {overdue_tasks}
Percentage of tasks incomplete:{uncompleted_tasks_percentage}%
Percentage of overdue tasks: {overdue_tasks_percentage}%''')

    # -- generate 'user_overview' file output data
    with open('user_overview.txt', 'w') as user_file:
        # display total amount of users
        total_users = len(username_password)
        user_file.write(f'Total number of users: {total_users}\n')

        # display total number of tasks
        user_file.write(f'Total number of tasks: {len(task_list)}\n\n')

        # display each users report in a readable format.
        for user in username_password:
            # total number of tasks assigned to user
            user_tasks = 0
            for t in task_list:
                if user == t['username']:
                    user_tasks += 1

            # percentage of total tasks assigned to user
            user_tasks_perc = round((user_tasks / len(task_list)) * 100, 2)

            # percentage of tasks assigned to user that have been completed
            completed_tasks = 0
            for t in task_list:
                if t['username'] == user and t['completed']:
                    completed_tasks += 1
                # try incase user has 0 tasks completed
                try:
                    user_completed_tasks_perc = round(
                        (completed_tasks / user_tasks) * 100, 2)
                except ZeroDivisionError:
                    user_completed_tasks_perc = 0

            # percentage of tasks assigned to user that have not been completed
            uncompleted_tasks = 0
            for t in task_list:
                if t['username'] == user and t['completed'] == False:
                    uncompleted_tasks += 1
                # try incase user has 0 tasks uncompleted
                try:
                    user_uncompleted_tasks_perc = round(
                        (uncompleted_tasks / user_tasks) * 100, 2)
                except ZeroDivisionError:
                    user_uncompleted_tasks_perc = 0

            # percentage of tasks assigned to user that are overdue
            user_overdue_tasks = 0
            for t in task_list:
                if t['username'] == user and t['due_date'] < datetime.today() and t['completed'] == False:
                    user_overdue_tasks += 1
                # try incase user has 0 tasks overdue
                try:
                    user_overdue_tasks_perc = round(
                        (user_overdue_tasks / user_tasks) * 100, 2)
                except ZeroDivisionError:
                    user_overdue_tasks_perc = 0

            user_file.write(f'''\nUsername: {user}
Tasks assigned to user: {user_tasks}
Percentage of tasks assigned to user: {user_tasks_perc}%
Percentage of completed tasks assigned to user: {user_completed_tasks_perc}%
Percentage of uncompleted tasks assigned to user: {user_uncompleted_tasks_perc}%
Percentage of overdue tasks assigned to user: {user_overdue_tasks_perc}%\n''')

    print('Task reports and user reports generated.')


def display_stats():
    while True:
        try:
            task_file = open('task_overview.txt')
            print('\nTasks report:')
            print(task_file.read())
            task_file.close()
            break
        except FileNotFoundError:
            generate_reports()
            continue
    while True:
        try:
            user_file = open('user_overview.txt')
            print('\nUser reports:')
            print(''.join(user_file.readlines()[4:]))

            user_file.close()
            break
        except FileNotFoundError:
            generate_reports()
            continue


logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate Reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            break
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(
                    task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        add_task(id, task_username, task_title,
                 task_description, task_due_date)

    elif menu == 'va':
        # Reads all the tasks from task.txt file and prints to the console in the format of Output 2 presented in the task pdf (i.e. includes spacing and labelling
        view_all()

    elif menu == 'vm':
        # Reads all the current users tasks from task.txt file and prints to the console in the format of Output 2 presented in the task pdf (i.e. includes spacing and labelling
        view_mine()

    elif menu == 'gr':
        # Generates all task reports file and each user reports file ('task_overview.txt' and 'user_overview.txt')
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin':
        # If the user is an admin they can display statistics about all users and tasks
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")
        display_stats()

    elif menu == 'ds' and curr_user != 'admin':
        print('You need to be logged in as admin to display stats.')

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
