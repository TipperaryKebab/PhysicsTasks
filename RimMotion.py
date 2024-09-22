import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import wx
import math
import numpy as np



def dynamicGraph(r, v):
    radius = r
    velocity = v
    period = 2 * math.pi * radius
    SCALING = 1
    if velocity > radius:
        SCALING = velocity
    T = np.arange(0, 50 * period, 0.2 / SCALING)

    fig, ax = plt.subplots()
    ax.set_xlabel("X, м")
    ax.set_xlabel("Y, м")

    line_point, = ax.plot([], [], 'o', label="Точка", color='green')
    line_path, = ax.plot([], [], '-', label="Траектория", color='green')
    ax.grid()

    path_x = []
    path_y = []


    def init():
        line_point.set_data([], [])
        line_path.set_data([], [])
        return line_point, line_path

    def animate(i):

        if i >= len(T):
            return line_point, line_path
        
        x_curr = velocity * T[i] - radius * np.sin(velocity / radius * T[i])
        y_curr = radius - radius * np.cos(velocity / radius * T[i])

        path_x.append(x_curr)
        path_y.append(y_curr)

        line_point.set_data([x_curr], [y_curr])
        line_path.set_data(path_x, path_y)

        ax.set(xlim = (x_curr - period, x_curr + period), ylim = (-0.5 * radius, 2.5 * radius))

        ax.set_aspect('equal')



        return line_point, line_path


    ani = animation.FuncAnimation(fig, animate, init_func = init, frames=len(T), interval = 200 / SCALING, blit=False, repeat=False)

    plt.show()

def staticGraph(r, v):
    radius = r
    velocity = v
    period = 2 * math.pi * radius

    SCALING = 1
    if velocity > radius:
        SCALING = velocity

    T = np.arange(0, 50 * period, 0.2)
    X = np.array([velocity * t - radius * np.sin(velocity / radius * t) for t in T])
    Y = np.array([radius - radius * np.cos(velocity / radius * t) for t in T])
    fig, ax = plt.subplots()
    ax.set_xlabel("X, м")
    ax.set_xlabel("Y, м")
    ax.grid()
    ax.plot(X, Y)


    ax.set(xlim = (-0.5 * period, 2.5 * period), ylim = (-0.5 * radius, 2.5 * radius))

    ax.set_aspect('equal')

    plt.show()

class InputFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(InputFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        lbl_radius = wx.StaticText(panel, label="Радиус (м):")
        self.radius_txt = wx.TextCtrl(panel)
        hbox1.Add(lbl_radius, flag=wx.RIGHT, border=8)
        hbox1.Add(self.radius_txt, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        lbl_velocity = wx.StaticText(panel, label="Скорость центра масс(м/с):")
        self.velocity_txt = wx.TextCtrl(panel)
        hbox2.Add(lbl_velocity, flag=wx.RIGHT, border=8)
        hbox2.Add(self.velocity_txt, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.graph_type = wx.Choice(panel, wx.ID_ANY, choices=["Динамический", "Статический"])
        self.graph_type.SetSelection(0)
        hbox3.Add(self.graph_type, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.btn_proceed = wx.Button(panel, label="Продолжить")
        self.btn_proceed.Bind(wx.EVT_BUTTON, self.on_proceed)
        vbox.Add(self.btn_proceed, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=20)

        panel.SetSizer(vbox)

    def on_proceed(self, event):
        try:
            startRadius = float(self.radius_txt.GetValue())
            startVelocity = float(self.velocity_txt.GetValue())
            graphType = float(self.graph_type.GetSelection())

            if startRadius <= 0:
                wx.MessageBox("Радиус должен быть положительным", "Ошибка", wx.OK | wx.ICON_ERROR)
            elif startVelocity <= 0:
                wx.MessageBox("Скорость должна быть положительной ", "Ошибка", wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox(f"Значения приняты!\Радиус: {startRadius}\Скорость: {startVelocity}",
                              "", wx.OK | wx.ICON_INFORMATION)

            if graphType == 0:
                dynamicGraph(startRadius, startVelocity)
                self.Close()
            else:
                staticGraph(startRadius, startVelocity)
                self.Close()

        except ValueError:
            wx.MessageBox("Неправильный формат ввода.", "Ошибка", wx.OK | wx.ICON_ERROR)

            

class MyApp(wx.App):
    def OnInit(self):
        self.frame = InputFrame(None, title="Движение точки на ободе колеса", size=(300, 250))
        self.frame.Show()
        return True

app = MyApp()
app.MainLoop()