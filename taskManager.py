# For this capstone project, I will be modifiying an existing
# 'task manager' file to extend its functionality.

# =====================================================================
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"
# Creating functions for text styling methods
GREEN_START = '\033[32;1m'
GREEN_BANNER_START = '\033[42;30;1m'
RED_START = '\033[31;1m'
BOLD_TEXT = '\033[1m'
COLOUR_END = '\033[0m'

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", 'w') as default_file:
        pass


with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}
        
    # Split by semicolon and manually add each component into a dict
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], 
    DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], 
    DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


'''This code reads usernames and password from the user.txt file to 
allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", 'w') as default_file:
        default_file.write("admin;password")
            
# Read in user_data
with open("user.txt", 'r') as user_file: 
    user_data = user_file.read().split("\n") 


# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password  

        
# ====================== def functions ======================
def login():
    """
    Prompts the user to enter a username and password, checks if the 
    user exists and the password is correct. Allows access upon
    successful login.
    
    Returns:
        'display_menu()' function.
    """
    logged_in = False
    while not logged_in:

        print(f"{GREEN_BANNER_START}===================== LOGIN ====================={COLOUR_END}")
        global current_user
        current_user = input(f"{GREEN_START}Username: {COLOUR_END}")
        if current_user not in username_password.keys():
            print(f"{RED_START}User does not exist{COLOUR_END}")
        elif current_user in username_password.keys():
            curr_pass = input(f"{GREEN_START}Password: {COLOUR_END}")
            if username_password[current_user] != curr_pass:
                print(f"{RED_START}Wrong password{COLOUR_END}")
            else:
                print(f"\n{GREEN_BANNER_START}Login Successful!{COLOUR_END}")
                logged_in = True       
    return display_menu()


def reg_user():
    """
    Registers a new user by prompting for a unique username and 
    password, checking for existing usernames, and storing the user
    data in the 'user.txt' file if the new user is successfully
    registered.
    
    Returns:
        'display_menu()' function.
    """
    print(f"{GREEN_BANNER_START}===================== REGISTER ====================={COLOUR_END}")
    global current_user
    new_user = False
    while not new_user:
        new_username = input(f"{GREEN_START}New Username: {COLOUR_END}")
        
        if new_username in username_password.keys():
            print(f"{RED_START}This username already exists! Please try again.{COLOUR_END}")
            return reg_user()

        confirm_username = input(f"{GREEN_START}Confirm Username: {COLOUR_END}")
        if new_username != confirm_username:
            print(f"{RED_START}Usernames do not match! Please try again.{COLOUR_END}")
            return reg_user()
        else: 
            new_pass = False
            while not new_pass:
                new_password = input(f"{GREEN_START}New Password: {COLOUR_END}")

                confirm_password = input(f"{GREEN_START}Confirm Password: {COLOUR_END}")

                if new_password != confirm_password:
                    print(f"{RED_START}Passwords do no match.{COLOUR_END}")
                    
                else:
                    print(f"\n{GREEN_BANNER_START}New user added!{COLOUR_END}")
                    new_pass = True
        new_user = True
        current_user = new_username
    username_password[current_user] = new_password
                
    with open("user.txt", 'w') as out_file:
        user_data = []
        for k in username_password:
            user_data.append(f"{k};{username_password[k]}")
        out_file.write("\n".join(user_data))
    return display_menu()    


def add_task():
    """
    Prompts the user to input task details, validates the input, adds
    the task to 'task_list', and writes the task data to the 'task.txt'
    file.
    
    Returns:
        'display_menu()' function.
    """
    task_username = input(f"{GREEN_START}Name of person assigned to task: {COLOUR_END}")
    if task_username not in username_password.keys():
        print(f"{RED_START}User does not exist. Please enter a valid username.{COLOUR_END}")
        return add_task()
    task_title = input(f"{GREEN_START}Title of Task: {COLOUR_END}")
    task_description = input(f"{GREEN_START}Description of Task: {COLOUR_END}")
    while True:
        try:
            task_due_date = input(f"{GREEN_START}Due date of task (YYYY-MM-DD): {COLOUR_END}")
            due_date_time = datetime.strptime(task_due_date, 
            DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print(f"{RED_START}Invalid datetime format. Please use the format specified.{COLOUR_END}")


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
        }

    task_list.append(new_task)
    with open("tasks.txt", 'w') as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print(f"{GREEN_BANNER_START}Task successfully added!{COLOUR_END}")
    return display_menu()


def view_all():
    """
    Iterates through the 'task_list' and displays detailed information about
    each task in a formatted manner.
    Returns:
        'display_menu()' function.
    """
    for pos, t in enumerate(task_list, 1):
        disp_str = f"\n\n{GREEN_BANNER_START}Key\tTitle\t\tDetails{COLOUR_END}\n"
        disp_str += f" {GREEN_BANNER_START}{pos}{COLOUR_END}\t{GREEN_START}Task: {COLOUR_END}\t\t{t['title']}\n"
        disp_str += f"\t{GREEN_START}Assigned to: {COLOUR_END}\t{t['username']}\n"
        disp_str += f"\t{GREEN_START}Date Assigned: {COLOUR_END}\t{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"\t{GREEN_START}Due Date: {COLOUR_END}\t{t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"\t{GREEN_START}Task Description: {COLOUR_END}\n\t {t['description']}\n"
        print(disp_str)
    return display_menu()


def updating_task_txt(task_list: str):
    """
    Writes the updated 'task_list' to 'tasks.txt'. Each task in the 
    list is represented as a dictionary with keys 'username', 'title',
    'description', 'due_date', and 'assigned_date'.
    
    Args:
        task_list: A list of all tasks, seperated into their own 
        dictionaries.
    """
    with open("tasks.txt", 'w') as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
                ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
        

def complete_task(chosen_task: str, task: int) -> str:
    """
    Prompts the user to mark a specific task as complete or not, with
    appropriate messages and actions based on the user's input.
    
    Args:
        chosen_task: Chosen task selected by user to modify.
        task: Represents the task number. Used in prompts and display 
        messages to the user during the task completion process. 
    Returns:
        If 'chosen_task' is marked as complete, returns 'display_menu'
        function.
        If 'chosen_task' not marked as complete, returns
        'task_details(chosen_task, task)' function.
    """
    while True:
        complete = input(f"{GREEN_START}Would you like to mark Task {task} as complete? (Yes/No){COLOUR_END}").capitalize()
        if complete == 'Yes':
            if chosen_task ['completed']:
                print(f"\n{BOLD_TEXT}This task has already been marked as complete.{COLOUR_END}")
                return display_menu()
            else:
                chosen_task['completed'] = True
                updating_task_txt(task_list)
                print(f"\n{GREEN_BANNER_START}This task is now complete! Congratulations! :){COLOUR_END}")
                return display_menu()
        elif complete == 'No':
            print(f"\n{BOLD_TEXT}No changes have been made.{COLOUR_END}\n{GREEN_START}Returning to Task {task} details...{COLOUR_END}\n")
            return task_details(chosen_task, task)
        else:    
            print(f"{RED_START}Oopsie, that didn't quite work. Please enter either 'Yes' or 'No'.{COLOUR_END}")  


def edit_task(chosen_task: str, task: int) -> str:
    """
    This function first checks if the 'chosen_task' is marked as 
    complete. If the task is incomplete, this function allows users to
    edit specific details for 'chosen_task' such as username,
    assignment and due date, with error handling and user prompts.
    
    Args: 
        chosen_task: Chosen task selected by user to modify.
        task: Represents the task number. Used in display messages.
    Returns:
        'display_menu()' function.
    """
    if chosen_task['completed']:
        print(f"\n{RED_START}This task is marked as complete and cannot be edited.{COLOUR_END}\n{GREEN_START}Returning you to the main menu now\n...\n{COLOUR_END}")
        return display_menu()
    else:
        edit = False
        while not edit:
            editing_menu = input(f'''\n{GREEN_START}What would you like to edit?{COLOUR_END}
            {GREEN_START}u{COLOUR_END} - Username assigned to task {task}
            {GREEN_START}d{COLOUR_END} - Due date for task {task}
            {GREEN_START}m{COLOUR_END} - Return to the main menu
            {GREEN_START}->{COLOUR_END} ''').lower()
            if editing_menu == 'u':
                username = input(f"{GREEN_START}Please enter the username you wish to assign this task to\n-> {COLOUR_END}")
                if username not in username_password.keys():
                    print(f"{RED_START}Oopsie, this username does not exist. Please try again.{COLOUR_END}")
                else:
                    chosen_task['username'] = username
                    updating_task_txt(task_list)
                    print(f"{GREEN_BANNER_START}Username has been changed successfully!{COLOUR_END}")
                    edit = True
            elif editing_menu == 'd':
                try:
                    due_date = input(f"{GREEN_START}Please enter the new due date in the following format: YYYY-MM-DD\n-> {COLOUR_END}")
                    new_date = datetime.strptime(due_date, DATETIME_STRING_FORMAT)
                    chosen_task['due_date'] = new_date
                    updating_task_txt(task_list)
                    print(f"{GREEN_BANNER_START}The due date has been changed successfully!{COLOUR_END}")
                    edit = True
                except ValueError:
                    print(f"{RED_START}Oopsie, that date format doesn't seem right, please try again.{COLOUR_END}")
            elif editing_menu == 'm':
                return display_menu()
            else:
                print(f"\n{RED_START}Invalid option, please try again.{COLOUR_END}")
    return display_menu()


def task_details(chosen_task: str, task: int) -> str:
    """
    Displays details of a 'chosen_task' and provides options to mark 
    the task as complete, edit the task, or return to the main menu.
    
    Args:
        chosen_task: Chosen task selected by user to modify.
        task: Represents the task number. Used in display messages.
    Returns:
        If task_menu == 1: returns 'complete_task(chosen_task, task)' 
        function.
        If task_menu == 2: returns 'edit_task(chosen_task, task)' 
        function.
        If task_menu == 3: returns 'display_menu()' function.
    """
    disp_str = f"\n{GREEN_BANNER_START}=============== Task {task} Details ==============={COLOUR_END}\n\n"
    disp_str += f" \t{GREEN_START}Task:{COLOUR_END} \t\t {chosen_task['title']}\n"
    disp_str += f"\t{GREEN_START}Assigned to:{COLOUR_END} \t {chosen_task['username']}\n"
    disp_str += f"\t{GREEN_START}Date Assigned:{COLOUR_END} \t {chosen_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"\t{GREEN_START}Due Date:{COLOUR_END} \t {chosen_task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"\t{GREEN_START}Task Description:{COLOUR_END} \n\t {chosen_task['description']}\n"
    print(disp_str)
        
    while True:
        try:
            task_menu = int(input(f'''\n\n{GREEN_START}Please choose from the following options:{COLOUR_END}
        {GREEN_START}1{COLOUR_END} - Mark Task {task} as complete
        {GREEN_START}2{COLOUR_END} - Edit Task {task}
        {GREEN_START}3{COLOUR_END} - Return to the Main Menu
        {GREEN_START}-> {COLOUR_END}'''))
            if task_menu == 1:
                return complete_task(chosen_task, task)
            elif task_menu == 2:
                return edit_task(chosen_task, task)
            elif task_menu == 3:
                return display_menu()
            else:
                print(f"{RED_START}Invalid selection, please try again.{COLOUR_END}")   
        except ValueError:
            print(f"{RED_START}Oopsie, that was not a number, please try again.{COLOUR_END}") 


def selecting_a_task():
    """
    Prompts the user to either enter '-1' to return to the main menu, 
    or select a task number to view and only displays the task if it is
    assigned to that user.
    
    Returns:
        If user input == '-1': returns 'display_menu()' function.
        Else: uses the chosen task followed by its task number as 
        parameters when returning the 'task_details(chosen_task, task)'
        function.
    """
    selection = False
    while not selection: 
        try:
            for t in task_list:
                task = int(input(f"{GREEN_START}Please select the task number you would like to view or alternatively, enter '-1' to return to the main menu:\n-> {COLOUR_END}"))
                if 1 <= task <= len(task_list) and task_list[task - 1]['username'] == current_user:
                    chosen_task = task_list[task - 1]
                    return task_details(chosen_task, task)
                elif task == - 1:
                    return display_menu()
                else:
                    print(f"{RED_START}Invalid selection, please try again.{COLOUR_END}")
        except ValueError:
            print(f"{RED_START}Oopsie, that was not a number, please try again.{COLOUR_END}")


def view_mine():
    """
    Iterates through the 'task_list' to display tasks assigned to the
    current user in a formatted manner.
    
    Returns:
        If user has no tasks, returns 'display_menu()'.
        Else, returns 'selecting_a_task()' function.
    """
    user_task_count = 0
    for pos, t in enumerate(task_list, 1):
        if t['username'] == current_user:
            user_task_count +=1
            disp_str = f"\n\n{GREEN_START}Task {pos}:{COLOUR_END} \t {t['title']}\n"
            disp_str += f"{GREEN_START}Assigned to:{COLOUR_END} \t {t['username']}\n"
            disp_str += f"{GREEN_START}Date Assigned:{COLOUR_END} \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"{GREEN_START}Due Date:{COLOUR_END} \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"{GREEN_START}Task Description:{COLOUR_END} \n {t['description']}\n" 
            print(disp_str)
        
    if user_task_count == 0:
        print(f"\n{BOLD_TEXT}No tasks created.\nRedirecting you back to the main menu now\n...{COLOUR_END}")
        return display_menu()
    else:
        return selecting_a_task()


def generate_reports():
    """
    Generates 'task_overview.txt' and 'user_overview.txt' based on the
    provided 'task_list' and 'user_data'.
    
    Generates the following for 'task_overview' file:
        Total num of tasks tracked on task_manager.py.
        Completed tasks total.
        Uncompleted tasks total.
        Incomplete and overdue.
        Percentage of incomplete tasks.
        Percentage of tasks overdue.

    Generates the following for 'user_overview' file:
        Total num of users registered to task_manager.
        Total num of tasks that have been generated on task_manager.
            For each user:
                Total num of tasks assigned to user,
                Percentage or users tasks over total tasks,
                Percentage of users completed tasks,
                Percentage of incomplete tasks,
                Percentage of overdue tasks.
    
    Returns:
        'display_menu()' function.
    """
    # Gathering data for 'task_overview' file.
    curr_date = datetime.today()
    num_tasks = len(task_list)
    
    completed_task = 0
    uncompleted_task = 0
    for task in task_list:
        if not task['completed']:
            uncompleted_task += 1
        else:
            completed_task += 1

    overdue_task = 0
    for task in task_list:
        if not task['completed'] and task['due_date'] < curr_date:
            overdue_task += 1
    
    incomplete_task_percent = round((uncompleted_task / num_tasks) *100, 2)
    overdue_task_percent = round((overdue_task / num_tasks) * 100, 2)

    task_overview = ("\tTask Overview\n\n")
    task_overview += (f"Number of Tasks: {num_tasks}\n")
    task_overview += (f"Completed Tasks: {completed_task}\n")
    task_overview += (f"Uncompleted Tasks: {uncompleted_task}\n")
    task_overview += (f"Incomplete Tasks Percentage: {incomplete_task_percent}%\n")
    task_overview += (f"Overdue Tasks: {overdue_task}\n")
    task_overview += (f"Overdue Tasks Percentage: {overdue_task_percent}%\n")
    
    with open("task_overview.txt", 'w') as overview_file:
        overview_file.write(task_overview)
    
    
    # Gathering data for 'user_overview' file.
    num_users = len(username_password.keys())
    
    with open("user_overview.txt", 'w') as overview_file:
        user_overview = ("\n\tUser Overview\n\n")
        user_overview += (f"Number of Users: {num_users}\n")
        user_overview += (f"Number of Tasks: {num_tasks}\n") 
        overview_file.write(user_overview)
        
        for user in username_password:
            user_tasks = 0
            completed = 0
            incompleted = 0
            for task in task_list:
                if task['username'] == user:
                    user_tasks += 1
                    if not task['completed']:
                        incompleted += 1
                    else:
                        completed += 1
                        
            overdue = 0 
            for task in task_list:
                if task['username'] == user:
                    if not task['completed'] and task['due_date'] < curr_date:
                        overdue += 1

            user_tasks_percent = f"{round((user_tasks / num_tasks) *100, 2)}%"
            if user_tasks != 0:
                complete_percent = f"{round((completed / user_tasks) *100, 2)}%"
                incompleted_percent = f"{round((incompleted / user_tasks) *100, 2)}%"
                overdue_percent = f"{round((overdue / user_tasks) *100, 2)}%"
            else:
                complete_percent = "0%"
                incompleted_percent = "0%"
                overdue_percent = "0%"

            user_details = (f"\n\t{user}'s Details\n\n")
            user_details += (f"Number of User Tasks: {user_tasks}\n")
            user_details += (f"Percentage of User Tasks out of Total Tasks: {user_tasks_percent}\n")
            user_details += (f"Percentage of Completed Tasks: {complete_percent}\n")
            user_details += (f"Percentage of Incompleted Tasks: {incompleted_percent}\n")
            user_details += (f"Percentage of Overdue Tasks: {overdue_percent}\n")      
            overview_file.write(user_details)

    print(f"{GREEN_BANNER_START}Reports have been generated!{COLOUR_END}")
    return display_menu()


def display_statistics():
    """
    Checks if the current user is an admin, generates reports if 
    necessary, and displays statistics from files if the user is an 
    admin. Prints an appropriate error message if user != 'admin'.
    
    Returns:
        'display_menu()' function
    """
    if current_user == 'admin':
        if (os.path.exists("./task_overview.txt") == False) or (os.path.exists("./user_overview.txt") == False):
            generate_reports()

        with open("task_overview.txt", 'r') as file:
            for line in file:
                    print(line, end = '')

        with open("user_overview.txt", 'r') as file:
            for line in file:
                print(line, end = '')
    else:
        print(f"\n{RED_START}Oopsie, as a non-admin member, you don't have access to the statistics.\n\nPlease allow us to redirect you.\n...{COLOUR_END}")
    return display_menu()


def display_menu():
    """
    Presents a menu of options for the user to interact with a task
    management system. Prints an appropriate error message if an 
    invalid choice has been made. Exits program if 'e' is selected.

    Returns: 
        Based on users input, returns either 'add_task()', 
        'view_all()', 'view_mine()', 'generate_reports()', or
        'display_statistics()' function.
    """
    while True:
        print(f"\n{GREEN_START}Hello {current_user}!{COLOUR_END}\n")  
        menu = input(f'''{GREEN_START}How can we help you today:{COLOUR_END}
        {GREEN_START}a{COLOUR_END} - Adding a task
        {GREEN_START}va{COLOUR_END} - View all task(s)
        {GREEN_START}vm{COLOUR_END} - View my task(s)
        {GREEN_START}gr{COLOUR_END} - generate reports
        {GREEN_START}ds{COLOUR_END} - Display statistics (for admins only)
        {GREEN_START}e{COLOUR_END} - Exit
        {GREEN_START}-> {COLOUR_END}''').lower()
                
        if menu == 'a':
            return add_task()

        elif menu == 'va':
            return view_all()
                
        elif menu == 'vm':
            return view_mine()
                
        elif menu == 'gr':
            return generate_reports()
            
        elif menu == 'ds':
            return display_statistics() 

        elif menu == 'e':
            print(f"{GREEN_BANNER_START}==========Thank you for using our services. See you again soon!=========={COLOUR_END}")
            exit()

        else:
            print(f"{RED_START}You have made a wrong choice, Please Try again.{COLOUR_END}")    


# All of the above functions can be placed in another file. Then we
# would say: 'from file_name import (followed by the name of all the
# functions you wish to use)'.


def main():
    """
    Presents a task manager interface with options to log in, register
    a user, or exit.
    """
    print()
    print(f"{GREEN_BANNER_START}===================== Hello, Welcome to Task Manager! ====================={COLOUR_END}\n\n")
        
    while True:
        start = input(f'''{GREEN_START}Please choose from the following options:{COLOUR_END}
        {GREEN_START}l{COLOUR_END} - Log in
        {GREEN_START}r{COLOUR_END} - Registering a user
        {GREEN_START}e{COLOUR_END} - Exit
        {GREEN_START}-> {COLOUR_END}''').lower()
            
        if start == 'l':
            login()
                
        elif start == 'r':
            reg_user()
        
        elif start == 'e':
            print(f"{GREEN_BANNER_START}==========Thank you for using our services. See you again soon!=========={COLOUR_END}")
            exit()
        else:
            print("Invalid option, Please Try again")           


# If we are importing this document, it is imperative to place the main
# body within a function to avoid printing it all in the imported files
# terminal.
# We specify this file as the main file by writting the following code:
if __name__ == "__main__":
    main()
# We do not need this if we specify "from 'file' import x y z" when
# importing. 
    