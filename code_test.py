import hashlib
import inquirer
import time
# line 292 changed


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


def WriteIntoDB(dict):
    with open('database.txt', "r") as readFile:
        file_contents = readFile.read()

        db = eval(file_contents)

    db.append(dict)

    with open('database.txt', "w") as writeFile:
        # Write the list of dictionaries as a string representation into the text file
        writeFile.write(str(db))


def WriteIntoRoomDB(dict):
    with open('roomdetails.txt', "r") as readFile:
        file_contents = readFile.read()

        db = eval(file_contents)

    db.append(dict)

    with open('roomdetails.txt', "w") as writeFile:
        # Write the list of dictionaries as a string representation into the text file
        writeFile.write(str(db))


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


def view_personal_details(username):
    with open('database.txt', "r") as file:
        file_content = file.read()

    db = eval(file_content)

    for items in db:
        if (items.get("username") == username):
            return items
            break


def delete_personal_details(username):
    with open('database.txt', 'r') as file:
        file_content = file.read()

    # Convert the file content to a list of dictionaries using eval
    db = eval(file_content)

    updated_db = [item for item in db if item.get("username") != username]

    with open('database.txt', 'w') as file:
        file.write(str(updated_db))

    return updated_db


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

    address = input("Home Address: ")
    contact = input("Contact Number: ")
    gender = input("Gender: ")
    dob = input("Date of birth:")

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
        "address": address,
        "contact_number": contact,
        "gender": gender,
        "date_of_birth": dob,
        "role": "registered_user",
    }

    WriteIntoDB(credentials)
    print("Account registered successfully!")
    print("=================================================")

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
    print("=================================================")
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


def view_room_details(room_number=None, room_type=None):
    with open('roomdetails.txt', "r") as file:
        file_content = file.read()

        db = eval(file_content)

        if room_number:
            for item in db:
                if item.get("Room Number") == room_number:
                    return item
            return None

        if room_type:
            available = []
            for item in db:
                if item.get("Availability") == "Available" and item.get("Room Type") == room_type:
                    available.append(item)
            return available

    return None

# Second Phase: User access

# Work in Progress upload room details


def book_room():
    print("--Book a room--")
    questions = [
        inquirer.List("room_type", message="Select a room type", choices=[
            "Single Bedroom", "Double Bedroom", "Family Bedroom"]),
    ]

    answers = inquirer.prompt(questions)

    rdavailable = view_room_details(room_type=answers["room_type"])
    print(rdavailable)

    print("Your room number is: ", rdavailable[0]["Room Number"])


def upload_room_details():
    print("--Upload Room Details--")
    questions = [
        inquirer.List("room_type", message="Select a room type", choices=[
            "Single Bedroom", "Double Bedroom", "Family Bedroom"]),
        inquirer.Text("room_price", message="Enter a room price"),
        inquirer.Text("room_number", message="Enter A room number"),
        inquirer.Checkbox("room_service", message="Select all applicable room services.", choices=[
            "Room Cleaning",
            "Karaoke Booking",
            "Food and Beverages"
        ])
    ]

    answers = inquirer.prompt(questions)

    answers["room_type"]
    answers["room_price"]
    answers["room_number"]
    answers["room_service"]

    R_Details = {
        "Room Type": answers["room_type"],
        "Room Price": answers["room_price"],
        "Room Number": answers["room_number"],
        "Room Services": answers["room_service"],
        "Availability": "Available"
    }

    WriteIntoRoomDB(R_Details)

    print("Room Details uploaded Succesfully")


def menu(user_type, username):
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
                    "Update/Modify Room Details",
                    "Search Specific Room Service Menu For Specific Restaurant",
                    "View All Booking Of Customers",
                    "Generate Bills",
                    "Search Booking Of Specific Customer",
                    "Generate Customer Report"
                ]
            )
        ]

        print("=================================================")
        choices = inquirer.prompt(questions)

        admin_choices = choices["admin"]

        if (admin_choices == "View All Room Details"):
            details = view_room_details()

            print(details)
        elif (admin_choices == "Upload Room Details"):
            upload_room_details()
            menu(user_type, username)

        elif (admin_choices == "Update/Modify Room Details"):
            room_number = input(
                "Enter the room number to modify room details: ")

            update_details = view_room_details(room_number)

            with open('roomdetails.txt', 'r') as read:
                file_contents = read.read()

                db = eval(file_contents)

            questions = [inquirer.Checkbox("update_details", "Please check any room details that you would like to update.",
                                           choices=[
                                               "Room Type",
                                               "Room Number",
                                               "Room Price",
                                               "Room Services",
                                           ])]

            answers = inquirer.prompt(questions)

            for x in answers["update_details"]:
                if x == "Room Type":
                    new_rt = input("Update your Room Type: ")
                    update_details.update({"Room Type": new_rt})

                if x == "Room Number":
                    new_rn = input("Update your Room Number: ")
                    update_details.update({"Room Number": new_rn})

                if x == "Room Price":
                    new_rp = input("Enter your new Room Price: ")
                    update_details.update({"Room Price": new_rp})

                if x == "Room Services":
                    questions = [inquirer.Checkbox("room_service", "Please update with the applicable room services.",
                                                   choices=[
                                                       "Room Cleaning",
                                                       "Karaoke Booking",
                                                       "Food and Beverages"
                                                   ])]

                    answers = inquirer.prompt(questions)

                    update_details.update(
                        {"Room Services": answers["room_service"]})

            updated_db = [item if item.get(
                "username") != username else update_details for item in db]

            with open("roomdetails.txt", "w") as overwriteFile:
                overwriteFile.write(str(updated_db))

            print("Details updated successfully!")
            print("Your new room details are: ", update_details)

            count = 5
            while count != 0:
                count -= 1
                time.sleep(1)
                print(
                    f"Returning to admin menu in... {count+1} seconds", end="\r")

            menu(user_type, username)
        elif (admin_choices == "Search Specific Room Service Menu For Specific Restaurant"):
            print("Searching specific room service menu for specific restaurant")
        elif (admin_choices == "View All Booking Of Customers"):
            print("viewing all bookings of customers")
        elif (admin_choices == "Generate Bills"):
            print("generating bill for each customers")
        elif (admin_choices == "Search Booking Of Specific Customer"):
            print("searching booking of specific customer")
        elif (admin_choices == "Generate Customer Report"):
            print("Generating customer report")

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

        print("=================================================")
        choices = inquirer.prompt(questions)

        user_choices = choices["user"]

        if (user_choices == "View Room Details"):
            details = view_room_details()
            print(details)
        elif (user_choices == "Book a Room"):
            book_room()
        elif (user_choices == "View/Order from Room Service Menu"):
            print("-- Room Service Menu --")
            print("menu is under maintenance.")
        elif (user_choices == "View Booking"):
            print("Viewing Booking Details")
        elif (user_choices == "Update Booking"):
            print("Updating booking status and details")
        elif (user_choices == "Cancel Booking"):
            print("cancelling booking...")
        elif (user_choices == "View Personal Details"):
            print("-- Personal Details --")

            personal_details = view_personal_details(username)

            dob = personal_details["date_of_birth"]
            gender = personal_details["gender"]
            address = personal_details["address"]
            contact_number = personal_details["contact_number"]

            print("Username:", username, "\nDate of birth:", dob, "\nGender:",
                  gender, "\nAddress:", address, "\nContact number:", contact_number)

            print("Returning back to main menu...")

            menu(user_type, username)

        elif (user_choices == "Update Personal Details"):

            update_details = view_personal_details(username)

            with open('database.txt', 'r') as read:
                file_contents = read.read()

                db = eval(file_contents)

            questions = [inquirer.Checkbox("update_details", "Please check any personal details that you would like to update.",
                                           choices=[
                                               "Date of birth",
                                               "Gender",
                                               "Address",
                                               "Contact Number",
                                               "Email",
                                               "Password",
                                           ])]

            answers = inquirer.prompt(questions)

            for x in answers["update_details"]:
                if x == "Date of birth":
                    new_dob = input("Update your Date of Birth: ")
                    update_details.update({"date_of_birth": new_dob})

                if x == "Gender":
                    new_gender = input("Update your gender: ")
                    update_details.update({"gender": new_gender})

                if x == "Address":
                    new_address = input("Enter your new Home Address: ")
                    update_details.update({"address": new_address})

                if x == "Contact Number":
                    new_contact = input("Update your new Contact Number: ")
                    update_details.update({"contact_number": new_contact})

                if x == "Email":
                    new_email = input("Update your new email: ")
                    update_details.update({"email": new_email})

                if x == "Password":
                    new_password = input("Enter yout new password: ")
                    update_details.update({"password": new_password})

            updated_db = [item if item.get(
                "username") != username else update_details for item in db]

            with open("database.txt", "w") as overwriteFile:
                overwriteFile.write(str(updated_db))

            print("Details updated successfully!")
            print("Your new personal details are: ", update_details)

            count = 5
            while count != 0:
                count -= 1
                time.sleep(1)
                print(
                    f"Returning to user menu in... {count+1} seconds", end="\r")

            menu(user_type, username)

        elif (user_choices == "Delete Personal Details"):
            prompt = input(
                "Deleting your personal information will result in account deletion from our database. Are you sure you want to delete your information? (Y/N) ")

            if (prompt.upper() == "Y"):
                print("Removing personal details from database...")
                updated = delete_personal_details(username)
                print(
                    "Account has been deleted. Sorry to see you go! Thanks for using APU Hotel Reservation System :/")

                welcome_screen()

            elif (prompt.upper() == "N"):
                print("Returning to main menu.")

                menu(user_type, username)
            else:
                print("Invalid input. Please try again.")
        elif (user_choices == "Exit"):
            print("Thank you for using APU Hotel Reservation System.")
            return

    elif (user_type == "registered_user"):
        return


def welcome_screen(user_type=None, username=None):
    print("Welcome to APU Hotel Reservation System (HRS).")
    print("=================================================")
    questions = [
        inquirer.List("user_type", message="Select your User type",
                      choices=["Admin", "Registered User", "New User"])
    ]

    if (user_type == None and username == None):
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
                return {"user_type": "user", "username": username}
            else:
                questions = [inquirer.List("qna", message="What do you want to do?", choices=[
                    "View Room Details", "Login"])]
                registered = inquirer.prompt(questions)

                if registered["qna"] == 'Login' and username:
                    login(username)
                    return {"user_type": "user", "username": username}
                elif registered["qna"] == 'View Room Details':
                    view_room_details()
                    return {"user_type": "registered_user", "action": "View Room Details"}


def main():
    # Step 1: Welcome the user
    welcome = welcome_screen()

    # Step 2: Check user type
    user_type = welcome["user_type"]

    username = welcome["username"]

    menu(user_type, username)


main()
