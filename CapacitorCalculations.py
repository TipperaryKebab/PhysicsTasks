import wx

epsilon_0 = 8.854e-12

class CapacitorCalculator(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(400, 400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(panel, label='Напряжение (В):'), flag=wx.RIGHT, border=8)
        self.voltage_input = wx.TextCtrl(panel)
        hbox1.Add(self.voltage_input, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(panel, label='Расстояние (м):'), flag=wx.RIGHT, border=8)
        self.distance_input = wx.TextCtrl(panel)
        hbox2.Add(self.distance_input, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(wx.StaticText(panel, label='Диэлектрическая проницаемость:'), flag=wx.RIGHT, border=8)
        self.dielectric_input = wx.TextCtrl(panel)
        hbox3.Add(self.dielectric_input, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(wx.StaticText(panel, label='Площадь пластин (м²):'), flag=wx.RIGHT, border=8)
        self.area_input = wx.TextCtrl(panel)
        hbox4.Add(self.area_input, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.connection_status = wx.CheckBox(panel, label='Подключен к источнику питания')
        hbox5.Add(self.connection_status)
        vbox.Add(hbox5, flag=wx.LEFT|wx.TOP, border=10)

        self.calculate_button = wx.Button(panel, label='Рассчитать')
        self.calculate_button.Bind(wx.EVT_BUTTON, self.calculate)
        vbox.Add(self.calculate_button, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.result_text = wx.StaticText(panel, label='Результаты появятся здесь')
        vbox.Add(self.result_text, flag=wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        panel.SetSizer(vbox)

    def calculate(self, event):
        try:
            voltage = float(self.voltage_input.GetValue())
            distance = float(self.distance_input.GetValue())
            dielectric = float(self.dielectric_input.GetValue())
            area = float(self.area_input.GetValue())
            connected = self.connection_status.GetValue()

            capacitance = epsilon_0 * dielectric * area / distance

            if connected:
                charge = capacitance * voltage
                field_strength = voltage / distance
            else:
                charge = capacitance * voltage
                field_strength = charge / (epsilon_0 * dielectric * area)

            self.result_text.SetLabelText(
                f'Ёмкость: {capacitance:.2e} Ф\n'
                f'Напряженность поля: {field_strength:.2e} В/м\n'
                f'Заряд на пластинах: {charge:.2e} Кл'
            )
        except ValueError:
            self.result_text.SetLabelText('Ошибка: Проверьте правильность ввода.')

if __name__ == '__main__':
    app = wx.App()
    frame = CapacitorCalculator(None, title='Калькулятор параметров конденсатора')
    frame.Show()
    app.MainLoop()
