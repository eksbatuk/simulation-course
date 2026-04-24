import tkinter as tk
from tkinter import messagebox
import random

class ProbabilityApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("850x400")
        self.root.configure(bg="#ffffff")

        self.probs_vars = [tk.StringVar(value="") for _ in range(4)]
        self.prob5_var = tk.StringVar(value="auto")
        self.n_var = tk.StringVar(value="1000")

        self.create_widgets()

        self.probs_vars[0].set("0.2")
        self.probs_vars[1].set("0.1")
        self.probs_vars[2].set("0.3")
        self.probs_vars[3].set("0.25")
        self.update_prob5()

    def create_widgets(self):
        left_frame = tk.Frame(self.root)
        left_frame.place(x=20, y=50, width=280, height=320)

        for i in range(4):
            tk.Label(left_frame, text=f"Prob {i+1}", font=("Arial", 14)).place(x=20, y=20 + i*40)
            entry = tk.Entry(left_frame, textvariable=self.probs_vars[i], width=8, font=("Arial", 12), justify="center")
            entry.place(x=100, y=20 + i*40)
            entry.bind('<KeyRelease>', self.update_prob5)

        tk.Label(left_frame, text="Prob 5", font=("Arial", 14)).place(x=20, y=180)
        tk.Label(left_frame, textvariable=self.prob5_var, bg="#d3d3d3", width=8, font=("Arial", 12)).place(x=100, y=180)

        tk.Label(left_frame, text="Number of experiments", font=("Arial", 14)).place(x=20, y=240)
        tk.Entry(left_frame, textvariable=self.n_var, width=8, font=("Arial", 12), justify="center").place(x=220, y=240)

        tk.Button(left_frame, text="Start", font=("Arial", 14), command=self.run_experiment).place(x=100, y=280, width=80, height=30)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.place(x=400, y=50, width=420, height=320)

        self.graph_canvas = tk.Canvas(self.right_frame, bg="white", width=380, height=180)
        self.graph_canvas.place(x=20, y=20)

        self.lbl_average = tk.Label(self.right_frame, text="Average: - (error = -%)", font=("Arial", 12), anchor="w")
        self.lbl_average.place(x=20, y=220, width=380)

        self.lbl_variance = tk.Label(self.right_frame, text="Variance: - (error = -%)", font=("Arial", 12), anchor="w")
        self.lbl_variance.place(x=20, y=250, width=380)

        self.lbl_chi = tk.Label(self.right_frame, text="Chi-squared: -", font=("Arial", 12), anchor="w")
        self.lbl_chi.place(x=20, y=280, width=380)

    def update_prob5(self, event=None):
        try:
            p_sum = sum(float(var.get()) for var in self.probs_vars if var.get())
            p5 = 1.0 - p_sum
            if p5 < 0:
                self.prob5_var.set("Error")
            else:
                self.prob5_var.set(f"{p5:.3f}")
        except ValueError:
            self.prob5_var.set("Error")

    def run_experiment(self):
        try:
            P = [float(var.get()) for var in self.probs_vars]
            p5 = 1.0 - sum(P)
            if p5 < -1e-6:
                raise ValueError("Сумма вероятностей превышает 1")
            P.append(max(0.0, p5))
            
            N = int(self.n_var.get())
            if N <= 0:
                raise ValueError("N должно быть > 0")

            frequencies = [0] * 5
            for _ in range(N):
                r = random.random()
                cumulative = 0.0
                for i, p in enumerate(P):
                    cumulative += p
                    if r < cumulative:
                        frequencies[i] += 1
                        break
            
            emp_P = [f / N for f in frequencies]

            X = [1, 2, 3, 4, 5]
            th_mean = sum(x * p for x, p in zip(X, P))
            emp_mean = sum(x * p for x, p in zip(X, emp_P))
            err_mean = abs(emp_mean - th_mean) / th_mean * 100

            th_var = sum((x**2) * p for x, p in zip(X, P)) - th_mean**2
            emp_var = sum((x**2) * p for x, p in zip(X, emp_P)) - emp_mean**2
            err_var = abs(emp_var - th_var) / th_var * 100

            chi_squared = 0.0
            for i in range(5):
                if P[i] > 0:
                    expected = N * P[i]
                    chi_squared += ((frequencies[i] - expected) ** 2) / expected
            
            chi_critical = 9.488
            is_true = chi_squared <= chi_critical

            self.lbl_average.config(text=f"Average: {emp_mean:.3f} (error = {err_mean:.0f}%)")
            self.lbl_variance.config(text=f"Variance: {emp_var:.3f} (error = {err_var:.0f}%)")
            
            color = "red" if not is_true else "green"
            word = "false" if not is_true else "true"
            self.lbl_chi.config(text=f"Chi-squared: {chi_squared:.2f} {'<' if is_true else '>'} {chi_critical} is ")

            for widget in self.right_frame.place_slaves():
                if getattr(widget, "is_dynamic_label", False):
                    widget.destroy()
            
            lbl_tf = tk.Label(self.right_frame, text=word, fg=color, font=("Arial", 12, "bold"))
            lbl_tf.is_dynamic_label = True
            lbl_tf.place(x=220, y=280)

            self.draw_histogram(emp_P)

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def draw_histogram(self, emp_P):
        self.graph_canvas.delete("all")
        width = 380
        height = 180
        pad_x, pad_y = 30, 20
        
        self.graph_canvas.create_line(pad_x, height - pad_y, width, height - pad_y, fill="gray")
        self.graph_canvas.create_line(pad_x, 0, pad_x, height - pad_y, fill="gray")
        self.graph_canvas.create_text(pad_x + 10, 10, text="freq.", anchor="w", fill="gray")

        max_p = max(emp_P) if max(emp_P) > 0.3 else 0.35
        
        for i in range(1, 6):
            y_val = i * (max_p / 5)
            y_pos = height - pad_y - (y_val / max_p) * (height - 2*pad_y)
            self.graph_canvas.create_line(pad_x, y_pos, width, y_pos, fill="#e0e0e0")
            self.graph_canvas.create_text(pad_x - 5, y_pos, text=f"{y_val:.2f}", anchor="e", font=("Arial", 8))

        bar_width = (width - 2*pad_x) / 5 - 10
        for i, p in enumerate(emp_P):
            x0 = pad_x + 10 + i * (bar_width + 10)
            y0 = height - pad_y - (p / max_p) * (height - 2*pad_y)
            x1 = x0 + bar_width
            y1 = height - pad_y

            self.graph_canvas.create_rectangle(x0, y0, x1, y1, fill="#e6f2ff", outline="#5c8aab")
            self.graph_canvas.create_text((x0+x1)/2, y0 - 10, text=f"{p:.3f}", font=("Arial", 8))
            self.graph_canvas.create_text((x0+x1)/2, y1 + 10, text=str(i+1), font=("Arial", 8))

if __name__ == "__main__":
    root = tk.Tk()
    app = ProbabilityApp(root)
    root.mainloop()