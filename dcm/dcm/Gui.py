import tkinter as tk
from Frames.Login import *
from Frames.Register import *
from Frames.Central import *
from Credentials import *


class Application(tk.Frame):
    def __init__(self, coms, master=None):
        super().__init__(master)
        # initializing the gui window
        self.coms = coms
        self.width = 1000
        self.height = 700
        master.geometry("" + str(self.width) + "x" + str(self.height))
        master.title("Pacemaker Control Center")
        self.pack()
        self.master = master
        self.create_login()
        self.creds = Credentials()

    # function to create login window
    def create_login(self):
        self.login_screen = Login(reference=self)
        # Uncomment line below to skip login
        self.move_login_central(name="")

    # function to create register window
    def create_register(self):
        self.register_screen = Register(reference=self)

    # function to create pacemaker options window
    def create_central(self):
        self.central_screen = Central(reference=self)

    # function to move from login window to register window
    def move_login_register(self):
        self.login_screen.pack_forget()
        self.login_screen.destroy()
        self.create_register()

    # function to move from register window to login window
    def move_register_login(self):
        self.register_screen.pack_forget()
        self.register_screen.destroy()
        self.create_login()

    # function to move from register window to main window
    def move_register_central(self, name):
        self.register_screen.pack_forget()
        self.register_screen.destroy()
        self.create_central()

    # function to move from login window to main widow
    def move_login_central(self, name):
        self.login_screen.pack_forget()
        self.login_screen.destroy()
        self.create_central()
