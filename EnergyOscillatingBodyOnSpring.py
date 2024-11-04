import wx
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class EnergyPlotApp(wx.Frame):
    def __init__(self, parent, title):
        super(EnergyPlotApp, self).__init__(parent, title=title, size=(400, 300))

        panel = wx.Panel(self)

        wx.StaticText(panel, label="Масса (кг):", pos=(20, 20))
        self.mass_input = wx.TextCtrl(panel, pos=(150, 20))

        wx.StaticText(panel, label="Коэффициент упругости (Н/м):", pos=(20, 60))
        self.spring_input = wx.TextCtrl(panel, pos=(230, 60))

        wx.StaticText(panel, label="Коэффициент сопротивления среды:", pos=(20, 100))
        self.damping_input = wx.TextCtrl(panel, pos=(230, 100))

        plot_button = wx.Button(panel, label="Построить графики", pos=(20, 150))
        plot_button.Bind(wx.EVT_BUTTON, self.on_plot)

        self.Show()

    def on_plot(self, event):
        try:
            m = float(self.mass_input.GetValue())
            k = float(self.spring_input.GetValue())
            b = float(self.damping_input.GetValue())
            
            if m <= 0 or k <= 0 or b < 0:
                wx.MessageBox("Введите положительные значения.", 
                              "Ошибка ввода", wx.OK | wx.ICON_ERROR)
                return
            
            self.plot_energy_graphs(m, k, b)
            
        except ValueError:
            wx.MessageBox("Введите корректные значения.", "Ошибка ввода", wx.OK | wx.ICON_ERROR)

    def plot_energy_graphs(self, m, k, b):
        def equation(t, y):
            x, v = y
            dxdt = v
            dvdt = -(b / m) * v - (k / m) * x
            return [dxdt, dvdt]

        y0 = [1.0, 0.0]
        t_span = (0, 20)
        t_eval = np.linspace(0, 20, 500)

        solution = solve_ivp(equation, t_span, y0, t_eval=t_eval)
        x = solution.y[0]
        v = solution.y[1]
        t = solution.t

        kinetic_energy = m * v**2 / 2
        potential_energy = k * x**2 / 2
        total_energy = kinetic_energy + potential_energy

        fig, axs = plt.subplots(3, 1, figsize=(8, 10))
        plt.subplots_adjust(hspace=0.4)
        fig.suptitle("Зависимость энергий от времени")

        axs[0].plot(t, kinetic_energy, label="Кинетическая энергия")
        axs[0].set_ylabel("E, Дж")
        axs[0].set_xlabel("t, c")
        axs[0].legend()
        axs[0].grid()

        axs[1].plot(t, potential_energy, label="Потенциальная энергия", color='orange')
        axs[1].set_ylabel("Ek, Дж")
        axs[1].set_xlabel("t, c")
        axs[1].legend()
        axs[1].grid()

        axs[2].plot(t, total_energy, label="Полная механическая энергия", color='green')
        axs[2].set_ylabel("Eмех, Дж")
        axs[2].set_xlabel("t, c")
        axs[2].legend()
        axs[2].grid()

        energy_plot_frame = wx.Frame(None, title="Графики", size=(800, 800))
        canvas = FigureCanvas(energy_plot_frame, -1, fig)
        energy_plot_frame.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = EnergyPlotApp(None, "Визуализация колебания на пружине")
    app.MainLoop()
