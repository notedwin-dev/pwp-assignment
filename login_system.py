import hashlib
import json

def ReadDB(toRead, actual_value):
    # Opening the database JSON file
    with open("database.json", "r") as openFile:
        # Reading the database
        db = json.load(openFile)

        # Loop through the database to find a match of the specified value
        for item in db:
            if item.get(toRead) == actual_value:
                print(f"{toRead.capitalize()} already exists. Please choose a new one or login with the existing {toRead}.")
                return False

    return True


def WriteIntoDB(credentials):
    with open('database.json', "r") as read:
        read = json.load(read)
    
    read.append(credentials)

    with open('database.json', "w") as writeFile:
        json.dump(read, writeFile, indent=2)

        print("Account registered successfully!")


def signup():
    while True:
        username = input("Choose a username: ") # SAMPLE_USERNAME_1
        if ReadDB("username", username):
            break
    
    while True:
        email = input("Enter your email: ")
        if ReadDB("email", email):
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

signup()
