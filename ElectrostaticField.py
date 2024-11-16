import wx
import matplotlib.pyplot as plt
import numpy as np

class ElectricFieldApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Электростатическое поле точечных зарядов", size=(600, 500))
        
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_charge_btn = wx.Button(panel, label="Добавить заряд")
        self.remove_charge_btn = wx.Button(panel, label="Удалить заряд")
        self.calculate_btn = wx.Button(panel, label="Рассчитать поле")
        
        button_sizer.Add(self.add_charge_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.remove_charge_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.calculate_btn, 0, wx.ALL, 5)
        
        self.sizer.Add(button_sizer, 0, wx.CENTER)
        
        self.charges_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.charges_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        self.charge_inputs = []
        self.add_charge_input(panel)
        
        self.add_charge_btn.Bind(wx.EVT_BUTTON, self.add_charge_input)
        self.remove_charge_btn.Bind(wx.EVT_BUTTON, self.remove_charge_input)
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

    def calculate_field(self, event):
        charges = []
        for x_input, y_input, q_input in self.charge_inputs:
            try:
                x = float(x_input.GetValue())
                y = float(y_input.GetValue())
                q = float(q_input.GetValue())
                charges.append((x, y, q))
            except ValueError:
                wx.MessageBox("Неправильный формал ввода.", "Ошибка ввода", wx.OK | wx.ICON_ERROR)
                return

        if charges:
            self.plot_field(charges)

    def plot_field(self, charges):

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
            return X, Y, Ex, Ey, Phi

        X, Y, Ex, Ey, Phi = calculate_field(charges, x_range=(-5, 5), y_range=(-5, 5))

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.quiver(X, Y, Ex, Ey, color='blue', pivot='middle', scale=1e12, width=0.002)
        contour = ax.contourf(X, Y, Phi, levels=50, cmap="RdYlBu")
        plt.colorbar(contour, label="Потенциал (В)")
        ax.set_title("Электростатическое поле")
        ax.set_xlabel("X, м")
        ax.set_ylabel("Y, м")
        plt.show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = ElectricFieldApp()
    app.MainLoop()
