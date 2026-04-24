import tkinter as tk
from tkinter import messagebox
import math
import random
import numpy as np
from scipy.stats import norm, chi2
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NormalSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("850x500")
        self.font_standard = ("Arial", 12)
        self._setup_ui()

    def _setup_ui(self):
        self.frame_input = tk.Frame(self.root, padx=20, pady=50)
        self.frame_input.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.frame_input, text="Mean", font=self.font_standard).grid(row=0, column=0, sticky="w", pady=10)
        self.entry_mean = tk.Entry(self.frame_input, font=self.font_standard, width=10, relief="solid", borderwidth=1)
        self.entry_mean.grid(row=0, column=1, pady=10, padx=10)
        self.entry_mean.insert(0, "0")

        tk.Label(self.frame_input, text="Variance", font=self.font_standard).grid(row=1, column=0, sticky="w", pady=10)
        self.entry_var = tk.Entry(self.frame_input, font=self.font_standard, width=10, relief="solid", borderwidth=1)
        self.entry_var.grid(row=1, column=1, pady=10, padx=10)
        self.entry_var.insert(0, "1")

        tk.Label(self.frame_input, text="Sample size", font=self.font_standard).grid(row=2, column=0, sticky="w", pady=10)
        self.entry_n = tk.Entry(self.frame_input, font=self.font_standard, width=10, relief="solid", borderwidth=1)
        self.entry_n.grid(row=2, column=1, pady=10, padx=10)
        self.entry_n.insert(0, "100")

        self.btn_start = tk.Button(self.frame_input, text="Start", font=self.font_standard, 
                                   command=self._process_data, relief="ridge", padx=20)
        self.btn_start.grid(row=3, column=0, columnspan=2, pady=30)

        self.frame_output = tk.Frame(self.root, padx=20, pady=20)
        self.frame_output.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.fig = Figure(figsize=(5, 3.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_output)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.frame_text = tk.Frame(self.frame_output)
        self.frame_text.pack(fill=tk.X, pady=10)

        self.lbl_avg = tk.Label(self.frame_text, text="Average: -", font=self.font_standard)
        self.lbl_avg.pack(anchor="w")

        self.lbl_var = tk.Label(self.frame_text, text="Variance: -", font=self.font_standard)
        self.lbl_var.pack(anchor="w")

        self.frame_chi = tk.Frame(self.frame_text)
        self.frame_chi.pack(anchor="w", pady=5)

        self.lbl_chi_text = tk.Label(self.frame_chi, text="Chi-squared: -", font=self.font_standard)
        self.lbl_chi_text.pack(side=tk.LEFT)

        self.lbl_chi_res = tk.Label(self.frame_chi, text="", font=self.font_standard)
        self.lbl_chi_res.pack(side=tk.LEFT)

    def _generate_normal_data(self, mean, variance, n):
        std_dev = math.sqrt(variance)
        data = []
        
        for _ in range((n + 1) // 2):
            u1 = random.random()
            u2 = random.random()
            
            if u1 == 0:
                u1 = 1e-10 
                
            z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
            z1 = math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)
            
            data.append(mean + z0 * std_dev)
            data.append(mean + z1 * std_dev)
            
        return data[:n]

    def _process_data(self):
        try:
            mean_val = float(self.entry_mean.get())
            var_val = float(self.entry_var.get())
            n_val = int(self.entry_n.get())
            
            if var_val <= 0:
                messagebox.showerror("Ошибка", "Дисперсия должна быть строго больше 0")
                return
            if n_val <= 0:
                messagebox.showerror("Ошибка", "Объем выборки должен быть положительным")
                return
                
            data = self._generate_normal_data(mean_val, var_val, n_val)
            
            emp_mean = sum(data) / n_val
            emp_var = sum((x - emp_mean) ** 2 for x in data) / (n_val - 1 if n_val > 1 else 1)
            
            err_mean = abs((emp_mean - mean_val) / mean_val) * 100 if mean_val != 0 else abs(emp_mean) * 100
            err_var = abs((emp_var - var_val) / var_val) * 100
            
            self.lbl_avg.config(text=f"Average: {emp_mean:.3f} (error = {err_mean:.0f}%)")
            self.lbl_var.config(text=f"Variance: {emp_var:.3f} (error = {err_var:.0f}%)")
            
            k = int(1 + 3.322 * math.log10(n_val))
            if k < 5: k = 5 
            
            observed_freqs, bin_edges = np.histogram(data, bins=k)
            
            chi_squared_stat = 0
            for i in range(k):
                p = norm.cdf(bin_edges[i+1], loc=mean_val, scale=math.sqrt(var_val)) - \
                    norm.cdf(bin_edges[i], loc=mean_val, scale=math.sqrt(var_val))
                expected = p * n_val
                if expected > 0:
                    chi_squared_stat += ((observed_freqs[i] - expected) ** 2) / expected
                    
            df = k - 1 
            chi_squared_crit = chi2.ppf(0.95, df)
            
            is_true = chi_squared_stat <= chi_squared_crit
            sign = "<" if chi_squared_stat < chi_squared_crit else ">"
            
            self.lbl_chi_text.config(text=f"Chi-squared: {chi_squared_stat:.2f} {sign} {chi_squared_crit:.2f} is ")
            self.lbl_chi_res.config(text="true" if is_true else "false", 
                                    fg="green" if is_true else "red")

            self._plot_graph(data, mean_val, var_val, k, bin_edges)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите числовые значения.")

    def _plot_graph(self, data, mean_val, var_val, bins_count, bin_edges):
        """Метод для перерисовки гистограммы и графика"""
        self.ax.clear()
        
        self.ax.hist(data, bins=bins_count, density=True, alpha=0.4, 
                     edgecolor='red', color='#a2b9de')
        
        x = np.linspace(min(data), max(data), 100)
        y = norm.pdf(x, loc=mean_val, scale=math.sqrt(var_val))
        self.ax.plot(x, y, linewidth=2.5, color='#66b04c')
        
        x_labels = [f"({bin_edges[i]:.1f}; {bin_edges[i+1]:.1f}]" for i in range(len(bin_edges)-1)]
        self.ax.set_xticks(bin_edges[:-1] + np.diff(bin_edges)/2)
        self.ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
        
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = NormalSimulatorApp(root)
    root.mainloop()