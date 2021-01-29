import tkinter as tk

from Frames.Graph import *

class Central(tk.Frame):

    def __init__(self, reference):
        super(Central, self).__init__()
        # Saving reference to gui
        self.reference = reference

        # Setting up widgets
        self.grid_columnconfigure(0, weight=1)
        w = reference.width
        h = reference.height
        self.devices = tk.StringVar(self)
        self.connection_state = tk.StringVar(self)
        self.connection_state.set("Inactive")
        self.b1t = tk.StringVar(self)
        self.b1t.set("Connect")
        self.b2t = tk.StringVar(self)
        self.b2t.set("Upload")
        self.mode = tk.StringVar(self)
        self.mode.set("AOO")
        self.l8t = tk.StringVar(self)
        self.l8t.set("Atrium")
        self.devices_list = []
        self.devices_text = ['a']
        print(self.devices_list)
        self.f1 = tk.Frame(self, height=reference.height, width=250, bg="grey").place(x=0, y=0)
        self.l1 = tk.Label(self, text="Pacemaker Menu").place(x=75, y=10)
        self.l2 = tk.Label(self, text="Devices").place(x=15, y=44)

        self.o1 = tk.OptionMenu(self, self.devices, *self.devices_text)
        self.devices_refresh()

        self.o1.place(anchor=tk.NE, x=235, y=40)
        self.b1 = tk.Button(self, textvariable=self.b1t, command=self.device_button, state=tk.DISABLED, width=30)
        self.b1.place(x=15, y=80)
        self.devices.trace('w', self.device_select)
        self.l3 = tk.Label(self, text="Connection Status").place(x=15, y=120)
        self.l4 = tk.Label(self, textvariable=self.connection_state).place(anchor=tk.NE, x=235, y=120)
        self.b2 = tk.Button(self, textvariable=self.b2t, command=self.device_upload, state=tk.DISABLED, width=30)
        self.b2.place(x=15, y=180)
        self.b3 = tk.Button(self, text="Refresh", command=self.devices_refresh, width=30)
        self.b3.place(x=15, y=210)

        self.l10 = tk.Label(self, text="Egram PlayBack").place(x=75, y=340)
        self.b4 = tk.Button(self, text="Play", command=self.device_play, width=9, state=tk.DISABLED)
        self.b4.place(x=15, y=370)
        self.b5 = tk.Button(self, text="Stop", command=self.device_stop, width=9, state=tk.DISABLED)
        self.b5.place(x=90, y=370)
        self.b6 = tk.Button(self, text="Clear", command=self.device_clear, width=9, state=tk.DISABLED)
        self.b6.place(x=165, y=370)

        # Pacemaker parameters
        self.t1 = tk.Label(self, text="Pacemaker Parameter").place(x=w/2+60, y=0)
        self.o2 = tk.OptionMenu(self, self.mode, "AOO", "VOO", "AAI", "VVI", "DOO", "AOOR", "VOOR", "AAIR", "VVIR", "DOOR").place(x=265, y=40)
        self.l7 = tk.Label(self, text="Affected Chamber: ").place(x=355, y=46)
        self.l8 = tk.Label(self, textvariable=self.l8t).place(x=460, y=46)
        self.mode.trace('w', self.mode_select)

        rx = 265
        ry = 76
        rinc = 170
        self.s1v = tk.DoubleVar()
        self.s1 = tk.Scale(self, orient=tk.HORIZONTAL, variable=self.s1v, length=150, from_=0.1, to=1.9, resolution=0.1)
        self.s1.place(x=rx, y=ry)
        self.s1v.set(0.4)
        self.s1t = tk.Label(self, text="Pulse Width (ms)").place(x=rx+20, y=ry+40)
        rx += rinc

        self.s2v = tk.DoubleVar()
        self.s2 = tk.Scale(self, orient=tk.HORIZONTAL, variable=self.s2v, length=150, from_=500, to=7500, resolution=50)
        self.s2.place(x=rx, y=ry)
        self.s2v.set(3750)
        self.s2t = tk.Label(self, text="Pulse Amplitude (mV)").place(x=rx+20, y=ry+40)
        rx += rinc
        self.s3v = tk.DoubleVar()
        self.s3 = tk.Scale(self, orient=tk.HORIZONTAL, variable=self.s3v, length=150, from_=30, to=175, resolution=1)
        self.s3.place(x=rx, y=ry)
        self.s3v.set(60)
        self.s3t = tk.Label(self, text="Lower Limit (ppm)").place(x=rx+20, y=ry+40)

        self.s5v = tk.DoubleVar()
        self.s5 = tk.Scale(self, orient=tk.HORIZONTAL, variable=self.s5v, length=150, from_=120, to=300, resolution=1)
        self.s5.place(x=rx, y=ry+70)
        self.s5v.set(200)
        self.s5t = tk.Label(self, text="Upper Limit (ppm)").place(x=rx+20, y=ry+110)
        rx += rinc
        self.s4v = tk.DoubleVar()
        self.s4 = tk.Scale(self, orient=tk.HORIZONTAL, variable=self.s4v, length=150, from_=150, to=500, resolution=5)
        self.s4.place(x=rx, y=ry)
        self.s4v.set(250)
        self.s4t = tk.Label(self, text="Refractory Period (ms)").place(x=rx+20, y=ry+40)

        # Create Graphs

        canvasHeight = 300
        canvasWidth = 500
        self.c1 = Graph(reference=reference, canv_h=canvasHeight,canv_w=canvasWidth, name="Atrium EGram")
        self.c1.place(x=-2, y=398)
        self.c2 = Graph(reference=reference, canv_h=canvasHeight, canv_w=canvasWidth, name="Ventricle EGram")
        self.c2.place(x=500, y=398)
        self.reference.coms.set_atr_graph(self.c1)
        self.reference.coms.set_vent_graph(self.c2)

        self.pack(expand=1, fill=tk.BOTH)

    # Function to start connection with devices
    def device_button(self):
        print(self.devices.get())
        for devices in self.devices_list:
            if devices[1] == self.devices.get():
                self.reference.coms.connect(devices[0])
                self.b2.configure(state="normal")
                self.b4.configure(state="normal")
                self.connection_state.set("Active")

    # Function to upload data to pacemaker
    def device_upload(self):
        modes = ["AOO", "VOO", "AAI", "VVI", "DOO", "AOOR", "VOOR", "AAIR", "VVIR", "DOOR"]
        mode_text = self.mode.get()
        mode = 1
        for i in range(len(modes)):
            if modes[i] == mode_text:
                mode = i+1
        lrl = self.s3v.get()
        url = self.s5v.get()
        pulse_amp = self.s2v.get()
        pulse_width = self.s1v.get()
        pulse_per = self.s4v.get()
        self.reference.coms.upload(mode=mode, lrl=lrl, url=url, pulse_amp=pulse_amp, pulse_width=pulse_width, pulse_per=pulse_per)

    # Function to start the graphing
    def device_play(self):
        self.reference.coms.play()
        self.b4.configure(state=tk.DISABLED)
        self.b5.configure(state="normal")
        self.b6.configure(state="normal")

    # Function to stop the graphing
    def device_stop(self):
        self.reference.coms.stop()
        self.b4.configure(state="normal")
        self.b5.configure(state=tk.DISABLED)
        self.b6.configure(state=tk.DISABLED)

    # Function to clear the graphs
    def device_clear(self):
        self.c1.clear()
        self.c2.clear()

    # Function to fresh device list
    def devices_refresh(self):
        self.devices.set('')
        self.o1['menu'].delete(0, 'end')
        self.devices_list = self.reference.coms.refresh_comports()
        self.devices_text = []
        for port in self.devices_list:
            self.devices_text.append(port[1])
            print(port[1])
        if len(self.devices_text) == 0:
            self.devices_text = [""]
            self.o1.configure(state=tk.DISABLED)
        else:
            self.o1.configure(state="normal")
            for text in self.devices_text:
                self.o1['menu'].add_command(label=text, command=tk._setit(self.devices, text))

    # Selection of device
    def device_select(self, *args):
        self.b1.config(state="normal")

    # On selection of mode
    def mode_select(self, *args):
        mode = self.mode.get()
        self.s1v.set(0.4)
        self.s5v.set(200)
        self.s3v.set(60)
        if mode == "AOO":
            self.l8t.set("Atrium")
            self.s4v.set(250)
            self.s2v.set(3750)
        elif mode == "AAI":
            self.l8t.set("Atrium")
            self.s4v.set(250)
            self.s2v.set(3500)
        elif mode == "VOO":
            self.l8t.set("Ventricle")
            self.s4v.set(320)
            self.s2v.set(3750)
        elif mode == "VVI":
            self.l8t.set("Ventricle")
            self.s4v.set(320)
            self.s2v.set(3500)
        elif mode == "DOO":
            self.l8t.set("Both")
            self.s4v.set(250)
            self.s2v.set(3750)
        elif mode == "AOOR":
            self.l8t.set("Atrium")
            self.s4v.set(250)
            self.s2v.set(3750)
        elif mode == "VOOR":
            self.l8t.set("Ventricle")
            self.s4v.set(320)
            self.s2v.set(3750)
        elif mode == "AAIR":
            self.l8t.set("Atrium")
            self.s4v.set(250)
            self.s2v.set(3500)
        elif mode == "VVIR":
            self.l8t.set("Ventricle")
            self.s4v.set(320)
            self.s2v.set(3500)
        elif mode == "DOOR":
            self.l8t.set("Both")
            self.s4v.set(250)
            self.s2v.set(3750)