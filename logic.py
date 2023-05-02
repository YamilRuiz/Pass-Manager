# Yamil Ruiz
# Final Project
# Due Date: 03/03/2023

from database import *
from passwordLogic import password_generator
from colorama import Fore, Style
import sys

""" Need to work adding the delete and add option and selection 2/272023"""
verified_username = ""


def add_app():
    user = input("Please enter your username again:")
    app = input("Enter name of app to be added: ")
    if verified_username != user:
        print("Operation Denied incorrect username: Redirecting to Login")
        display()
    try:
        add_app_password(user, app)
    except Exception as e:
        print(e)
        display()
    else:
        print("App Added")
        display()


# Will add an application to the list
def update_app():
    user = input("Please enter your username again:  ")
    app = input("Enter app to be updated must patch from current list: ")
    if verified_username != user:
        print("Operation Denied incorrect username: Redirecting to Login")
        main()
    try:
        user_app_update(user, app)
    except Exception as e:
        print(e)
        display()
    else:
        print("Password Added")
        display()


# Delete an application for list


def delete_app():
    user = input("Please enter your username again:  ")
    app = input("Enter app to be deleted must match from current list: ")
    if verified_username != user:
        print("Operation Denied incorrect username: Redirecting to Login")
        main()
    try:
        delete_app_password(user, app)
    except Exception as e:
        print(e)
    else:
        print("App Deleted")
        display()


def display():
    data = user_info(verified_username)
    print("Your Application Passwords are:   \n")
    for x, y in data['user_apps'].items():
        print(Fore.RED + "Application:  " + x, " Password:  " + y)
        print(Style.RESET_ALL)
    input_test_b()




def register():
    """ No Regex will be added for simplicity """
    print("Please register to create account")
    user_name = input("Please enter your new username:  ")
    user_password = str(input("Please enter your desired password:  "))
    user_password = user_password.encode('utf-8')
    hashed = bcrypt.hashpw(user_password, bcrypt.gensalt(10))
    user_email = input("Please enter your email (ex: john@company.com:  ")
    User = {
        "username": user_name,
        "password": hashed,
        "email": user_email,
        "passcode": '',
        "user_apps": {
            "app1": password_generator(),
            "app2": password_generator()
        }
    }
    try:
        insert_collection(User)
    except Exception as e:
        print("Insert Error" + str(e))
        main()
    else:
        c = user_name
        print(c + " User was registered!! Redirecting to Login.")
        login()


def passcode_check():
    print("\nPlease check your email. Passcode was sent to the registered email\n"
          "Email sender name: pymanager@gmail.com")
    input_passcode = input("\nPlease input sent passcode:  ")
    user = verified_username
    try:
        passcode_checker(user, int(input_passcode))
    except Exception as e:
        print("\nPasscode did not match" + str(e))
        login()
    else:
        display()


# Password input should be masked but pycharm config is need to get getpass to work
def login():
    print("You are at Login page\n")
    username = input("\nPlease enter your username  ")
    user_check = user_search_login(username)
    if user_check:
        print("User found")
        password = input("\nPlease enter your password  ")  # Pycham does not work with modules to hide input
        try:
            user_login(username, password)
        except Exception:
            print("Please check your password ")
            login()
        else:
            global verified_username
            verified_username = username
            passcode_check()
    else:
        print("\nIncorrect username")
        main()
# Test user Option for Dialog box

def input_test_b():
    print("Please select\n"
              "Update Password : 1\n"
              "Delete Application: 2\n"
              "Add Application:  3\n"
              "Exit Application: 4\n")
    # I was unable to create a timeout function, instead a hard coded exit was created.
    # Attempted with sys.stdin and inputimeout
    a = input("Your Selection: ")
    if int(a) == 1:
        update_app()
    elif int(a) == 2:
        delete_app()
    elif int(a) == 3:
        add_app()
    elif int(a) == 4:
        print("Closing Application Bye!!")
        sys.exit()
    else:
        print("Incorrect option selected")
        display()



# Test for user input
def input_test(a):
    if a == str(1):
        login()
    elif a == str(2):
        register()
    else:
        print("Incorrect option selected!")
        main()


# Home screen function for the program
def main():
    print("Welcome to Pymanager to Login enter 1 for Registration enter 2! \n")
    option_select = str(input("Enter your option:  "))
    input_test(option_select)


if __name__ == "__main__":
    main()


