# Class is responsible saving data during registration and login of users
import os


class Credentials:

    # file which is being used for password storage
    filename = "userlist.txt"

    def __init__(self):
        # running a check to see if the file exists in case of first time run
        # if it doesnt a file is create to prevent reading a non existent file
        if not self.check_file():
            f = open(self.filename, "x")
            f.close()

    # function for registering a user
    def add_user(self, username, password, name):
        f = open(self.filename, "r")
        temp_list = []
        # loop over whole file and add every user to temp list
        while True:
            next_line = f.readline()
            if next_line != "":
                temp_line = next_line.split("|")
                if len(temp_line) == 3:
                    temp_list.append(temp_line)
            else:
                break
        f.close()
        username_not_used = True
        # check if theres already 10 users
        if len(temp_list) > 9:
            username_not_used = False
        else:
            for user in temp_list:
                if user[0] == username:
                    username_not_used = False
                    break
        if username_not_used:
            f = open(self.filename, "a")
            f.write(username + "|" + password + "|" + name + '\n')
            f.close()
        return username_not_used

    # function for logging a user in
    def check_user(self, username, password):
        f = open(self.filename, "r")
        name = ""
        # loop over every entry in the file to check for matching username and password
        while True:
            next_line = f.readline()
            if next_line != "":
                temp_line = next_line.split("|")
                if len(temp_line) == 3:
                    if temp_line[0] == username and temp_line[1] == password:
                        name = temp_line[2]
            else:
                break
        f.close()
        return name

    # function to check if file exists
    def check_file(self):
        return os.path.exists('./' + self.filename)
