import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def run_correct_simulation(rate_in, rate_out, total_requests):
    success_count = 0
    fail_count = 0
    t_curr = 0.0
    system_free_at = 0.0
    
    for _ in range(total_requests):
        is_busy = t_curr < system_free_at
        current_rate_in = rate_in / 2.0 if is_busy else rate_in
        
        delta_t = np.random.exponential(1.0 / current_rate_in)
        t_curr += delta_t
        
        if t_curr < system_free_at:
            fail_count += 1
        else:
            success_count += 1
            process_time = np.random.exponential(1.0 / rate_out)
            start_processing = max(t_curr, system_free_at)
            system_free_at = start_processing + process_time

    return success_count, fail_count

class SimulationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("950x750")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        input_frame = ttk.LabelFrame(self, text=" Параметры системы ", padding=10)
        input_frame.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        
        ttk.Label(input_frame, text="Интенсивность поступления (λ):").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_lambda = ttk.Entry(input_frame, width=10)
        self.entry_lambda.insert(0, "2.0")
        self.entry_lambda.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Интенсивность обслуживания (μ):").grid(row=0, column=2, sticky="w", padx=5)
        self.entry_mu = ttk.Entry(input_frame, width=10)
        self.entry_mu.insert(0, "3.0")
        self.entry_mu.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Количество заявок (N):").grid(row=0, column=4, sticky="w", padx=5)
        self.entry_n = ttk.Entry(input_frame, width=12)
        self.entry_n.insert(0, "10000")
        self.entry_n.grid(row=0, column=5, padx=5, pady=5)
        
        self.btn_run = ttk.Button(input_frame, text="Запустить симуляцию", command=self.on_start_simulation)
        self.btn_run.grid(row=0, column=6, padx=20, pady=5)
        
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
        
        self.fig = Figure(figsize=(6, 3.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.stat_frame = ttk.LabelFrame(self, text=" Статистика и результаты ", padding=10)
        self.stat_frame.grid(row=2, column=0, padx=15, pady=15, sticky="ew")
        
        self.tree = ttk.Treeview(self.stat_frame, columns=("emp", "theor", "diff"), height=2)
        self.tree.heading("#0", text="Состояние")
        self.tree.heading("emp", text="Эмпирическая")
        self.tree.heading("theor", text="Теоретическая")
        self.tree.heading("diff", text="Разница (Abs)")
        
        self.tree.column("#0", width=150, anchor="center")
        self.tree.column("emp", width=150, anchor="center")
        self.tree.column("theor", width=150, anchor="center")
        self.tree.column("diff", width=150, anchor="center")
        self.tree.pack(fill=tk.X, pady=5)
        
        self.lbl_processed = ttk.Label(self.stat_frame, text="Обработано заявок (Успешно): -", font=("Arial", 10))
        self.lbl_processed.pack(anchor="w", pady=2)
        
        self.lbl_load = ttk.Label(self.stat_frame, text="Фактическая нагрузка на систему (ρ): -", font=("Arial", 10))
        self.lbl_load.pack(anchor="w", pady=2)
        
        self.lbl_capacity = ttk.Label(self.stat_frame, text="Абсолютная пропускная способность (A): -", font=("Arial", 10, "bold"))
        self.lbl_capacity.pack(anchor="w", pady=5)
        
        self.draw_empty_chart()

    def draw_empty_chart(self):
        self.ax.clear()
        self.ax.set_title("Сравнение распределений состояний СМО")
        self.ax.set_ylabel("Вероятность")
        self.ax.set_xticks([0, 1])
        self.ax.set_xticklabels(["P0 (Свободен)", "P1 (Занят)"])
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        self.canvas.draw()

    def calculate_theoretical(self, rate_in, rate_out):
        rho = rate_in / rate_out
        p0 = 1.0 / (1.0 + 0.5 * rho)
        p1 = rho * 0.5 / (1.0 + 0.5 * rho)
        return p0, p1

    def on_start_simulation(self):
        try:
            rate_in = float(self.entry_lambda.get())
            rate_out = float(self.entry_mu.get())
            total_requests = int(self.entry_n.get())
            
            if rate_in <= 0 or rate_out <= 0 or total_requests <= 0:
                raise ValueError("Все значения должны быть больше нуля.")
                
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, проверьте корректность введенных данных.\n"
                                                 "Интенсивности — дробные числа, количество — целое.")
            return

        success, fail = run_correct_simulation(rate_in, rate_out, total_requests)
        
        p0_emp = success / total_requests
        p1_emp = fail / total_requests
        
        p0_theor, p1_theor = self.calculate_theoretical(rate_in, rate_out)
        
        diff_p0 = abs(p0_emp - p0_theor)
        diff_p1 = abs(p1_emp - p1_theor)
        
        a_emp = rate_out * p1_emp
        a_theor = rate_out * p1_theor
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.tree.insert("", "end", text="P0 (Канал свободен)", values=(f"{p0_emp:.4f}", f"{p0_theor:.4f}", f"{diff_p0:.4f}"))
        self.tree.insert("", "end", text="P1 (Канал занят)", values=(f"{p1_emp:.4f}", f"{p1_theor:.4f}", f"{diff_p1:.4f}"))
        
        self.lbl_processed.config(text=f"Обработано заявок (Успешно): {success} из {total_requests}")
        self.lbl_load.config(text=f"Фактическая нагрузка на систему (ρ = λ/μ): {rate_in/rate_out:.3f}")
        self.lbl_capacity.config(text=f"Абсолютная пропускная способность (A): {a_emp:.4f} з-к/ед.вр. (Теория: {a_theor:.4f})")
        
        self.ax.clear()
        
        x = np.array([0, 1])
        width = 0.35
        
        self.ax.bar(x - width/2, [p0_emp, p1_emp], width, label='Эмпирические', color='#3498db')
        self.ax.bar(x + width/2, [p0_theor, p1_theor], width, label='Теоретические', color='#2ecc71', alpha=0.8)
        
        self.ax.set_title("Сравнение Эмпирических и Теоретических состояний СМО")
        self.ax.set_ylabel("Вероятность")
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(["P0 (Свободен)", "P1 (Занят)"])
        self.ax.legend()
        self.ax.grid(axis='y', linestyle='--', alpha=0.5)
        
        self.ax.set_ylim(0, 1.1)
        
        self.canvas.draw()

if __name__ == "__main__":
    app = SimulationApp()
    app.mainloop()