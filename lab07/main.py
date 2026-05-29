import tkinter as tk
from tkinter import messagebox
import random, csv, math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MarkovApp:
    def __init__(self, root):
        self.root = root
        
        self.root.geometry("2000x950")
        self.root.tk.call('tk', 'scaling', 2.0) 
        default_font = ("Arial", 11)
        bold_font = ("Arial", 12, "bold")
        
        self.states = {1: "Ясно", 2: "Облачно", 3: "Пасмурно"}
        self.colors = ["orange", "lightblue", "gray"]
        
        self.current_time, self.current_state = 0.0, 1
        self.history = [(0.0, 1)]
        self.durations = {1: 0.0, 2: 0.0, 3: 0.0}
        
        self.is_running, self.delay, self.pi_theo = False, 300, [1/3, 1/3, 1/3]

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        left = tk.Frame(root, padx=20, pady=20); left.pack(side=tk.LEFT, fill=tk.Y)
        right = tk.Frame(root, padx=20, pady=20); right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        m_frame = tk.LabelFrame(left, text="Интенсивности (в сутки)", font=bold_font, padx=10, pady=10)
        m_frame.pack(fill=tk.X, pady=10)
        defaults = [[0, 0.6, 0.2], [0.4, 0, 0.5], [0.1, 0.7, 0]]
        self.entries = {}
        
        for i in range(1, 4):
            self.entries[i] = {}
            tk.Label(m_frame, text=self.states[i], font=bold_font).grid(row=i, column=0, padx=10, pady=5)
            for j in range(1, 4):
                e = tk.Entry(m_frame, width=8, justify="center", font=default_font)
                e.insert(0, str(defaults[i-1][j-1]) if i != j else "0.0")
                if i == j: e.config(state="disabled", disabledbackground="#d9d9d9")
                else: e.bind("<KeyRelease>", lambda event, r=i: self.update_diagonal(r))
                e.grid(row=i, column=j, padx=5, pady=5)
                self.entries[i][j] = e

        self.btn_run = tk.Button(left, text="Старт", bg="lightgreen", command=self.toggle, font=bold_font, height=2)
        self.btn_run.pack(fill=tk.X, pady=4)
        tk.Button(left, text="Шаг (Прыжок)", command=self.step, font=default_font, height=2).pack(fill=tk.X, pady=4)
        tk.Button(left, text="Экспорт в .CSV", command=self.export_csv, font=default_font, height=2).pack(fill=tk.X, pady=4)
        tk.Button(left, text="Сброс", bg="#ffcccc", command=self.reset, font=default_font, height=2).pack(fill=tk.X, pady=4)
        
        tk.Label(left, text="Задержка между шагами (мс):", font=default_font).pack(anchor="w", pady=(15, 2))
        self.slider = tk.Scale(left, from_=50, to=1000, orient=tk.HORIZONTAL, font=default_font, command=self.update_speed)
        self.slider.set(self.delay)
        self.slider.pack(fill=tk.X, pady=(0, 10))
        
        self.lbl_info = tk.Label(left, text="Время: 0.00\nПогода: -", font=("Arial", 13, "bold"), justify=tk.LEFT)
        self.lbl_info.pack(anchor="w", pady=15)

        plt.rcParams.update({'font.size': 11})
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 8))
        self.fig.tight_layout(pad=4.0)
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_diagonal(1); self.update_diagonal(2); self.update_diagonal(3)
        self.calc_theoretical(); self.draw()

    def update_speed(self, val):
        self.delay = int(val)

    def update_diagonal(self, row):
        try:
            s = sum(float(self.entries[row][j].get()) for j in range(1, 4) if j != row)
            e = self.entries[row][row]
            e.config(state="normal"); e.delete(0, tk.END); e.insert(0, f"-{s:.2f}"); e.config(state="disabled")
        except ValueError: pass

    def get_q(self):
        try:
            Q = [[float(self.entries[i][j].get()) for j in range(1, 4)] for i in range(1, 4)]
            for i in range(3): Q[i][i] = -sum(Q[i][j] for j in range(3) if j != i)
            return Q
        except ValueError: return None

    def calc_theoretical(self):
        Q = self.get_q()
        if not Q: return False
        a, b, e_val = Q[0][0] - Q[2][0], Q[1][0] - Q[2][0], -Q[2][0]
        c, d, f_val = Q[0][1] - Q[2][1], Q[1][1] - Q[2][1], -Q[2][1]
        det = a * d - b * c
        if abs(det) > 1e-9:
            p1 = (e_val * d - b * f_val) / det
            p2 = (a * f_val - e_val * c) / det
            self.pi_theo = [p1, p2, 1.0 - p1 - p2]
        return True

    def toggle(self):
        if self.is_running:
            self.is_running = False
            self.btn_run.config(text="Старт", bg="lightgreen")
        else:
            if not self.calc_theoretical(): return
            self.is_running = True
            self.btn_run.config(text="Стоп", bg="orange")
            self.run_loop()

    def run_loop(self):
        if self.is_running: 
            self.step()
            # Теперь интервал берется динамически из self.delay, измененного ползунком
            self.root.after(self.delay, self.run_loop)

    def step(self):
        Q = self.get_q()
        if not Q or -Q[self.current_state-1][self.current_state-1] == 0: return
        
        i = self.current_state - 1
        q_ii = -Q[i][i]
        
        delta_t = -math.log(random.random()) / q_ii
        self.durations[self.current_state] += delta_t
        self.current_time += delta_t

        choices_indices = [j for j in range(3) if j != i]
        probs = [Q[i][j] / q_ii for j in choices_indices]
        
        chosen_index = random.choices(choices_indices, weights=probs)[0]
        self.current_state = chosen_index + 1
        
        self.history.append((self.current_time, self.current_state))
        self.lbl_info.config(text=f"Время: {self.current_time:.2f} сут.\nПогода: {self.states[self.current_state]}")
        self.draw()

    def draw(self):
        self.ax1.clear(); self.ax2.clear()
        
        times, states = zip(*self.history)
        self.ax1.step(times, states, where='post', color='blue', linewidth=2.5)
        self.ax1.set_yticks([1, 2, 3])
        self.ax1.set_yticklabels([self.states[1], self.states[2], self.states[3]])
        self.ax1.set_xlim(max(0, self.current_time - 20), max(20, self.current_time))
        self.ax1.set_title("История изменений", fontsize=11, fontweight='bold')
        self.ax1.grid(True, linestyle='--', alpha=0.5)

        x = [1, 2, 3]
        emp = [self.durations[i]/self.current_time if self.current_time > 0 else 0.0 for i in x]
        
        b1 = self.ax2.bar([v - 0.15 for v in x], emp, width=0.3, label="Эмпирич.", color=self.colors)
        b2 = self.ax2.bar([v + 0.15 for v in x], self.pi_theo, width=0.3, label="Теоретич.", edgecolor='red', fill=False, linewidth=2)
        
        self.ax2.bar_label(b1, fmt='%.3f', padding=3, fontsize=9, fontweight='bold')
        self.ax2.bar_label(b2, fmt='%.3f', padding=3, fontsize=9)

        self.ax2.set_xticks(x)
        self.ax2.set_xticklabels([self.states[i] for i in x])
        self.ax2.set_ylim(0, 1.2) 
        self.ax2.legend(fontsize=10)
        self.ax2.set_title("Распределение долей времени", fontsize=11, fontweight='bold')
        self.ax2.grid(True, linestyle='--', alpha=0.3, axis='y')
        
        self.canvas_plot.draw()

    def export_csv(self):
        if len(self.history) <= 1:
            messagebox.showwarning("Внимание", "Нет данных для сохранения. Запустите симуляцию.")
            return
        try:
            filename = "weather_stats.csv"
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Момент времени (сут)", "ID Состояния", "Название погоды"])
                for time_mark, state in self.history:
                    writer.writerow([round(time_mark, 4), state, self.states[state]])
            messagebox.showinfo("Готово", f"История погоды успешно сохранена в файл:\n{filename}")
        except Exception as err:
            messagebox.showerror("Ошибка экспорта", f"Не удалось записать файл: {err}")

    def reset(self):
        self.is_running = False
        self.btn_run.config(text="Старт", bg="lightgreen")
        self.current_time, self.current_state = 0.0, 1
        self.history = [(0.0, 1)]
        self.durations = {1: 0.0, 2: 0.0, 3: 0.0}
        self.lbl_info.config(text="Время: 0.00\nПогода: -")
        self.calc_theoretical(); self.draw()

    def on_closing(self):
        self.is_running = False
        plt.close('all')
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovApp(root)
    root.mainloop()