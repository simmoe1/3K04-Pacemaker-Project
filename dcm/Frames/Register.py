import tkinter as tk


class Register(tk.Frame):

    def __init__(self, reference):
        super(Register, self).__init__()
        # Save reference to main gui
        self.reference = reference

        # Set up gui widgets
        self.title_label = tk.Label(self, text="Register To The Control Center")
        self.title_label.pack(side="top")

        self.subtitle_label = tk.Label(self, text="Please register if you do not have an account")
        self.subtitle_label.pack(side="top")

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.password_confirm = tk.StringVar()
        self.name = tk.StringVar()
        self.helper = tk.StringVar()
        self.helper.set("")

        self.username_text = tk.Label(self, text="Username")
        self.username_text.pack()
        self.username_entry = tk.Entry(self, textvariable=self.username, width=15).pack()

        self.password_text = tk.Label(self, text="Password")
        self.password_text.pack()
        self.password_entry = tk.Entry(self, textvariable=self.password, show="*", width=15).pack()

        self.password_confirm_text = tk.Label(self, text="Confirm Password")
        self.password_confirm_text.pack()
        self.password_confirm_entry = tk.Entry(self, textvariable=self.password_confirm, show="*", width=15).pack()

        self.name_text = tk.Label(self, text="Name")
        self.name_text.pack()
        self.name_entry = tk.Entry(self, textvariable=self.name, width=15).pack()

        self.helper_text = tk.Label(self, textvariable=self.helper)
        self.helper_text.pack()

        self.register_button = tk.Button(self, text="Register", fg="red", command=self.check_register)
        self.register_button.pack()

        self.back_button = tk.Button(self, text="Back To Login", fg="red", command=self.back)
        self.back_button.pack()

        self.pack()

    # When register button is clicked
    def check_register(self):
        username = self.username.get()
        password = self.password.get()
        password_confirm = self.password_confirm.get()
        name = self.name.get()

        user_flag = False
        pass_flag = False
        conf_flag = False
        name_flag = False
        char_flag = False

        # Check to make sure registration info is valid
        if len(username) == 0:
            user_flag = True
            self.helper.set("Username is empty")
        if len(password) < 4:
            pass_flag = True
            self.helper.set("Password too short")
        if password != password_confirm:
            conf_flag = True
            self.helper.set("Passwords dont match")
        if len(name) < 3:
            name_flag = True
            self.helper.set("Name is too short")
        if "|" in username or "|" in password or "|" in name:
            char_flag = True

        # if the registration info is correct ask credentials class to add a user
        if user_flag | pass_flag | conf_flag | name_flag | char_flag:
            print("failed")
        else:
            if self.reference.creds.add_user(username, password, name):
                print("Registered Successful")
                self.reference.move_register_central(name=name)
            else:
                print("Username in use")
                self.helper.set("Username in use")

    # When the back button is pressed
    def back(self):
        self.reference.move_register_login()
