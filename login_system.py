import hashlib
import inquirer


def ReadDB(toRead, actual_value):
    # Opening the database TXT file
    with open("database.txt", "r") as openFile:
        # Reading the database
        file_contents = openFile.read()

        # Evaluate the string representation of list of dictionaries into the actual list object
        db = eval(file_contents)

        # Loop through the database to find a match of the specified value
        for item in db:
            if item.get(toRead) == actual_value:
                print(
                    f"{toRead.capitalize()} already exists. Please choose a new one or login with the existing {toRead}.")

                choice_question = [
                    inquirer.List("action_type", choices=[
                                  f"Choose new {toRead}", "Login instead"], carousel=True)
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
    with open('database.txt', "r") as readFile:
        file_contents = readFile.read()

        db = eval(file_contents)

    db.append(credentials)

    with open('database.txt', "w") as writeFile:
        # Write the list of dictionaries as a string representation into the text file
        writeFile.write(str(db))

        print("Account registered successfully!")
        print("=================================================")


def CompareCredentials(username, password):
    with open('database.txt', 'r') as read:
        # Read the contents of the file
        file_contents = read.read()

    # Evaluate the string representation of list of dictionaries into the actual list object
    db = eval(file_contents)

    # Loop through the list of user credentials
    for item in db:
        # If the username matches for the user that tries to log in
        if item.get("username") == username:
            # And the password hash is correct, return True so that the while loop stops.
            if item.get("password") == password:
                return True
            else:
                # Otherwise, return False so that the while loop will keep repeating until the password is correct.
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
    while (pwd != pwdConfirm):
        print("The password does not match.")
        pwdConfirm = input("Re-confirm your password: ")

    if pwd == pwdConfirm:
        encode = pwd.encode()
        hashed = hashlib.md5(encode).hexdigest()

    credentials = {
        "username": username,
        "email": email,
        "password": hashed,
        "role": "registered_user"
    }

    WriteIntoDB(credentials)

    return [{"action": None, "username": username}]


def login(username=None):
    if not username:
        print("Please login using your username and password.")
        while True:
            username = input("Username: ")

            with open('database.txt', 'r') as read:
                file_contents = read.read()

            db = eval(file_contents)

            # Check if the username exists in the database
            username_exists = any(item.get("username") ==
                                  username for item in db)

            if username_exists:
                break

            print("Username does not exist. Please try again.")

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

    return {"user_type": "user", "username": username}


def admin_login():
    print("Welcome to the Admin Login Portal.")
    print("=================================================")
    print("Please enter your admin credentails below.")
    while True:
        username = input("Username: ")

        with open('database.txt', 'r') as read:
            file_contents = read.read()

        db = eval(file_contents)

        # Check if the username exists in the database
        username_exists = any(item.get("username") == username for item in db)

        if username_exists:
            role = next((item.get("role")
                        for item in db if item.get("username") == username), None)
            if role == "admin":
                break
            else:
                print("Invalid username. Please try again.")
        else:
            print("Username does not exist. Please try again.")

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

    print("=================================================")
    print(
        f"Welcome {username}! Your password is {pwd}. You're now logged in as admin!")
    return {"user_type": "admin", "username": username}


def view_room_details():
    # view room details logic
    print("viewing room details")

# Second Phase: User access


def welcome_screen():
    print("Welcome to APU Hotel Reservation System (HRS).")
    print("=================================================")
    questions = [
        inquirer.List("user_type", message="Select your User type",
                      choices=["Admin", "Registered User", "New User"])
    ]

    answers = inquirer.prompt(questions)

    if answers["user_type"] == 'Admin':
        admin = admin_login()
        # code for admin login
        return admin

    elif answers["user_type"] == 'Registered User':
        user = login()
        # code for registered user
        return user

    elif answers["user_type"] == 'New User':
        print("Please sign up an account with us.", end="\n\n")
        print("=================================================")
        signupProcess = signup()

        username = signupProcess[0]["username"]
        action = signupProcess[0]["action"]

        if action == "LOGIN" and username:
            login(username)
        else:
            questions = [inquirer.List("qna", message="What do you want to do?", choices=[
                                       "View Room Details", "Login"])]
            registered = inquirer.prompt(questions)

            if registered["qna"] == 'Login' and username:
                login(username)
            elif registered["qna"] == 'View Room Details':
                view_room_details()


def main():
    # Step 1: Welcome the user
    welcome = welcome_screen()

    print("=================================================")

    # Step 2: Check user type
    user_type = welcome["user_type"]

    if (user_type == "admin"):
        # provide options for uploading room details, view all rooms, update/modify room info, delete room service info,
        # search specific room service menu for specific restaurant, view all booking of customers, generate bills,
        # search booking of specific customer, generate a report and exit
        questions = [
            inquirer.List(
                "admin",
                "Admin Menu",
                choices=[
                    "View All Room Details",
                    "Upload Room Details",
                    "Update/Modify Room Info",
                    "Delete Room Service Info",
                    "Search Specific Room Service Menu For Specific Restaurant",
                    "View All Booking Of Customers",
                    "Generate Bills",
                    "Search Booking Of Specific Customer",
                    "Generate Customer Report"
                ]
            )
        ]

        choices = inquirer.prompt(questions)

        return choices

    elif (user_type == "user"):
        questions = [
            inquirer.List(
                "user",
                "Registered User Menu",
                choices=[
                    "View Room Details",
                    "Book a Room",
                    "View/Order from Room Service Menu",
                    "View Booking",
                    "Update Booking",
                    "Cancel Booking",
                    "View Personal Details",
                    "Update Personal Details",
                    "Delete Personal Details",
                    "Exit"
                ]
            )
        ]

        choices = inquirer.prompt(questions)

        return


main()
