import time
import serial
import struct
import threading
import time


class Coms:

    def __init__(self):
        self.com_list = list([])
        self.connected = False
        self.play_state = False
        self.ser = None
        self.sleep_interval = 0
        self.timeout_interval = 0.1
        self.play_start = 0

    # Upload the current values from dcm to device
    def upload(self, mode, lrl, url, pulse_amp, pulse_width, pulse_per):
        if self.connected:
            print("Mode " + str(mode))
            print("Lower Rate Limit " + str(lrl))
            print("Upper Rate Limit " + str(url))
            print("Pulse Amplitude " + str(pulse_amp))
            print("Pulse Width" + str(pulse_width))
            print("Pulse Period " + str(pulse_per))
            mode_b = struct.pack("H", mode)
            lrl_b = struct.pack("d", lrl)
            url_b = struct.pack("d", url)
            pulse_amp_b = struct.pack("d", pulse_amp)
            pulse_width_b = struct.pack("d", pulse_width)
            pulse_per_b = struct.pack("d", pulse_per)
            data = b"\x16" + b"\x55" + pulse_amp_b + pulse_width_b + pulse_per_b + lrl_b + url_b + mode_b
            self.ser.write(data)

    # Stop
    def play(self):
        if self.connected:
            self.play_data = b"\x16" + b"\x22" + b"\x00" * 42
            self.play_state = True
            self.play_start = time.time()
            #self.thread = threading.Thread(target=self.coms_looper, args=())
            #self.thread.start()

    # Stop Reading from device
    def stop(self):
        self.play_state = False

    # Looper to keep getting signal data on different thread
    def coms_looper(self):
        while True:
            #need check to see if device disconnected
            if self.play_state:
                self.read_from_port(self.play_data)
            time.sleep(self.sleep_interval)

    # Read from the device
    def read_from_port(self, data):
            self.ser.write(data)
            print("Reading")
            data_r = self.ser.read(58)
            # if full data is received before timeout
            if len(data_r) == 58:
                # packing and unpacking
                t = time.time()-self.play_start
                atr_signal = struct.unpack("d", data_r[0:8])[0]
                vent_signal = struct.unpack("d", data_r[8:16])[0]
                mode = struct.unpack("H", data_r[16:18])
                url = struct.unpack("d", data_r[18:26])
                lrl = struct.unpack("d", data_r[26:34])
                pulse_width = struct.unpack("d", data_r[34:42])
                pulse_per = struct.unpack("d", data_r[42:50])
                pulse_amp = struct.unpack("d", data_r[50:58])
                print("Time " + str(t))
                print("Atr Signal " + str(atr_signal))
                print("Vent Signal " + str(vent_signal))
                # Adding points to graph
                self.atr_graph.add_point(time=t*1000, y=atr_signal*1000)
                self.vent_graph.add_point(time=t * 1000, y=vent_signal * 1000)
            else:
                # if not all data was received check to see if at least signals were received
                if len(data_r) >= 16:
                    t = time.time()-self.play_start
                    atr_signal = struct.unpack("d", data_r[0:8])[0]
                    vent_signal = struct.unpack("d", data_r[8:16])[0]
                    self.atr_graph.add_point(t * 1000, atr_signal * 1000)
                    self.vent_graph.add_point(t * 1000, vent_signal * 1000)
                else:
                    print("Read Failed")

    # Function to refresh the com ports
    def refresh_comports(self):
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            return None
        if comports:
            self.com_list = list(comports())
        return self.com_list

    # Initalize the serial connection
    def connect(self, port):
        print("connection started")
        self.ser = serial.Serial(port, 115200, timeout=self.timeout_interval)
        self.connected = True
        self.thread = threading.Thread(target=self.coms_looper, args=())
        self.thread.start()

    # Setting reference to ventricle graph
    def set_vent_graph(self, graph):
        self.vent_graph = graph

    # Setting reference to atrium graph
    def set_atr_graph(self, graph):
        self.atr_graph = graph