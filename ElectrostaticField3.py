import wx
import matplotlib.pyplot as plt
import numpy as np

class ElectricFieldApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Электростатическое поле точечных зарядов", size=(700, 600))
        
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Button controls
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_charge_btn = wx.Button(panel, label="Добавить заряд")
        self.remove_charge_btn = wx.Button(panel, label="Удалить заряд")
        self.add_dipole_btn = wx.Button(panel, label="Добавить диполь")
        self.remove_dipole_btn = wx.Button(panel, label="Удалить диполь")
        self.calculate_btn = wx.Button(panel, label="Рассчитать поле")
        
        button_sizer.Add(self.add_charge_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.remove_charge_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.add_dipole_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.remove_dipole_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.calculate_btn, 0, wx.ALL, 5)
        
        self.sizer.Add(button_sizer, 0, wx.CENTER)
        
        self.charges_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dipoles_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.sizer.Add(wx.StaticText(panel, label="Заряды:"), 0, wx.ALL, 5)
        self.sizer.Add(self.charges_sizer, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer.Add(wx.StaticText(panel, label="Диполи:"), 0, wx.ALL, 5)
        self.sizer.Add(self.dipoles_sizer, 1, wx.EXPAND | wx.ALL, 10)

        # Results display
        self.results_display = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 100))
        self.sizer.Add(wx.StaticText(panel, label="Результаты:"), 0, wx.ALL, 5)
        self.sizer.Add(self.results_display, 0, wx.EXPAND | wx.ALL, 10)

        self.charge_inputs = []
        self.dipole_inputs = []

        self.add_charge_input(panel)
        
        self.add_charge_btn.Bind(wx.EVT_BUTTON, self.add_charge_input)
        self.remove_charge_btn.Bind(wx.EVT_BUTTON, self.remove_charge_input)
        self.add_dipole_btn.Bind(wx.EVT_BUTTON, self.add_dipole_input)
        self.remove_dipole_btn.Bind(wx.EVT_BUTTON, self.remove_dipole_input)
        self.calculate_btn.Bind(wx.EVT_BUTTON, self.calculate_field)
        
        panel.SetSizer(self.sizer)
        self.Show()

    def add_charge_input(self, event=None):
        panel = self.GetChildren()[0]
        charge_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        x_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        y_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        q_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        
        charge_sizer.Add(wx.StaticText(panel, label="x (м):"), 0, wx.ALL | wx.CENTER, 5)
        charge_sizer.Add(x_input, 1, wx.ALL, 5)
        charge_sizer.Add(wx.StaticText(panel, label="y (м):"), 0, wx.ALL | wx.CENTER, 5)
        charge_sizer.Add(y_input, 1, wx.ALL, 5)
        charge_sizer.Add(wx.StaticText(panel, label="q (Кл):"), 0, wx.ALL | wx.CENTER, 5)
        charge_sizer.Add(q_input, 1, wx.ALL, 5)
        
        self.charges_sizer.Add(charge_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.charge_inputs.append((x_input, y_input, q_input))
        self.sizer.Layout()

    def remove_charge_input(self, event=None):
        if self.charge_inputs:
            inputs = self.charge_inputs.pop()
            for input_field in inputs:
                input_field.Destroy()
            self.sizer.Layout()

    def add_dipole_input(self, event=None):
        panel = self.GetChildren()[0]
        dipole_sizer = wx.BoxSizer(wx.HORIZONTAL)

        x_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        y_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        p_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        angle_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)

        dipole_sizer.Add(wx.StaticText(panel, label="x (м):"), 0, wx.ALL | wx.CENTER, 5)
        dipole_sizer.Add(x_input, 1, wx.ALL, 5)
        dipole_sizer.Add(wx.StaticText(panel, label="y (м):"), 0, wx.ALL | wx.CENTER, 5)
        dipole_sizer.Add(y_input, 1, wx.ALL, 5)
        dipole_sizer.Add(wx.StaticText(panel, label="p (Кл·м):"), 0, wx.ALL | wx.CENTER, 5)
        dipole_sizer.Add(p_input, 1, wx.ALL, 5)
        dipole_sizer.Add(wx.StaticText(panel, label="угол (°):"), 0, wx.ALL | wx.CENTER, 5)
        dipole_sizer.Add(angle_input, 1, wx.ALL, 5)

        self.dipoles_sizer.Add(dipole_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.dipole_inputs.append((x_input, y_input, p_input, angle_input))
        self.sizer.Layout()

    def remove_dipole_input(self, event=None):
        if self.dipole_inputs:
            inputs = self.dipole_inputs.pop()
            for input_field in inputs:
                input_field.Destroy()
            self.sizer.Layout()

    def calculate_field(self, event):
        charges = []
        for x_input, y_input, q_input in self.charge_inputs:
            try:
                x = float(x_input.GetValue())
                y = float(y_input.GetValue())
                q = float(q_input.GetValue())
                charges.append((x, y, q))
            except ValueError:
                wx.MessageBox("Неправильный формат ввода.", "Ошибка ввода", wx.OK | wx.ICON_ERROR)
                return

        dipoles = []
        for x_input, y_input, p_input, angle_input in self.dipole_inputs:
            try:
                x = float(x_input.GetValue())
                y = float(y_input.GetValue())
                p = float(p_input.GetValue())
                angle = np.radians(float(angle_input.GetValue()))
                dipoles.append((x, y, p, angle))
            except ValueError:
                wx.MessageBox("Неправильный формат ввода.", "Ошибка ввода", wx.OK | wx.ICON_ERROR)
                return

        if charges or dipoles:
            self.plot_field(charges, dipoles)

    def plot_field(self, charges, dipoles):

        def calculate_field(charges, x_range, y_range, grid_size=100):
            k_e = 8.987551787e9
            x = np.linspace(*x_range, grid_size)
            y = np.linspace(*y_range, grid_size)
            X, Y = np.meshgrid(x, y)
            Ex = np.zeros_like(X)
            Ey = np.zeros_like(Y)
            Phi = np.zeros_like(X)

            for (x_c, y_c, q) in charges:
                r = np.sqrt((X - x_c)**2 + (Y - y_c)**2)
                r_hat_x = (X - x_c) / r
                r_hat_y = (Y - y_c) / r
                r[r == 0] = np.inf
                Ex += k_e * q * r_hat_x / r**2
                Ey += k_e * q * r_hat_y / r**2
                Phi += k_e * q / r

            for (x_d, y_d, p, theta) in dipoles:
                r = np.sqrt((X - x_d)**2 + (Y - y_d)**2)
                r_hat_x = (X - x_d) / r
                r_hat_y = (Y - y_d) / r
                r[r == 0] = np.inf

                px = p * np.cos(theta)
                py = p * np.sin(theta)

                p_dot_r = px * r_hat_x + py * r_hat_y

                Ex += k_e * (3 * p_dot_r * r_hat_x - px) / r**3
                Ey += k_e * (3 * p_dot_r * r_hat_y - py) / r**3    
            return X, Y, Ex, Ey, Phi

        def calculate_dipole_force_moment(dipole, Ex, Ey, X, Y):
            x, y, p, theta = dipole
            idx = (np.abs(X[0] - x)).argmin()
            idy = (np.abs(Y[:, 0] - y)).argmin()

            E_dipole = np.array([Ex[idy, idx], Ey[idy, idx]])
            p_vector = np.array([p * np.cos(theta), p * np.sin(theta)])
            
            force = E_dipole * p
            torque = np.cross(p_vector, E_dipole)
            return force, torque

        X, Y, Ex, Ey, Phi = calculate_field(charges, x_range=(-5, 5), y_range=(-5, 5))

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.quiver(X, Y, Ex, Ey, color='blue', pivot='middle', scale=1e12, width=0.002, label='Векторное поле')
        ax.streamplot(X, Y, Ex, Ey, color=np.sqrt(Ex**2 + Ey**2), cmap="viridis", density=1.5, linewidth=1)
        contour = ax.contour(X, Y, Phi, levels=20, colors="red", linewidths=0.8)
        ax.clabel(contour, inline=1, fontsize=8, fmt="%.1e")
        filled_contour = ax.contourf(X, Y, Phi, levels=50, cmap="RdYlBu", alpha=0.8)
        plt.colorbar(filled_contour, label="Потенциал (В)")

        results = []

        for dipole in dipoles:
            x, y, p, theta = dipole
            force, torque = calculate_dipole_force_moment(dipole, Ex, Ey, X, Y)
            ax.arrow(x, y, 0.2 * np.cos(theta), 0.2 * np.sin(theta), head_width=0.1, color='magenta', label='Диполь')
            results.append(f"Диполь в ({x:.1f}, {y:.1f}): Сила = {force}, Момент = {torque:.2e}")

        self.results_display.SetValue("\n".join(results))

        ax.set_title("Электростатическое поле с диполями")
        ax.set_xlabel("X, м")
        ax.set_ylabel("Y, м")
        ax.legend(loc='upper right')
        plt.show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = ElectricFieldApp()
    app.MainLoop()
