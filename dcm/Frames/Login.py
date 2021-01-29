import tkinter as tk


class Login(tk.Frame):

    def __init__(self, reference):
        super(Login, self).__init__()
        # Saving reference to main gui
        self.reference = reference

        # Setting gui widgets
        self.login_title_label = tk.Label(self, text="Welcome To the Control Center")
        self.login_title_label.pack(side="top")

        self.login_subtitle_label = tk.Label(self, text="Please login to continue")
        self.login_subtitle_label.pack(side="top")

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.helper = tk.StringVar()
        self.helper.set("")

        self.login_username_text = tk.Label(self, text="Username")
        self.login_username_text.pack()
        self.login_username = tk.Entry(self, textvariable=self.username, width=15).pack()

        self.login_password_text = tk.Label(self, text="Password")
        self.login_password_text.pack()
        self.login_password = tk.Entry(self, textvariable=self.password, show="*", width=15).pack()

        self.login_helper_text = tk.Label(self, textvariable=self.helper)
        self.login_helper_text.pack()

        self.login_button = tk.Button(self, text="Login", fg="red", command=self.check_login)
        self.login_button.pack()

        self.register_button = tk.Button(self, text="Register", fg="red", command=self.change_register)
        self.register_button.pack()

        self.pack()

    # when login button is clicked
    def check_login(self):
        username = self.username.get()
        password = self.password.get()
        # Use credentials class to check if login passes
        name = self.reference.creds.check_user(username, password)
        # Let user know they got it wrong or move to main window
        if name == "":
            self.helper.set("Credentials are incorrect")
        else:
            self.reference.move_login_central(name=name)

    # move to register window
    def change_register(self):
        print("register")
        self.reference.move_login_register()

