import hashlib
import inquirer
import time
from email_validator import validate_email, EmailNotValidError
# line 292 changed


def countdown():
    count = 3
    while count != -1:
        count -= 1
        time.sleep(1)
        print(f"Returning to user menu in... {count+1} seconds", end="\r")


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

def search_specific_customer():
        with open('database.txt', "r") as file:
            file_content = file.read()

        db = eval(file_content)




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
        try:
            validate_email(email)
        except EmailNotValidError as errorMsg:
            print(str(errorMsg))
            continue

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

        if room_number == None and room_type == None:
            available = []
            for items in db:
                available.append(items)
            return available

    return None


# Second Phase: User access

# Work in Progress upload room details


def generate_report(Rname=None):
    with open('database.txt', "r") as file:
        file_content = file.read()

        db = eval(file_content)

        if Rname == None:
            for items in db:
                print(items)

    return None



def book_room(username):
    print("--Book a room--")
    questions = [
        inquirer.List("room_type", message="Select a room type", choices=[
            "Single Bedroom", "Double Bedroom", "Family Bedroom"]),
    ]

    answers = inquirer.prompt(questions)

    rdavailable = view_room_details(room_type=answers["room_type"])

    if type(rdavailable) is list and len(rdavailable) > 0:
        selected_room = rdavailable[0]
        print("Your room number is: ", selected_room["Room Number"])

        with open('roomdetails.txt', 'r') as read:
            file_contents = read.read()

            db = eval(file_contents)

        selected_room["Availability"] = "Booked"
        selected_room["Booked by"] = username

        updated_db = [
            room if room.get("Room Number") != selected_room["Room Number"]
            else selected_room for room in db
        ]

        with open("roomdetails.txt", "w") as overwriteFile:
            overwriteFile.write(str(updated_db))

        print("Room booked successfully")

    else:
        print("No room is available at this moment")


def view_all_bookings():
    with open('roomdetails.txt', "r") as file:
        file_content = file.read()

        db = eval(file_content)

        booked_rooms = []

        for items in db:
            if items.get("Availability") == "Booked":
                booked_rooms.append(items)
        return booked_rooms


def view_booking(username):
    with open('roomdetails.txt', "r") as file:
        file_content = file.read()

        db = eval(file_content)

        booked_rooms = []

        for items in db:
            if items.get("Booked by") == username:
                booked_rooms.append(items)
        return booked_rooms


def cancel_booking(username):
    print("--Cancel Booking--")
    booked_rooms = view_booking(username)

    if len(booked_rooms) > 0:
        for room in booked_rooms:
            print("Room Number:", room["Room Number"])
        room_number_to_cancel = input(
            "Enter the room number to cancel the booking: ")

        with open("roomdetails.txt", "r") as read:
            file_contents = read.read()

        db = eval(file_contents)

        updated_db = []
        for room in db:
            if room["Room Number"] == str(room_number_to_cancel):
                room["Availability"] = "Available"
                room["Booked by"] = "None"
            updated_db.append(room)

        with open("roomdetails.txt", "w") as overwriteFile:
            overwriteFile.write(str(updated_db))

        print("Booking canceled successfully!")
    else:
        print("You have no bookings to cancel.")

def cancel_booking(username):
    print("--Cancel Booking--")
    booked_rooms = view_booking(username)

    if len(booked_rooms) > 0:
        for room in booked_rooms:
            print("Room Number:", room["Room Number"])
        room_number_to_cancel = input(
            "Enter the room number to cancel the booking: ")

        with open("roomdetails.txt", "r") as read:
            file_contents = read.read()

        db = eval(file_contents)

        updated_db = []
        for room in db:
            if room["Room Number"] == str(room_number_to_cancel):
                room["Availability"] = "Available"
                room["Booked by"] = "None"
            updated_db.append(room)

        with open("roomdetails.txt", "w") as overwriteFile:
            overwriteFile.write(str(updated_db))

        print("Booking canceled successfully!")
    else:
        print("You have no bookings to cancel.")


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
        "Availability": "Available",
        "Booked by": "None"
    }

    WriteIntoRoomDB(R_Details)

    print("Room Details uploaded Succesfully")


def res_menu():
    restaurants = [inquirer.List("Restaurants", message="Please select the restaurant you wish to view", choices=[
        "Rordon Gamsey",
        "Mamakau Restaurant",
        "Sushi Mentai",
        "Return to Main Menu"
    ])]

    answers = inquirer.prompt(restaurants)

    if answers["Restaurants"] == "Rordon Gamsey":
        questions = [
            inquirer.List("rordon_gamsey_restaurant", "=====Rordon Gamsey Restaurant=====", choices=[
                "Nasi Lemak",  # RM20
                "Pan Mee",  # RM 11
                "Mee Goreng",  # RM 9
                "Yangzhou Fried Rice",  # RM13
                "Popiah",  # RM 9
                "Back"
            ])
        ]

        food_choices = inquirer.prompt(questions)

        food_choice = food_choices["rordon_gamsey_restaurant"]

        if food_choice == "Nasi Lemak":
            print(f"The price for {food_choice} is RM20.")

            questions = [
                inquirer.List("nasi_lemak", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            nasi_lemak_choices = inquirer.prompt(questions)

            if nasi_lemak_choices["nasi_lemak"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Pan Mee":
            print(f"The price for {food_choice} is RM11.")

            questions = [
                inquirer.List("pan_mee", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            pan_mee_choices = inquirer.prompt(questions)

            if pan_mee_choices["pan_mee"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Mee Goreng":
            print(f"The price for {food_choice} is RM11.")

            questions = [
                inquirer.List("mee_goreng", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            mee_goreng_choices = inquirer.prompt(questions)

            if mee_goreng_choices["mee_goreng"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Yangzhou Fried Rice":
            print(f"The price for {food_choice} is RM13.")

            questions = [
                inquirer.List("fried_rice", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            fried_rice_choices = inquirer.prompt(questions)

            if fried_rice_choices["fried_rice"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Popiah":
            print(f"The price for {food_choice} is RM9.")

            questions = [
                inquirer.List("popiah", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            popiah_choices = inquirer.prompt(questions)

            if popiah_choices["popiah"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Back":
            return

    elif answers["Restaurants"] == "Mamakau Restaurant":
        questions = [
            inquirer.List("mamakau_restaurant", "=====Mamakau Restaurant=====", choices=[
                "Roti Canai",  # RM6
                "Roti Bakar Mozzarella",  # RM10
                "Roti Telur",  # RM7
                "Roti Planta",  # RM7
                "Naan Biasa"  # RM5
            ])
        ]

        food_choices = inquirer.prompt(questions)

        food_choice = food_choices["mamakau_restaurant"]

        if food_choice == "Roti Canai":
            print(f"Successfully {food_choice} is RM6.")

            questions = [
                inquirer.List("roti_canai", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            nasi_lemak_choices = inquirer.prompt(questions)

            if nasi_lemak_choices["roti_canai"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Roti Bakar Mozzarella":
            print(f"The price for {food_choice} is RM10.")

            questions = [
                inquirer.List("roti_bakar", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            roti_bakar_choices = inquirer.prompt(questions)

            if roti_bakar_choices["roti_bakar"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Roti Telur":
            print(f"The price for {food_choice} is RM7.")

            questions = [
                inquirer.List("roti_telur", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            roti_telur_choices = inquirer.prompt(questions)

            if roti_telur_choices["roti_telur"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Roti Planta":
            print(f"The price for {food_choice} is RM7.")

            questions = [
                inquirer.List("roti_planta", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            roti_planta_choices = inquirer.prompt(questions)

            if roti_planta_choices["roti_planta"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Naan Biasa":
            print(f"The price for {food_choice} is RM5.")

            questions = [
                inquirer.List("naan_biasa", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            naan_choices = inquirer.prompt(questions)

            if naan_choices["naan_biasa"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

    elif answers["Restaurants"] == "Sushi Mentai":
        questions = [
            inquirer.List("sushi_mentai", "======Sushi Mentai======", choices=[
                "Salad Deluxe", #RM15
                "Tori Katsu Curry Rice", #RM18
                "Tori Katsu Don", #RM16
                "Tempura Udon", #RM15
                "Tenzaru Soba" #RM14
            ])
        ]

        food_choices = inquirer.prompt(questions)

        food_choice = food_choices["sushi_mentai"]

        if food_choice == "Salad Deluxe":
            print(f"Successfully {food_choice} is RM6.")

            questions = [
                inquirer.List("salad_deluxe", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            salad_deluxe_choices = inquirer.prompt(questions)

            if salad_deluxe_choices["roti_canai"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Tori Katsu Curry Rice":
            print(f"The price for {food_choice} is RM10.")

            questions = [
                inquirer.List("tori_katsu_curry_don", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            tori_katsu_curry_don_choices = inquirer.prompt(questions)

            if tori_katsu_curry_don_choices["tori_katsu_curry_don"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Tori Katsu Don":
            print(f"The price for {food_choice} is RM7.")

            questions = [
                inquirer.List("tori_katsu_don", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            tori_katsu_don_choices = inquirer.prompt(questions)

            if tori_katsu_don_choices["tori_katsu_don"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Tempura Udon":
            print(f"The price for {food_choice} is RM7.")

            questions = [
                inquirer.List("tempura_udon", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            tempura_udon_choices = inquirer.prompt(questions)

            if tempura_udon_choices["tempura_udon"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")

        elif food_choice == "Tenzaru Soba":
            print(f"The price for {food_choice} is RM5.")

            questions = [
                inquirer.List("tenzaru_soba", "Select our action", choices=[
                    "Order",
                    "Back",
                    "Return to Main Menu"
                ])
            ]

            tenzaru_soba_choices = inquirer.prompt(questions)

            if tenzaru_soba_choices["tenzaru_soba"] == "Order":
                quantity = int(input("Quantity: "))

                print(f"Sucessfully ordered x{quantity} {food_choice}(s).")


def search_specific_booking(Cname=None):
    if not Cname:
        print("Type the name of the customer you wish to view.")
        if True:
            Cname = input("Username: ")

            with open('roomdetails.txt', 'r') as read:
                file_contents = read.read()

            db = eval(file_contents)

            # Check if the username exists in the database
            username_exists = any(item.get("Booked by") ==
                                  Cname for item in db)
            for items in db:
                if username_exists:
                    print(items)
                    break   



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
                    "Generate Customer Report",
                    "Exit"
                ]
            )
        ]

        print("=================================================")
        choices = inquirer.prompt(questions)

        admin_choices = choices["admin"]

        if (admin_choices == "View All Room Details"):
            details = view_room_details()

            print(details)

            countdown()

            menu(user_type, username)

        elif (admin_choices == "Upload Room Details"):
            upload_room_details()

            countdown()

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

            countdown()

            menu(user_type, username)

        elif (admin_choices == "Search Specific Room Service Menu For Specific Restaurant"):
            res_menu()

            countdown()

            menu(user_type, username)

        elif (admin_choices == "View All Booking Of Customers"):
            print(view_all_bookings())

            countdown()

            menu(user_type, username)

        elif (admin_choices == "Generate Bills"):
            print("generating bill for each customers")

            countdown()

            menu(user_type, username)

        elif (admin_choices == "Search Booking Of Specific Customer"):
                search_specific_booking(Cname=None)


                countdown()

                menu(user_type, username)

        elif (admin_choices == "Generate Customer Report"):
            generate_report(Rname=None)
            countdown()

            menu(user_type, username)

        elif (admin_choices == "Exit"):
            print("Admin Account logged out successfully.")

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

            countdown()

            menu(user_type, username)

        elif (user_choices == "Book a Room"):
            book_room(username)

            countdown()

            menu(user_type, username)

        elif (user_choices == "View/Order from Room Service Menu"):
            res_menu()

            countdown()

            menu(user_type, username)

        elif (user_choices == "View Booking"):
            print(view_booking(username))

            countdown()

            menu(user_type, username)

        elif (user_choices == "Update Booking"):
            room_number = input("Enter your booked room number: ")

            countdown()

            menu(user_type, username)

        elif (user_choices == "Cancel Booking"):
            cancel_booking(username)


            countdown()

            menu(user_type, username)

        elif (user_choices == "View Personal Details"):
            print("-- Personal Details --")

            personal_details = view_personal_details(username)

            dob = personal_details["date_of_birth"]
            gender = personal_details["gender"]
            address = personal_details["address"]
            contact_number = personal_details["contact_number"]
            email_a = personal_details["email"]

            print("Username:", username, "\nDate of birth:", dob, "\nGender:",
                  gender, "\nAddress:", address, "\nContact number:", contact_number, "\nEmail:", email_a)

            countdown()

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
                    new_password = input("Enter your new password: ")
                    update_details.update({"password": new_password})

            updated_db = [item if item.get(
                "username") != username else update_details for item in db]

            with open("database.txt", "w") as overwriteFile:
                overwriteFile.write(str(updated_db))

            print("Details updated successfully!")
            print("Your new personal details are: ", update_details)

            countdown()

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
                countdown()

                menu(user_type, username)
            else:
                print("Invalid input. Please try again.")

                countdown()

                menu(user_type, username)

        elif (user_choices == "Exit"):
            print("Thank you for using APU Hotel Reservation System.")
            return

    elif (user_type == "registered_user"):
        return


def welcome_screen(user_type=None, username=None):
    print("Welcome to APU Hotel Reservation System (HRS).")
    print("To navigate the menu, press the UP and DOWN arrow keys")
    print("To select your choice, press the SPACEBAR button")
    print("To confirm your choice, press the ENTER button")
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
                    print(view_room_details())
                    return {"user_type": "registered_user", "username": username}


def main():
    # Step 1: Welcome the user
    welcome = welcome_screen()

    # Step 2: Check user type
    user_type = welcome["user_type"]

    username = welcome["username"]

    menu(user_type, username)


main()
