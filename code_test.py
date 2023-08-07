import inquirer
import hashlib

def ReadDB(toRead, actual_value):
    # Opening the database TXT file
    with open("roomdetails.txt", "r") as openFile:
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

def upload_room_details():
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

    return [{"action": None, "username": username}]

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

