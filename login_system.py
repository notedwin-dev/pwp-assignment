import hashlib
import json
import inquirer

def ReadDB(toRead, actual_value):
    # Opening the database JSON file
    with open("database.json", "r") as openFile:
        # Reading the database
        db = json.load(openFile)

        # Loop through the database to find a match of the specified value
        for item in db:
            if item.get(toRead) == actual_value:
                print(f"{toRead.capitalize()} already exists. Please choose a new one or login with the existing {toRead}.")

                choice = [
                    inquirer.List("action_type", choices=[f"Choose new {toRead}", "Login instead"], carousel=True)
                ]
                answer = inquirer.prompt(choice)

                choice = answer["action_type"]

                if choice == f"Choose new {toRead}":
                    return False, choice
                else:
                    return True, choice


def WriteIntoDB(credentials):
    with open('database.json', "r") as read:
        read = json.load(read)
    
    read.append(credentials)

    with open('database.json', "w") as writeFile:
        json.dump(read, writeFile, indent=2)

        print("Account registered successfully!")


def signup():
    while True:
        username = input("Choose a username: ")
        proceed, choice = ReadDB("username", username)
        if proceed == False:
            continue
        elif choice == "Login instead":
            print("redirecting you to login instead.")
            return
        else:
            break
    
    while True:
        email = input("Enter your email: ")
        proceed, choice = ReadDB("email", email)
        if proceed == False:
            continue
        elif choice == "Login instead":
            print("redirecting you to login instead.")
            return
        else:
            break
        
    pwd = input("Enter your password: ")
    pwdConfirm = input("Confirm your password: ")
    while(pwd != pwdConfirm):
        print("The password does not match.")
        pwdConfirm = input("Re-confirm your password: ")

    if pwd == pwdConfirm:
        encode = pwd.encode()
        hashed = hashlib.md5(encode).hexdigest()
        

    credentials = {
        "username": username,
        "email": email,
        "password": hashed
    }

    WriteIntoDB(credentials)

print("Welcome to APU Hotel Reservation System (HRS).")
questions = [
inquirer.List("user_type", message="Select your User type", choices=["Admin", "Registered User", "New User"])
]

answers = inquirer.prompt(questions)

if answers["user_type"] == 'Admin':
    print("Please login to your account.")
    # code for admin login

elif answers["user_type"] == 'Registered User':
    print("Please login to your account.")
    # code for registered user

elif answers["user_type"] == 'New User':
    print("Please sign up an account with us.")
    signup()
