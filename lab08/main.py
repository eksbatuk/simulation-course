import tkinter as tk
from tkinter import messagebox, ttk
import math
import random

# Переключаем matplotlib в стабильный режим работы с графическими интерфейсами
import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import poisson

class PoissonSimulationApp:
    def __init__(self, root):
        self.root = root

        self.root.geometry("2000x1000")
        
        self.font_main = ("Helvetica", 20)
        self.font_bold = ("Helvetica", 20, "bold")
        
        style = ttk.Style()
        style.configure("TLableFrame.Label", font=self.font_bold)
        style.configure("TLabel", font=self.font_main)
        style.configure("TButton", font=self.font_bold)
        
        control_frame = ttk.LabelFrame(root, text=" Параметры моделирования ", padding=25)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        
        ttk.Label(control_frame, text="Интенсивность λ (запросов в сек):").pack(anchor=tk.W, pady=5)
        self.entry_lambda = ttk.Entry(control_frame, font=self.font_main, width=15)
        self.entry_lambda.insert(0, "5.0")
        self.entry_lambda.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="Интервал времени T (сек):").pack(anchor=tk.W, pady=5)
        self.entry_t = ttk.Entry(control_frame, font=self.font_main, width=15)
        self.entry_t.insert(0, "2.0")
        self.entry_t.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="Количество опытов (N):").pack(anchor=tk.W, pady=5)
        self.entry_n = ttk.Entry(control_frame, font=self.font_main, width=15)
        self.entry_n.insert(0, "1000")
        self.entry_n.pack(fill=tk.X, pady=10)
        
        self.btn_run = ttk.Button(control_frame, text="Моделировать", command=self.run_simulation)
        self.btn_run.pack(fill=tk.X, pady=25, ipady=15)
        
        stats_frame = ttk.LabelFrame(control_frame, text=" Данные ", padding=20)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.lbl_mean = ttk.Label(stats_frame, text="Эмп. среднее: -\nТеор. среднее: -", justify=tk.LEFT, font=self.font_main)
        self.lbl_mean.pack(anchor=tk.W, pady=15)
        
        self.lbl_var = ttk.Label(stats_frame, text="Эмп. дисперсия: -\nТеор. дисперсия: -", justify=tk.LEFT, font=self.font_main)
        self.lbl_var.pack(anchor=tk.W, pady=15)

        self.plot_frame = ttk.LabelFrame(root, text=" Эмпирическое распределение ", padding=20)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.fig = plt.figure(figsize=(9, 8))
        self.ax = self.fig.add_subplot(111)
        
        self.fig.subplots_adjust(left=0.12, right=0.95, top=0.9, bottom=0.15)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generate_poisson(self, mu, n):
        results = []
        L = math.exp(-mu)
        
        for _ in range(n):
            k = 0
            p = 1.0
            while True:
                k += 1
                p *= random.random()
                if p < L:
                    break
            results.append(k - 1)
            
        return np.array(results)

    def run_simulation(self):
        try:
            lam = float(self.entry_lambda.get())
            t_interval = float(self.entry_t.get())
            n_experiments = int(self.entry_n.get())
            
            if lam <= 0 or t_interval <= 0 or n_experiments <= 0:
                raise ValueError("Все параметры должны быть строго больше нуля.")
                
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Проверьте корректность введенных данных.\n{e}")
            return
        
        mu = lam * t_interval
        
        data = self.generate_poisson(mu, n_experiments)
        
        emp_mean = np.mean(data)
        emp_var = np.var(data)
        
        theo_mean = mu
        theo_var = mu
        
        self.lbl_mean.config(text=f"Эмп. среднее: {emp_mean:.4f}\nТеор. среднее: {theo_mean:.4f}")
        self.lbl_var.config(text=f"Эмп. дисперсия: {emp_var:.4f}\nТеор. дисперсия: {theo_var:.4f}")

        self.ax.clear()
        
        bins = np.arange(0, np.max(data) + 2) - 0.5
        counts, x, _ = self.ax.hist(data, bins=bins, density=True, rwidth=0.8, 
                                   color='skyblue', edgecolor='black', alpha=0.7, label='Эмпирическое')
        
        x_theo = np.arange(0, np.max(data) + 1)
        y_theo = poisson.pmf(x_theo, mu)
        self.ax.plot(x_theo, y_theo, 'ro-', linewidth=3, markersize=10, label='Теоретическое')
        
        self.ax.set_title(f"Распределение числа запросов за T = {t_interval} сек.", fontsize=20, fontweight='bold')
        self.ax.set_xlabel("Число запросов за интервал", fontsize=20)
        self.ax.set_ylabel("Относительная частота (вероятность)", fontsize=20)
        
        self.ax.set_xticks(x_theo)
        self.ax.tick_params(axis='both', labelsize=20)
        self.ax.legend(fontsize=20)
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PoissonSimulationApp(root)
    root.mainloop()