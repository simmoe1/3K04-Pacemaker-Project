# Entry point of application
from Gui import *
import tkinter as tk
from Coms import *

# Starts gui loop
root = tk.Tk()
coms = Coms()
app = Application(master=root, coms=coms)

app.mainloop()
