import numpy as np
import tkinter as tk
from tkinter import messagebox, Canvas

def solve_circuit_gui():
    def add_resistor():
        try:
            r = float(entry_resistance.get())
            n1 = int(entry_r_node1.get())
            n2 = int(entry_r_node2.get())
            resistors.append((r, n1, n2))
            listbox_resistors.insert(tk.END, f"R: {r} Ом, узлы: {n1}-{n2}")
            update_max_node()
            draw_circuit()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные значения для резистора.")

    def add_source():
        try:
            v = float(entry_voltage.get())
            n1 = int(entry_v_node1.get())
            n2 = int(entry_v_node2.get())
            sources.append((v, n1, n2))
            listbox_sources.insert(tk.END, f"E: {v} В, узлы: {n1}-{n2}")
            update_max_node()
            draw_circuit()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные значения для источника.")

    def calculate():
        try:
            if len(resistors) == 0 and len(sources) == 0:
                messagebox.showerror("Ошибка", "Схема не содержит резисторов или источников.")
                return

            num_nodes = max([0] + [n for _, n1, n2 in resistors + sources for n in (n1, n2)])
            
            if num_nodes == 0:
                messagebox.showerror("Ошибка", "Нет узлов для расчета.")
                return

            G, I = create_admittance_matrix(resistors, sources, num_nodes)

            potentials = np.linalg.solve(G, I)

            result_text = "Рассчитанные потенциалы узлов:\n"
            for i, p in enumerate(potentials):
                result_text += f"Узел {i+1}: {p:.4f} В\n"

            result_text += "\nТоки через резисторы:\n"
            for i, (r, n1, n2) in enumerate(resistors):
                v1 = potentials[n1-1] if n1 != 0 else 0
                v2 = potentials[n2-1] if n2 != 0 else 0
                current = (v1 - v2) / r 
                result_text += f"I{i+1}: {current:.4f} A\n"

            messagebox.showinfo("Результат", result_text)

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные параметры схемы.")
        except np.linalg.LinAlgError:
            messagebox.showerror("Ошибка", "Матрица проводимостей вырождена. Проверьте конфигурацию схемы.")

    def create_admittance_matrix(resistors, sources, num_nodes):
        G = np.zeros((num_nodes, num_nodes))
        I = np.zeros(num_nodes)

        for r, n1, n2 in resistors:
            g = 1 / r
            if n1 != 0:
                G[n1-1, n1-1] += g
            if n2 != 0:
                G[n2-1, n2-1] += g
            if n1 != 0 and n2 != 0:
                G[n1-1, n2-1] -= g
                G[n2-1, n1-1] -= g

        for v, n1, n2 in sources:
            if n1 != 0:
                I[n1-1] += v
            if n2 != 0:
                I[n2-1] -= v

        return G, I

    def update_max_node():
        nonlocal max_node
        max_node = max([0] + [n for _, n1, n2 in resistors + sources for n in (n1, n2)])
        draw_circuit()

    def draw_circuit():
        canvas.delete("all")
        node_positions = {}
        radius = 20

        x_spacing = 150
        y_spacing = 100

        rows = (max_node + 3) // 4
        for n in range(1, max_node + 1):
            row = (n - 1) // 4
            col = (n - 1) % 4
            x = 50 + col * x_spacing
            y = 50 + row * y_spacing
            node_positions[n] = (x, y)
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue")
            canvas.create_text(x, y, text=str(n))

        for r, n1, n2 in resistors:
            x1, y1 = node_positions.get(n1, (0, 0))
            x2, y2 = node_positions.get(n2, (0, 0))
            if n1 == 0 or n2 == 0:
                x2, y2 = (x1 + 50, y1 + 50)

            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            offset = 20
            canvas.create_line(x1, y1, mid_x + offset, mid_y - offset, fill="black")
            canvas.create_line(mid_x + offset, mid_y - offset, x2, y2, fill="black")

            canvas.create_text(mid_x + offset, mid_y - offset - 10, text=f"R={r}")

        for v, n1, n2 in sources:
            x1, y1 = node_positions.get(n1, (0, 0))
            x2, y2 = node_positions.get(n2, (0, 0))
            if n1 == 0 or n2 == 0:
                x2, y2 = (x1 + 50, y1 - 50)

            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            offset = -20
            canvas.create_line(x1, y1, mid_x + offset, mid_y - offset, fill="red", dash=(4, 2))
            canvas.create_line(mid_x + offset, mid_y - offset, x2, y2, fill="red", dash=(4, 2))

            canvas.create_text(mid_x + offset, mid_y - offset - 10, text=f"E={v}", fill="red")

    root = tk.Tk()
    root.title("Расчет электрической схемы")

    resistors = []
    sources = []

    max_node = 0

    frame_resistors = tk.LabelFrame(root, text="Резисторы")
    frame_resistors.grid(row=0, column=0, padx=10, pady=10)

    tk.Label(frame_resistors, text="Сопротивление (Ом):").grid(row=0, column=0)
    entry_resistance = tk.Entry(frame_resistors)
    entry_resistance.grid(row=0, column=1)

    tk.Label(frame_resistors, text="Узел 1:").grid(row=1, column=0)
    entry_r_node1 = tk.Entry(frame_resistors)
    entry_r_node1.grid(row=1, column=1)

    tk.Label(frame_resistors, text="Узел 2:").grid(row=2, column=0)
    entry_r_node2 = tk.Entry(frame_resistors)
    entry_r_node2.grid(row=2, column=1)

    tk.Button(frame_resistors, text="Добавить резистор", command=add_resistor).grid(row=3, column=0, columnspan=2)

    listbox_resistors = tk.Listbox(frame_resistors, width=40, height=10)
    listbox_resistors.grid(row=4, column=0, columnspan=2)

    frame_sources = tk.LabelFrame(root, text="Источники напряжения")
    frame_sources.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame_sources, text="Напряжение (В):").grid(row=0, column=0)
    entry_voltage = tk.Entry(frame_sources)
    entry_voltage.grid(row=0, column=1)

    tk.Label(frame_sources, text="Узел 1:").grid(row=1, column=0)
    entry_v_node1 = tk.Entry(frame_sources)
    entry_v_node1.grid(row=1, column=1)

    tk.Label(frame_sources, text="Узел 2:").grid(row=2, column=0)
    entry_v_node2 = tk.Entry(frame_sources)
    entry_v_node2.grid(row=2, column=1)

    tk.Button(frame_sources, text="Добавить источник", command=add_source).grid(row=3, column=0, columnspan=2)

    listbox_sources = tk.Listbox(frame_sources, width=40, height=10)
    listbox_sources.grid(row=4, column=0, columnspan=2)

    tk.Button(root, text="Рассчитать", command=calculate).grid(row=1, column=0, columnspan=2, pady=10)

    canvas = Canvas(root, width=800, height=400, bg="white")
    canvas.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    solve_circuit_gui()
