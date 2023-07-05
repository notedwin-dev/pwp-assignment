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

                choice_question = [
                    inquirer.List("action_type", choices=[f"Choose new {toRead}", "Login instead"], carousel=True)
                ]
                choice_answer = inquirer.prompt(choice_question)

                choice = choice_answer["action_type"]

                if choice == f"Choose new {toRead}":
                    return False, choice
                else:
                    return True, choice
        else:
            return True, None



def WriteIntoDB(credentials):
    with open('database.json', "r") as read:
        read = json.load(read)
    
    read.append(credentials)

    with open('database.json', "w") as writeFile:
        json.dump(read, writeFile, indent=2)

        print("Account registered successfully!")


def CompareCredentials(username, password):
    with open('database.json', 'r') as read:
        db = json.load(read)

    for item in db:
        if item.get("username") == username:
            if item.get("password") == password:
                return True
            else:
                return False
    return False


def signup():
    while True:
        username = input("Choose a username: ")
        proceed, choice = ReadDB("username", username)
        if proceed == False:
            continue
        elif choice == "Login instead":
            print("redirecting you to login instead.")
            return [{"action": "LOGIN", "username": username}]
        else:
            break
    
    while True:
        email = input("Enter your email: ")
        proceed, choice = ReadDB("email", email)
        if proceed == False:
            continue
        elif choice == "Login instead":
            print("redirecting you to login instead.")
            return "LOGIN"
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
    return [{"action": None, "username": None}]


def login(username=None):
    if not username:
        print("Please login using your username and password.")
        username = input("Username: ")
        pwd = input("Password: ")

        encode = pwd.encode()
        hashed = hashlib.md5(encode).hexdigest()

        compare = CompareCredentials(username, hashed)

        while compare is False:
            print("Password is incorrect")
            pwd = input("Re-enter your password: ")
            encode = pwd.encode()
            hashed = hashlib.md5(encode).hexdigest()
            compare = CompareCredentials(username, hashed)
        
        
        print(f"Welcome {username}! Your password is {pwd}")
    else:
        print(f"Welcome {username}, please login with your password")
        print(f"Username: {username}")
        pwd = input("Password: ")

        encode = pwd.encode()
        hashed = hashlib.md5(encode).hexdigest()

        compare = CompareCredentials(username, hashed)

        while compare is False:
            print("Password is incorrect")
            pwd = input("Re-enter your password: ")
            encode = pwd.encode()
            hashed = hashlib.md5(encode).hexdigest()
            compare = CompareCredentials(username, hashed)
        
        
        print(f"Welcome {username}! Your password is {pwd}")

            


print("Welcome to APU Hotel Reservation System (HRS).")
questions = [
inquirer.List("user_type", message="Select your User type", choices=["Admin", "Registered User", "New User"])
]

answers = inquirer.prompt(questions)

if answers["user_type"] == 'Admin':
    login()
    # code for admin login

elif answers["user_type"] == 'Registered User':
    login()
    # code for registered user

elif answers["user_type"] == 'New User':
    print("Please sign up an account with us.")
    signupProcess = signup()

    username = signupProcess[0]["username"]
    action = signupProcess[0]["action"]

    if action == "LOGIN" and username:
        login(username)
    else:
        login()
