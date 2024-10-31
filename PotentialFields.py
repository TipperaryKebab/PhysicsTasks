import wx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class PotentialFieldApp(wx.Frame):
    def __init__(self, parent, title):
        super(PotentialFieldApp, self).__init__(parent, title=title, size=(400, 300))

        panel = wx.Panel(self)

        wx.StaticText(panel, label="Проекция силы по X (F_x):", pos=(20, 20))
        self.fx_input = wx.TextCtrl(panel, pos=(175, 20), size=(150, -1))

        wx.StaticText(panel, label="Проекция силы по Y (F_y):", pos=(20, 60))
        self.fy_input = wx.TextCtrl(panel, pos=(175, 60), size=(150, -1))

        plot_button = wx.Button(panel, label="График потенциального поля", pos=(20, 100))
        plot_button.Bind(wx.EVT_BUTTON, self.on_plot)

        self.Show()

    def on_plot(self, event):
 
        fx_expr = self.fx_input.GetValue()
        fy_expr = self.fy_input.GetValue()

        try:

            x = np.linspace(-10, 10, 100)
            y = np.linspace(-10, 10, 100)
            X, Y = np.meshgrid(x, y)

            Fx = eval(fx_expr, {"x": X, "y": Y, "np": np})
            Fy = eval(fy_expr, {"x": X, "y": Y, "np": np})

            U = self.calculate_potential(X, Y, Fx, Fy)

            self.plot_potential_field(X, Y, U)

        except Exception as e:
            wx.MessageBox(f"Неправильный формал ввода: {e}", "Ошибка ввода", wx.OK | wx.ICON_ERROR)

    def calculate_potential(self, X, Y, Fx, Fy):
        U = np.zeros_like(X)

        dx = X[0, 1] - X[0, 0]
        dy = Y[1, 0] - Y[0, 0]

        for i in range(1, X.shape[0]):
            U[i, 0] = U[i-1, 0] - Fy[i, 0] * dy
        for j in range(1, X.shape[1]):
            U[:, j] = U[:, j-1] - Fx[:, j] * dx

        return U

    def plot_potential_field(self, X, Y, U):
        fig, ax = plt.subplots(figsize=(8, 6))
        c = ax.contourf(X, Y, U, levels=50, cmap="viridis")
        fig.colorbar(c, ax=ax, label="Потенциальная энергия U(x, y)")
        ax.set_title("Потенциальное поле U(x, y)")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        
        potential_plot_frame = wx.Frame(None, title="Потенциальное поле", size=(800, 800))
        canvas = FigureCanvas(potential_plot_frame, -1, fig)
        potential_plot_frame.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = PotentialFieldApp(None, "Визуализация потенциального поля")
    app.MainLoop()
