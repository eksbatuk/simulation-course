import tkinter as tk
from tkinter import messagebox
import random
import csv

class MarkovWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("850x520")

        self.states = {1: "Ясно", 2: "Облачно", 3: "Пасмурно"}
        self.colors = {1: "orange", 2: "lightblue", 3: "gray"}

        self.current_day = 0
        self.current_state = 1
        self.history = []
        self.state_counts = {1: 0, 2: 0, 3: 0}
        self.is_running = False
        self.delay = 300
        self.pi_theoretical = [1/3, 1/3, 1/3]

        self.create_widgets()
        self.calculate_theoretical()

    def create_widgets(self):
        left_frame = tk.Frame(self.root, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        right_frame = tk.Frame(self.root, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        matrix_frame = tk.LabelFrame(left_frame, text="Матрица переходов", padx=5, pady=5)
        matrix_frame.pack(fill=tk.X, pady=(0, 10))

        defaults = [
            [0.6, 0.3, 0.1],
            [0.2, 0.5, 0.3],
            [0.1, 0.4, 0.5]
        ]
        self.entries = {}

        for col_idx, name in self.states.items():
            tk.Label(matrix_frame, text=name, fg=self.colors[col_idx], font=("Arial", 9, "bold")).grid(row=0, column=col_idx, padx=5, pady=2)

        for row_idx, name in self.states.items():
            tk.Label(matrix_frame, text=name + " ->", font=("Arial", 9, "bold")).grid(row=row_idx, column=0, padx=5, pady=2, sticky="w")
            self.entries[row_idx] = {}
            for col_idx in self.states.keys():
                entry = tk.Entry(matrix_frame, width=6, justify="center")
                entry.insert(0, str(defaults[row_idx-1][col_idx-1]))
                entry.grid(row=row_idx, column=col_idx, padx=3, pady=2)
                self.entries[row_idx][col_idx] = entry

        tk.Button(matrix_frame, text="Применить вероятности", command=self.calculate_theoretical, bg="#e1e1e1").grid(row=4, column=0, columnspan=4, pady=8, sticky="ew")

        ctrl_frame = tk.LabelFrame(left_frame, text="Управление", padx=5, pady=5)
        ctrl_frame.pack(fill=tk.BOTH, expand=True)

        self.btn_run = tk.Button(ctrl_frame, text="Старт", bg="lightgreen", command=self.toggle_run, font=("Arial", 10, "bold"))
        self.btn_run.pack(fill=tk.X, pady=3)

        tk.Button(ctrl_frame, text="+1 День (Шаг)", command=self.step).pack(fill=tk.X, pady=3)
        tk.Button(ctrl_frame, text="Сбросить статистику", command=self.reset_stats, bg="#ffcccc").pack(fill=tk.X, pady=3)
        tk.Button(ctrl_frame, text="Экспорт результатов (.CSV)", command=self.export_csv).pack(fill=tk.X, pady=3)

        tk.Label(ctrl_frame, text="Скорость (задержка в мс):").pack(anchor="w", pady=(10, 0))
        self.slider = tk.Scale(ctrl_frame, from_=50, to=1000, orient=tk.HORIZONTAL, command=self.update_speed)
        self.slider.set(self.delay)
        self.slider.pack(fill=tk.X, pady=(0, 5))

        self.lbl_day = tk.Label(ctrl_frame, text="День: 0", font=("Arial", 11, "bold"))
        self.lbl_day.pack(anchor="w", pady=2)
        self.lbl_state = tk.Label(ctrl_frame, text="Текущая погода: -", font=("Arial", 11, "bold"))
        self.lbl_state.pack(anchor="w", pady=2)

        tk.Label(right_frame, text="ИСТОРИЯ ИЗМЕНЕНИЯ ПОГОДЫ (ПОСЛЕДНИЕ 30 ДНЕЙ)", font=("Arial", 9, "bold")).pack(anchor="w")
        self.trend_canvas = tk.Canvas(right_frame, height=180, bg="white", relief="sunken", bd=1)
        self.trend_canvas.pack(fill=tk.X, pady=(0, 10))
        self.trend_canvas.bind("<Configure>", lambda e: self.draw_trend())

        tk.Label(right_frame, text="РАСПРЕДЕЛЕНИЕ ПОГОДЫ: ЭМПИРИЧЕСКОЕ VS ТЕОРЕТИЧЕСКОЕ", font=("Arial", 9, "bold")).pack(anchor="w")
        self.hist_canvas = tk.Canvas(right_frame, height=180, bg="white", relief="sunken", bd=1)
        self.hist_canvas.pack(fill=tk.BOTH, expand=True)
        self.hist_canvas.bind("<Configure>", lambda e: self.draw_histogram())

    def update_speed(self, val):
        self.delay = int(val)

    def calculate_theoretical(self):
        P = []
        for i in range(1, 4):
            row = []
            row_sum = 0.0
            for j in range(1, 4):
                try:
                    val = float(self.entries[i][j].get())
                    if val < 0 or val > 1: raise ValueError
                    row.append(val)
                    row_sum += val
                except ValueError:
                    messagebox.showerror("Ошибка", f"Некорректная вероятность перевода {self.states[i]} -> {self.states[j]}")
                    return False
            if abs(row_sum - 1.0) > 1e-5:
                messagebox.showwarning("Внимание", f"Сумма вероятностей в строке '{self.states[i]}' должна равняться 1.0! (Сейчас: {row_sum:.3f})")
                return False
            P.append(row)

        try:
            a = P[0][0] - P[2][0] - 1
            b = P[1][0] - P[2][0]
            e = -P[2][0]
            c = P[0][1] - P[2][1]
            d = P[1][1] - P[2][1] - 1
            f = -P[2][1]

            det = a * d - b * c
            if abs(det) < 1e-9:
                self.pi_theoretical = [1.0, 0.0, 0.0]
            else:
                p1 = (e * d - b * f) / det
                p2 = (a * f - e * c) / det
                p3 = 1.0 - p1 - p2
                self.pi_theoretical = [p1, p2, p3]

            self.draw_histogram()
            return True
        except Exception as err:
            messagebox.showerror("Ошибка", f"Ошибка расчета стационарного распределения: {err}")
            return False

    def toggle_run(self):
        if self.is_running:
            self.is_running = False
            self.btn_run.config(text="Старт", bg="lightgreen")
        else:
            if not self.calculate_theoretical(): return
            self.is_running = True
            self.btn_run.config(text="Стоп", bg="orange")
            self.run_loop()

    def run_loop(self):
        if self.is_running:
            self.step()
            self.root.after(self.delay, self.run_loop)

    def step(self):
        P_row = []
        for j in range(1, 4):
            P_row.append(float(self.entries[self.current_state][j].get()))

        r = random.random()
        cumulative = 0.0
        next_state = 3
        for index, prob in enumerate(P_row):
            cumulative += prob
            if r <= cumulative:
                next_state = index + 1
                break

        self.current_day += 1
        self.current_state = next_state
        self.state_counts[self.current_state] += 1
        self.history.append((self.current_day, self.current_state))

        self.lbl_day.config(text=f"День: {self.current_day}")
        self.lbl_state.config(text=f"Текущая погода: {self.states[self.current_state]}")

        self.draw_trend()
        self.draw_histogram()

    def draw_trend(self):
        canvas = self.trend_canvas
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w < 10 or h < 10: return

        px, py = 50, 20
        plot_w, plot_h = w - px - 20, h - py - 20

        y_coords = {}
        for state_id in [1, 2, 3]:
            y_pos = py + plot_h - ((state_id - 1) * (plot_h / 2.0))
            y_coords[state_id] = y_pos
            canvas.create_line(px, y_pos, w - 20, y_pos, fill="lightgray", dash=(2, 2))
            canvas.create_text(px - 10, y_pos, text=self.states[state_id], anchor="e", font=("Arial", 8))

        canvas.create_line(px, py, px, h - py, fill="black")
        canvas.create_line(px, h - py, w - 20, h - py, fill="black")

        if not self.history: return

        visible_data = self.history[-30:]
        x_step = plot_w / 29 if len(visible_data) > 1 else plot_w

        points = []
        for idx, (day, state) in enumerate(visible_data):
            x_pos = px + idx * x_step
            y_pos = y_coords[state]
            points.append((x_pos, y_pos, day, state))

        for i in range(len(points) - 1):
            canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill="blue", width=1.5)

        for x, y, day, state in points:
            canvas.create_oval(x-3, y-3, x+3, y+3, fill=self.colors[state], outline="black")
            if len(visible_data) < 15 or day % 5 == 0 or day == self.current_day:
                canvas.create_text(x, h - py + 10, text=f"д.{day}", font=("Arial", 7))

    def draw_histogram(self):
            canvas = self.hist_canvas
            canvas.delete("all")
            w, h = canvas.winfo_width(), canvas.winfo_height()
            if w < 10 or h < 10: return

            px, py = 50, 30
            plot_w, plot_h = w - px - 20, h - py - 20

            #        # Отрисовка координатной сетки (шаг 0.2 доли)
            canvas.create_line(px, py, px, h - py, fill="black")
            canvas.create_line(px, h - py, w - 20, h - py, fill="black")
            for i in range(6):
                val = i * 0.2
                y_pos = h - py - (val * plot_h)
                canvas.create_line(px, y_pos, w - 20, y_pos, fill="lightgray")
                canvas.create_text(px - 10, y_pos, text=f"{val:.1f}", anchor="e", font=("Arial", 8))

            # Легенда
            canvas.create_rectangle(px + 10, py - 20, px + 25, py - 10, fill="gray")
            canvas.create_text(px + 30, py - 15, text="Эмпирическое", anchor="w", font=("Arial", 8))
            canvas.create_rectangle(px + 150, py - 20, px + 165, py - 10, fill="", outline="red", width=1.5)
            canvas.create_text(px + 170, py - 15, text="Теоретическое", anchor="w", font=("Arial", 8))

            #        # Отрисовка трех групп столбцов распределения
            group_w = plot_w / 3.0
            bar_w = group_w * 0.25

            for i in range(1, 4):
                emp_p = (self.state_counts[i] / self.current_day) if self.current_day > 0 else 0.0
                theo_p = self.pi_theoretical[i-1]

                cx = px + (i - 0.5) * group_w

                # Эмпирический столбец (залитый)
                ey = h - py - (emp_p * plot_h)
                canvas.create_rectangle(cx - bar_w - 2, ey, cx - 2, h - py, fill=self.colors[i], outline="black")
                canvas.create_text(cx - bar_w/2 - 2, ey - 7, text=f"{emp_p:.3f}", font=("Arial", 8, "bold"))

                # Теоретический столбец (с рамкой)
                ty = h - py - (theo_p * plot_h)
                canvas.create_rectangle(cx + 2, ty, cx + bar_w + 2, h - py, fill="", outline="red", width=1.5)
                canvas.create_text(cx + bar_w/2 + 2, ty - 7, text=f"{theo_p:.3f}", font=("Arial", 8))

                # Подпись названия погоды
                canvas.create_text(cx, h - py + 10, text=self.states[i], font=("Arial", 9, "bold"))

    def reset_stats(self):
        self.is_running = False
        self.btn_run.config(text="Старт", bg="lightgreen")
        self.current_day = 0
        self.current_state = 1
        self.history = []
        self.state_counts = {1: 0, 2: 0, 3: 0}
        self.lbl_day.config(text="День: 0")
        self.lbl_state.config(text="Текущая погода: -")
        self.draw_trend()
        self.draw_histogram()

    def export_csv(self):
        if not self.history:
            messagebox.showwarning("Внимание", "Нет данных для сохранения. Запустите симуляцию.")
            return
        try:
            filename = "weather_stats.csv"
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["День", "ID Состояния", "Название"])
                for day, state in self.history:
                    writer.writerow([day, state, self.states[state]])
            messagebox.showinfo("Готово", f"История погоды успешно записана в {filename}")
        except Exception as err:
            messagebox.showerror("Ошибка экспорта", f"Не удалось записать файл: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovWeatherApp(root)
    root.mainloop()