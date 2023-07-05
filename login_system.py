import hashlib

def signup():
    email = input("Enter your email: ")
    pwd = input("Enter your password: ")
    pwdConfirm = input("Confirm your password: ")
    if pwd == pwdConfirm:
        pwd.encode("ascii")
        print(pwd)
    while(pwd != pwdConfirm):
        print("The password does not match.")
signup()
