import wx
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class ProjectileApp(wx.Frame):
    def __init__(self, parent, title):
        super(ProjectileApp, self).__init__(parent, title=title, size=(400, 400))

        panel = wx.Panel(self)

        wx.StaticText(panel, label="Начальная скорость (м/с):", pos=(20, 20))
        self.speed_input = wx.TextCtrl(panel, pos=(200, 20))

        wx.StaticText(panel, label="Угол (градусы):", pos=(20, 60))
        self.angle_input = wx.TextCtrl(panel, pos=(200, 60))

        wx.StaticText(panel, label="Высота (м):", pos=(20, 100))
        self.height_input = wx.TextCtrl(panel, pos=(200, 100))

        wx.StaticText(panel, label="Коэффициент сопротивление среды (k):", pos=(20, 140))
        self.resistance_input = wx.TextCtrl(panel, pos=(250, 140))

        plot_button = wx.Button(panel, label="Построить график", pos=(20, 200))
        plot_button.Bind(wx.EVT_BUTTON, self.on_plot)

        self.Show()

    def on_plot(self, event):
        try:

            initial_speed = float(self.speed_input.GetValue())
            launch_angle = float(self.angle_input.GetValue())
            initial_height = float(self.height_input.GetValue())
            air_resistance = float(self.resistance_input.GetValue())

            if initial_speed <= 0 or initial_height < 0 or air_resistance < 0:
                wx.MessageBox("Введите неотрицательные значения.",
                              "Ошибка ввода", wx.OK | wx.ICON_ERROR)
                return

            self.plot_trajectory(initial_speed, launch_angle, initial_height, air_resistance)

        except ValueError:
            wx.MessageBox("Некорректный ввод.", "Ошибка ввода", wx.OK | wx.ICON_ERROR)

    def plot_trajectory(self, initial_speed, launch_angle, initial_height, air_resistance):
        g = 10

        launch_angle_rad = np.radians(launch_angle)
        v_x0 = initial_speed * np.cos(launch_angle_rad)
        v_y0 = initial_speed * np.sin(launch_angle_rad)

        def equations(t, y):
            x, y_pos, v_x, v_y = y
            speed = np.sqrt(v_x**2 + v_y**2)
            dv_xdt = -air_resistance * v_x
            dv_ydt = -g - air_resistance * v_y
            return [v_x, v_y, dv_xdt, dv_ydt]

        y0 = [0, initial_height, v_x0, v_y0]
        t_span = (0, 10)
        t_eval = np.linspace(0, 10, 500)

        solution = solve_ivp(equations, t_span, y0, t_eval=t_eval, method="RK45")
        x = solution.y[0]
        y_pos = solution.y[1]
        v_x = solution.y[2]
        v_y = solution.y[3]
        t = solution.t

        speed = np.sqrt(v_x**2 + v_y**2)

        fig, axs = plt.subplots(3, 1, figsize=(8, 12))
        plt.subplots_adjust(hspace=0.4)
        fig.suptitle("Движения тела с учетом сопротивления воздуха")

        axs[0].plot(x, y_pos, label="Траектория")
        axs[0].set_xlabel("X, м")
        axs[0].set_ylabel("Y, м")
        axs[0].set_ylim(bottom=0)
        axs[0].legend()
        axs[0].grid()

        axs[1].plot(t, speed, label="Скорость", color='purple')
        axs[1].set_xlabel("t, с")
        axs[1].set_ylabel("v, м/с")
        axs[1].legend()
        axs[1].grid()

        axs[2].plot(t, x, label="координата x", color='blue')
        axs[2].plot(t, y_pos, label="координата y", color='red')
        axs[2].set_ylim(bottom=0)
        axs[2].set_xlabel("t, с")
        axs[2].set_ylabel("Позиция, м")
        axs[2].legend()
        axs[2].grid()

        plot_frame = wx.Frame(None, title="Моделирование движения тела", size=(800, 800))
        canvas = FigureCanvas(plot_frame, -1, fig)
        plot_frame.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = ProjectileApp(None, "Моделирование движения тела с учетом сопротивления воздуха")
    app.MainLoop()
