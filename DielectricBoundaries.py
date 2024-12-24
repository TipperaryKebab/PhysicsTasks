import wx
import math
import matplotlib.pyplot as plt
import numpy as np

class DielectricBoundaryApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Граничные условия на границе диэлектриков", size=(700, 600))
        
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.param_sizer = wx.BoxSizer(wx.VERTICAL)

        self.epsilon1_input = self.create_input(panel, "Диэлектрическая проницаемость среды 1 (ε1):")
        self.epsilon2_input = self.create_input(panel, "Диэлектрическая проницаемость среды 2 (ε2):")
        self.magnitude_input = self.create_input(panel, "Модуль поля (|E| или |D|):")
        self.angle_input = self.create_input(panel, "Угол относительно нормали (°):")

        self.sizer.Add(self.param_sizer, 0, wx.ALL | wx.EXPAND, 10)

        self.calculate_btn = wx.Button(panel, label="Рассчитать")
        self.calculate_btn.Bind(wx.EVT_BUTTON, self.calculate_and_plot)
        self.sizer.Add(self.calculate_btn, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(self.sizer)
        self.Show()

    def create_input(self, panel, label_text):
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, label=label_text)
        text_ctrl = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        input_sizer.Add(label, 0, wx.ALL | wx.CENTER, 5)
        input_sizer.Add(text_ctrl, 1, wx.ALL | wx.CENTER, 5)
        self.param_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 5)
        return text_ctrl

    def calculate_and_plot(self, event):
        try:
            epsilon1 = float(self.epsilon1_input.GetValue())
            epsilon2 = float(self.epsilon2_input.GetValue())
            magnitude = float(self.magnitude_input.GetValue())
            angle_deg = float(self.angle_input.GetValue())

            angle_rad = np.radians(angle_deg)

            E1_normal = magnitude * np.cos(angle_rad)
            E1_tangential = magnitude * np.sin(angle_rad)

            E2_normal = (epsilon1 / epsilon2) * E1_normal
            E2_tangential = E1_tangential

            E2_magnitude = np.sqrt(E2_normal**2 + E2_tangential**2)
            E2_angle_rad = np.arctan2(E2_tangential, E2_normal)
            E2_angle_deg = np.degrees(E2_angle_rad)

            self.plot_fields(
                epsilon1, epsilon2, magnitude, angle_deg, 
                E2_magnitude, E2_angle_deg
            )
        except ValueError:
            wx.MessageBox("Неправильный формат ввода.", "Ошибка ввода", wx.OK | wx.ICON_ERROR)

    def plot_fields(self, epsilon1, epsilon2, E1_magnitude, E1_angle_deg, E2_magnitude, E2_angle_deg):
        fig, ax = plt.subplots(figsize=(8, 6))

        ax.axhline(0, color='black', linewidth=1, linestyle='--', label="Граница раздела")

        E1_angle_rad = np.radians(E1_angle_deg) + np.pi
        ax.arrow(
            -E1_magnitude * math.sin(E1_angle_rad),
            E1_magnitude * math.cos(E1_angle_rad), 
            E1_magnitude * np.sin(E1_angle_rad), 
            -E1_magnitude * np.cos(E1_angle_rad), 
            head_width=0.2, color='blue', label=f"Поле в среде 1 (|E| = {E1_magnitude})"
        )

        E2_angle_rad = np.radians(E2_angle_deg)
        ax.arrow(
            0, 0, 
            -E2_magnitude * np.sin(E2_angle_rad), 
            E2_magnitude * np.cos(E2_angle_rad), 
            head_width=0.2, color='green', label=f"Поле в среде 2 (|E| = {E2_magnitude:.2f})"
        )

        ax.text(-1.5, -0.5, f"Среда 1 (ε = {epsilon1})", fontsize=10, color='blue')
        ax.text(-1.5, 0.5, f"Среда 2 (ε = {epsilon2})", fontsize=10, color='green')

        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect('equal', adjustable='box')
        ax.set_title("Преломление электрического поля на границе диэлектриков")
        ax.set_xlabel("X, м")
        ax.set_ylabel("Y, м")
        ax.legend()
        plt.grid()
        plt.show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = DielectricBoundaryApp()
    app.MainLoop()
