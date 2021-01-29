import tkinter as tk

# Static values of graphs
ranges = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 4000]
acceptable_y = 11
acceptable_x = 11


# Function to create the ticks on the graph
def create_ticks(canv, rh, rl, x_off, y_off, line, ranges, a, c_line, horz):
    ran = rh - rl
    ticks = 1
    for s in ranges:
        t_ticks = ran / s
        ticks = s
        if t_ticks < a:
            break
    f_tick = rh
    if f_tick % ticks:
        f_tick = f_tick - f_tick % ticks
    n_tick = float(line) / ran * (rh % ticks)
    i_tick = float(line) / ran * ticks
    ci = 0
    if horz:
        while f_tick - ticks * ci >= rl:
            num = int(f_tick - ticks * ci)
            canv.create_text(int(x_off + line - n_tick - i_tick * ci), y_off + c_line + 10, text=str(num))
            canv.create_line(int(x_off + line - n_tick - i_tick * ci), y_off + c_line,
                             int(x_off + line - n_tick - i_tick * ci), y_off + 5 + c_line, fill='#000000', width=1)
            ci += 1
    else:
        while f_tick - ticks * ci >= rl:
            num = int(f_tick - ticks * ci)
            if num == 0:
                canv.create_line(x_off, int(y_off + n_tick + i_tick * ci), x_off + c_line,
                                 int(y_off + n_tick + i_tick * ci), fill='#006A71', width=1)
            canv.create_text(40, int(y_off + n_tick + i_tick * ci), text=str(num))
            canv.create_line(x_off - 5, int(y_off + n_tick + i_tick * ci), x_off, int(y_off + n_tick + i_tick * ci),
                             fill='#000000', width=1)
            ci += 1


#Graph Class
class Graph(tk.Frame):
    def __init__(self, reference, canv_h, canv_w, name):
        super(Graph, self).__init__()
        # Saving reference to gui
        self.reference = reference
        self.name = name
        self.canv = tk.Canvas(self, width=canv_w, height=canv_h)
        self.canv_h = canv_h
        self.canv_w = canv_w
        self.data = [[0, 0]]
        self.y_line = canv_h - 60
        self.x_line = canv_w - 80
        self.x_off = 60
        self.y_off = 20
        self.mx = 0
        self.my = 0

        self.scale_hy = float(1000)
        self.scale_ly = float(-1000)
        self.scale_hx = float(4000)
        self.scale_lx = float(0)

        self.draw()

        # Biding mouse event handlers
        self.canv.bind("<B1-Motion>", self.graph_drag)
        self.canv.bind("<Button-1>", self.graph_down)
        self.canv.bind("<MouseWheel>", self.graph_scroll)
        self.canv.pack()
        self.pack()

    # Function to draw the graph
    def draw(self):
        # Scaling factor
        self.mod_y = self.y_line / (self.scale_hy - self.scale_ly)
        self.mod_x = self.x_line / (self.scale_hx - self.scale_lx)
        # Background and factor
        self.canv.create_rectangle(0, 0, self.canv_w, self.canv_h, fill='#C6C6C6')
        self.canv.create_line(self.x_off, self.y_off + self.y_line, self.x_off + self.x_line, self.y_off + self.y_line,fill='#000000', width=2)
        self.canv.create_line(self.x_off, self.y_off, self.x_off, self.y_off + self.y_line, fill='#000000', width=2)
        # Creating the scale / ticks
        create_ticks(canv=self.canv, rh=self.scale_hy, rl=self.scale_ly, x_off=self.x_off, y_off=self.y_off,line=self.y_line, c_line=self.x_line,ranges=ranges, a=acceptable_y, horz=False)
        create_ticks(canv=self.canv, rh=self.scale_hx, rl=self.scale_lx, x_off=self.x_off, y_off=self.y_off,line=self.x_line, c_line=self.y_line,ranges=ranges, a=acceptable_x, horz=True)
        # Draw the title and labels
        self.canv.create_text(self.canv_w/2, 10, text=self.name)
        self.canv.create_text(self.canv_w / 2, self.canv_h-10, text="Time (ms)")
        self.canv.create_text(10, self.canv_h/2, text="Amplitude (mv)", angle=90)
        # Plot the points
        self.plot()

    # Plot the points on the graph
    def plot(self):
        for i in range(len(self.data) - 1):
            if self.scale_lx <= self.data[i][0] <= self.scale_hx and self.scale_lx <= self.data[i + 1][0] <= self.scale_hx:
                if self.scale_ly <= self.data[i][1] <= self.scale_hy and self.scale_ly <= self.data[i + 1][1] <= self.scale_hy:
                    cx = (self.data[i][0] - self.scale_lx) * self.mod_x + self.x_off
                    nx = (self.data[i + 1][0] - self.scale_lx) * self.mod_x + self.x_off
                    cy = (self.scale_hy - self.data[i][1]) * self.mod_y + self.y_off
                    ny = (self.scale_hy - self.data[i + 1][1]) * self.mod_y + self.y_off
                    self.canv.create_line(int(cx), int(cy), int(nx), int(ny), fill='#710700', width=1)

    # On mouse drag over graph
    def graph_drag(self, event):
        dmx = event.x - self.mx
        dmy = event.y - self.my
        rdx = dmx/self.x_line * (self.scale_hx - self.scale_lx)
        rdy = dmy/self.y_line * (self.scale_hy - self.scale_ly)
        xr = self.scale_hx - self.scale_lx
        self.scale_hx -= rdx
        self.scale_lx -= rdx
        if self.scale_lx < 0:
            self.scale_lx = 0
            self.scale_hx = xr
        self.scale_hy += rdy
        self.scale_ly += rdy
        self.draw()
        self.mx = event.x
        self.my = event.y

    # On mouse down on the graph
    def graph_down(self, event):
        if self.x_off <= event.x <= self.x_off + self.x_line and self.y_off <= event.y <= self.y_off + self.y_line:
            self.mx = event.x
            self.my = event.y

    # On mouse scroll on the graph
    def graph_scroll(self, event):
        if self.x_off <= event.x <= self.x_off + self.x_line and self.y_off <= event.y <= self.y_off + self.y_line:
            percx = (event.x-self.x_off)/self.x_line
            percy = (event.y-self.y_off)/self.y_line
            if event.delta < 0:
                cyrange = self.scale_hy-self.scale_ly
                nyrange = cyrange*1.25
                dyrange = (nyrange - cyrange)
                cxrange = self.scale_hx - self.scale_lx
                nxrange = cxrange * 1.25
                dxrange = (nxrange - cxrange)
                self.scale_hy = self.scale_hy + dyrange * percy
                self.scale_ly = self.scale_ly - dyrange * (1-percy)
                self.scale_hx = self.scale_hx + dxrange * (1-percx)
                self.scale_lx = self.scale_lx - dxrange * percx
                if self.scale_lx < 0:
                    self.scale_lx = 0
                    self.scale_hx = nxrange
                self.draw()

            else:
                cyrange = self.scale_hy - self.scale_ly
                nyrange = cyrange * 0.80
                dyrange = (nyrange - cyrange)
                cxrange = self.scale_hx - self.scale_lx
                nxrange = cxrange * 0.80
                dxrange = (nxrange - cxrange)
                self.scale_hy = self.scale_hy + dyrange * percy
                self.scale_ly = self.scale_ly - dyrange * (1-percy)
                self.scale_hx = self.scale_hx + dxrange * (1-percx)
                self.scale_lx = self.scale_lx - dxrange * percx
                if self.scale_lx < 0:
                    self.scale_lx = 0
                    self.scale_hx = nxrange
                self.draw()

    # Add a point to graph
    def add_point(self, time, y):
        self.data.append([time, y])
        self.draw()

    # Clear the point from graph
    def clear(self):
        self.data = [[0,0]]
        self.scale_hy = float(1000)
        self.scale_ly = float(-1000)
        self.scale_hx = float(4000)
        self.scale_lx = float(0)
        self.draw()