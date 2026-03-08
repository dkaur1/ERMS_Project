import json
from json import JSONDecodeError

USERS_FILE = "data/users.json"

#------------------------------
#       User class
#______________________________
class User:

    def __init__(self, username, password, role):
        self.username = username
        self.__password = password
        self.role = role

    def validate_password(self, password):
        return self.__password == password

    def change_password(self, new_password):
        if len(new_password) < 6:
            raise ValueError("Password should be at least 6 characters long")

        self.__password = new_password

#----------------------------------------
#   Helper functions
#-----------------------------------------
# get users from the users file
def load_users():
    try:
        with open(USERS_FILE, "r") as userFile:
            users = json.load(userFile)
            return users

    except FileNotFoundError:
        print("User data file not found")
    except JSONDecodeError:
        print("Error: Corrupt JSON File for users")

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)   #indent=4, to indent each nesting level by 4 spaces, for cleaner file structure

def login():

    users = load_users()

    if not users:
        print("No users found")
        return None

    #allow 3 attempts max
    attempts = 3
    while attempts > 0:
        username = input("Username: ")
        password = input("Password: ")

        for user_data in users:
            user = User(user_data["username"], user_data["password"], user_data["role"])
            if user.username == username and user.validate_password(password):
                print("Login Successful")
                return user

        attempts -= 1
        print("Wrong Credentials - Maximum 3 attempts are allowed")

    print("Too many failed attempts")
    return None
