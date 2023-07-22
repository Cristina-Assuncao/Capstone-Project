# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
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
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    # curr_t['completed'] = 'Yes' if task_components[5] == 'Yes' else 'No'

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
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

# Log in
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
        print("Login successful!")
        logged_in = True

#____________________________ MODIFIED CODE STARTS HERE ___________________________

# Function to register a new user and add it to user.txt
def reg_user():
    # - Request input of a new username
    new_username = input("New Username: ")
    while new_username in username_password.keys():
        print("  That username is already in use! Please chose another.")
        new_username = input("New Username: ")
    # - Request input of a new password
    new_password = input("New Password: ")
    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")
    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password  
        with open("user.txt", "w") as out_file:
            user_data = []
            for new_user in username_password:
                user_data.append(f"{new_user};{username_password[new_user]}")
            out_file.write("\n".join(user_data))
    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")

# Function to add a new task to task.txt
def add_task():
    '''Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        task_username = input("Name of person assigned to task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
        # "completed": 'No'
    }
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
                # "No" if t['completed'] else "Yes"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to read all tasks from task.txt and print them in the console in the format of Output 2 i.e. including spacing and labelling
def view_all():
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Complete? \t {t['completed']}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to read the tasks from task.txt of the current user with added functionality of numbered tasks, possibility to edit or mark as read
def view_mine():
    # New list with the tasks of the current user only
    new_task_list = []

    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task:\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Complete? \t {t['completed']}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            new_task_list.append(disp_str)

    # Enumerates the tasks of current user only
    numbered_tasks = dict(enumerate(new_task_list, 1))

    for number, specific_task in numbered_tasks.items():
        print(f"{number}\n{specific_task}")
    
    # Gives the total count of tasks the current user has
    count = 0
    for specific_task in new_task_list:
        count +=1

    # User can choose specific task
    # If user has no tasks:
    if new_task_list == []:
        print("You have no tasks.")
    # If user has task(s):
    try:
        choose_task = int(input(f'''You have {count} tasks.
        Select a task         - enter the task no.
        Exit to the main menu - enter -1
        : '''))
        if choose_task in numbered_tasks:
            # choose_task                   number of the task that the user chooses to modify
            # numbered_tasks                all tasks from current user with numbers unedited
            # numbered_tasks[choose_task]   task chosen by the user edited without the number
            print(f"\nYou've chosen task no. {choose_task}\n{numbered_tasks[choose_task]}")
            task_change = input('''Would you like to:
        m  - Mark the task as complete
        ed - Edit the task
        : ''')
            # Change 'No' to 'Yes'
            if task_change == 'm':
                with open("tasks.txt", "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    count = 0
                    for i, line in enumerate(lines):
                        task_split = line.split(";")
                        if task_split[0] == curr_user:
                            count +=1
                            if count == choose_task:
                                new_line = line.replace(";No", ";Yes")
                                lines[i] = new_line
                                file.writelines(lines)
                                file.truncate()
                print(f"\nTask {choose_task} is marked has completed!")

            # Edit the task: with option of either assign a new user or change the due date
            elif task_change == 'ed':
                # Verify if task is complete: "Yes" or "No"
                with open("tasks.txt", "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    count = 0
                    for i, line in enumerate(lines):
                        # removes newline '\n'
                        task_strip = line.strip()
                        # splits by the symbol ';'
                        task_split = task_strip.split(";")
                        if task_split[0] == curr_user:
                            count += 1
                            if count == choose_task:
                                if task_split[5] == "No":
                                    edit_task = input('''\nNow, would you like to:
        u - Assign a new username
        d - Change the due date
        : ''')
                                    # Assign new user
                                    if edit_task == 'u':
                                        new_user = input("Write the username you want the task to be reassigned to: ")
                                        new_line = line.replace(curr_user, new_user)
                                        lines[i] = new_line
                                        print("\nUsername was succefully reassigned.")
                                        file.writelines(lines)
                                        file.truncate()

                                    # Change the due date    
                                    elif edit_task =='d':
                                        # Check if datetime format is correct
                                        while True:
                                                try:
                                                    new_due_date = input("Write the new due date: (YYYY-MM-DD): ")
                                                    new_due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                                    break
                                                except ValueError:
                                                    print("\nInvalid datetime format. Please use the format specified.\n")
                                        new_line = line.replace(task_split[3], new_due_date)
                                        lines[i] = new_line
                                        file.writelines(lines)
                                        file.truncate()
                                        print("\nDue date has been succefully changed.")
                                    else:
                                        print("5CHECK: You have made a wrong choice, please try again.")
                                        
                                elif task_split[5] == "Yes":
                                    print("\nThis task cannot be edited because it was completed.")
                                else:
                                    print("You have made a wrong choice, please try again.")
            else:
                print("You have made a wrong choice, please try again.")
        elif choose_task == -1:
            menu()
        else:
            print("You have made a wrong choice, please try again.")
    except:
        print("You have made a wrong choice, please try again.")

# Function to generate reports
def generate_reports(task_list):

    # Generate task overview report
    # total number of tasks
    total_tasks = len(task_list)

    # get() returns the value of a key if it is present in a dict
    # 'completed' is returned if it is present, otherwise defaults to False
    # sum() is the sum of all values
    completed_tasks = sum(task.get('completed', False) for task in task_list)

    incomplete_tasks = total_tasks - completed_tasks

    # for each task 2 conditions are checked; if it has not been completed and if due date is before today
    # if both conditions are met 1 id generated
    # sum() adds the generated value
    overdue_tasks = sum(1 for task in task_list if not task.get('completed', False) and task['due_date'] < datetime.now())

    completed_tasks_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    incomplete_tasks_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # task report string - different parts of the report are concatenated to task report string
    task_report = f"------- Task Overview -------\n\n"
    task_report += f"Total tasks: {total_tasks}\n"
    task_report += f"Completed tasks: {completed_tasks}\n"
    task_report += f"Incompleted tasks: {incomplete_tasks}\n"
    task_report += f"Overdue tasks: {overdue_tasks}\n"
    # .2f formats floating numbers with 2 decimal places
    task_report += f"Percentage of completed tasks: ({completed_tasks_percentage:.2f}%)\n"
    task_report += f"Percentage of incomplete tasks: ({incomplete_tasks_percentage:.2f}%)\n"

    # Write task report to task_overview file
    with open("task_overview.txt", "w") as file:
        file.write(task_report)


    # Generate user overview report
    # length of username_password dict
    total_users = len(username_password)

    # user report string
    user_report = f"------- User Overview -------\n\n"
    user_report += f"Total users: {total_users}\n"
    user_report += f"Total tasks generated: {total_tasks}\n"

    # calculate total tasks assigned to each user
    # dict to store statistics for each user
    tasks_assigned_to_user = {}

    # iterate over task list
    for task in task_list:
        assigned_user = task.get('username')

        # if user is in the tasks_assigned_to_user dict -> tasks that have already been assigned to that user
        if assigned_user in tasks_assigned_to_user:
            # increment count by 1
            tasks_assigned_to_user[assigned_user]['total_tasks'] += 1
        else:
            # create a new entry in the dict, add user to dict and create a dict for that user
            # dict keys and values
            # total_tasks = 1
            # completed tasks = 0
            # overdue tasks = 0
            tasks_assigned_to_user[assigned_user] = {'total_tasks': 1, 'completed_tasks': 0, 'overdue_tasks': 0}

        # if the task is completed
        if task.get('completed', False):
            # increment completed tasks by 1
            tasks_assigned_to_user[assigned_user]['completed_tasks'] += 1

        # if task is not completed and due date is earlier than current date
        if not task.get('completed', False) and task['due_date'] < datetime.now():
            # increment overdue task by 1
            tasks_assigned_to_user[assigned_user]['overdue_tasks'] += 1

    # add user-specific information to the user report
    user_report += "\nUser-specific task statistics:\n"

    # items() returns key:value tuple
    # user is the username
    # task_stats returns the dict which contains the different tasks statistics of the user
    for user, task_stats in tasks_assigned_to_user.items():
        user_total_tasks = task_stats['total_tasks']
        completed_tasks = task_stats['completed_tasks']
        overdue_tasks = task_stats['overdue_tasks']
        # percentage of user's total tasks compared with the total tasks
        tasks_assigned_percentage = (user_total_tasks / total_tasks) * 100
        # percentage of user's completed tasks compared with their total tasks
        tasks_completed_percentage = (completed_tasks / user_total_tasks) * 100
        # percentage of user's incomplete tasks compared with their total tasks
        tasks_incomplete_percentage = ((user_total_tasks - completed_tasks) / user_total_tasks) * 100
        # percentage of user's overdue tasks
        tasks_overdue_percentage = (overdue_tasks / user_total_tasks) * 100

        # concatenate different user statistics to user report string
        user_report += f"\nUser: {user}\n"
        # .2f floating-point numbers with 2 decimal places
        user_report += f"Total tasks assigned: {user_total_tasks} ({tasks_assigned_percentage:.2f}%)\n"
        user_report += f"Tasks completed: {completed_tasks} ({tasks_completed_percentage:.2f}%)\n"
        user_report += f"Tasks incomplete: {user_total_tasks - completed_tasks} ({tasks_incomplete_percentage:.2f}%)\n"
        user_report += f"Tasks incomplete and overdue: {overdue_tasks} ({tasks_overdue_percentage:.2f}%)\n"

    # Write task report to task_overview file
    with open("user_overview.txt", "w") as file:
        file.write(user_report)

    print("\nTask and User reports have been succefully generated.\n")
    return

# Function to display statistics
def display_statistics():
    # If the user is the admin they can read from task_overview.txt and user_overview.txt
    # If reports were not yet generated the function to generated is called

    if not os.path.exists('task_overview.txt'):
        generate_reports(task_list)

    task = open('task_overview.txt', 'r')
    print(task.read())
    task.close()

    if not os.path.exists('user_overview.txt'):
        generate_reports(task_list)

    user = open('user_overview.txt', 'r')
    print(user.read())
    user.close()

# Menu
def menu():
    while True:
        # presenting the menu to the user and making sure that the user input is converted to lower case
        print()
        menu = input('''Select one of the following options below:
    r  - Registering a user
    a  - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e  - Exit
    : ''').lower()

        if menu == 'r':
            reg_user()

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()
        
        elif menu == 'vm':
            view_mine()
        
        elif menu == 'gr':
            if curr_user == 'admin':
                generate_reports(task_list)
            else:
                print("Sorry, only an admin can generate reports.")
                    
        elif menu == 'ds':
            if curr_user == 'admin':
                display_statistics()
            else:
                print("Sorry, only an admin can display statistics.")
        
              
        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, please try again.")

menu()