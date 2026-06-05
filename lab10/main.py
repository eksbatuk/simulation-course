import tkinter as tk
from tkinter import ttk, messagebox
import random
import heapq
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Request:
    def __init__(self, req_id, arrival_time, max_waiting_time):
        self.id = req_id
        self.arrival_time = arrival_time
        self.patience_deadline = arrival_time + max_waiting_time
        self.service_start_time = None
        self.service_end_time = None

    def __lt__(self, other):
        return self.patience_deadline < other.patience_deadline

class Simulation:
    def __init__(self, lambda_rate, mu_rate, num_channels, max_queue, max_wait, sim_time):
        self.lambda_rate = lambda_rate
        self.mu_rate = mu_rate
        self.n = num_channels
        self.max_queue = max_queue
        self.max_wait = max_wait
        self.sim_time = sim_time

        self.events = []
        self.queue = []
        self.busy_channels = 0

        self.stats = {
            'total_arrivals': 0,
            'successful': 0,
            'rejected_queue_full': 0,
            'rejected_impatient': 0,
            'queue_lengths_time': []
        }

        self.state_durations = {}
        self.last_state_change_time = 0.0
        self.current_state = 0

    def add_event(self, time, event_type, data=None):
        if time <= self.sim_time:
            heapq.heappush(self.events, (time, event_type, data))

    def change_state(self, current_time, delta):
        duration = current_time - self.last_state_change_time
        if duration > 0:
            self.state_durations[self.current_state] = self.state_durations.get(self.current_state, 0.0) + duration
        
        self.current_state += delta
        self.last_state_change_time = current_time
        self.stats['queue_lengths_time'].append((current_time, len(self.queue)))

    def run(self):
        first_arrival = random.expovariate(self.lambda_rate)
        self.add_event(first_arrival, 'arrival')
        req_counter = 0

        while self.events:
            current_time, event_type, data = heapq.heappop(self.events)
            self.clean_impatient_requests(current_time)

            if event_type == 'arrival':
                req_counter += 1
                self.stats['total_arrivals'] += 1
                new_request = Request(req_counter, current_time, self.max_wait)

                if self.busy_channels < self.n:
                    self.busy_channels += 1
                    self.change_state(current_time, 1)
                    service_duration = random.expovariate(self.mu_rate)
                    self.add_event(current_time + service_duration, 'departure', new_request)
                elif len(self.queue) < self.max_queue:
                    self.queue.append(new_request)
                    self.change_state(current_time, 1)
                else:
                    self.stats['rejected_queue_full'] += 1

                next_arrival = current_time + random.expovariate(self.lambda_rate)
                self.add_event(next_arrival, 'arrival')

            elif event_type == 'departure':
                self.stats['successful'] += 1
                self.busy_channels -= 1
                self.change_state(current_time, -1)

                if self.queue:
                    next_req = self.queue.pop(0)
                    self.stats['queue_lengths_time'].append((current_time, len(self.queue)))
                    self.busy_channels += 1
                    service_duration = random.expovariate(self.mu_rate)
                    self.add_event(current_time + service_duration, 'departure', next_req)

        if self.sim_time > self.last_state_change_time:
            duration = self.sim_time - self.last_state_change_time
            self.state_durations[self.current_state] = self.state_durations.get(self.current_state, 0.0) + duration

        return self.calculate_results()

    def clean_impatient_requests(self, current_time):
        impatient_requests = [r for r in self.queue if r.patience_deadline < current_time]
        if impatient_requests:
            for r in impatient_requests:
                self.queue.remove(r)
                self.stats['rejected_impatient'] += 1
                self.change_state(r.patience_deadline, -1)

    def calculate_results(self):
        leftovers = self.busy_channels + len(self.queue)
        final_rejected_full = self.stats['rejected_queue_full'] + leftovers

        total_queue_area = 0.0
        q_history = self.stats['queue_lengths_time']
        for i in range(len(q_history) - 1):
            t1, q1 = q_history[i]
            t2, _ = q_history[i+1]
            total_queue_area += q1 * (t2 - t1)
        
        avg_queue_len = total_queue_area / self.sim_time if self.sim_time > 0 else 0

        total_busy_time = 0.0
        for state, duration in self.state_durations.items():
            channels_busy = min(state, self.n)
            total_busy_time += channels_busy * duration
        
        emp_p1_channel = (total_busy_time / (self.n * self.sim_time)) if self.sim_time > 0 else 0
        emp_p0_channel = 1.0 - emp_p1_channel

        rho = self.lambda_rate / self.mu_rate
        inv_p0_sys = 0.0
        for k in range(self.n + 1):
            inv_p0_sys += (rho ** k) / math.factorial(k)
        for k in range(1, self.max_queue + 1):
            inv_p0_sys += (rho ** (self.n + k)) / (math.factorial(self.n) * (self.n ** k))
        
        p0_sys = 1.0 / inv_p0_sys if inv_p0_sys > 0 else 0
        
        avg_busy_channels_theor = 0.0
        for k in range(1, self.n + 1):
            p_k = ((rho ** k) / math.factorial(k)) * p0_sys
            avg_busy_channels_theor += k * p_k
        for k in range(1, self.max_queue + 1):
            p_k = ((rho ** (self.n + k)) / (math.factorial(self.n) * (self.n ** k))) * p0_sys
            avg_busy_channels_theor += self.n * p_k
            
        theor_p1_channel = avg_busy_channels_theor / self.n
        theor_p0_channel = 1.0 - theor_p1_channel

        return {
            'total': self.stats['total_arrivals'],
            'successful': self.stats['successful'],
            'rejected_full': final_rejected_full,
            'rejected_impatient': self.stats['rejected_impatient'],
            'avg_queue': round(avg_queue_len, 3),
            'emp_p0': round(emp_p0_channel, 3),
            'emp_p1': round(emp_p1_channel, 3),
            'theor_p0': round(theor_p0_channel, 3),
            'theor_p1': round(theor_p1_channel, 3)
        }

class SimulationUI:
    def __init__(self, root, scale=1.5):
        self.root = root
        self.scale = scale
        self.root.title("Моделирование СМО M/M/n/K")
        
        width = int(2000 * scale)
        height = int(1000 * scale)
        self.root.geometry(f"{width}x{height}")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        font_size_normal = int(11 * self.scale)
        font_size_bold = int(11 * self.scale)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', font_size_normal))
        style.configure('TButton', font=('Helvetica', font_size_bold, 'bold'), padding=int(5 * self.scale))
        style.configure('TLabelframe.Label', font=('Helvetica', font_size_bold, 'bold'))
        style.configure('TEntry', font=('Helvetica', font_size_normal))

    def create_widgets(self):
        left_frame = ttk.Frame(self.root, padding=int(10 * self.scale))
        left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        input_frame = ttk.LabelFrame(left_frame, text=" Параметры системы ", padding=int(10 * self.scale))
        input_frame.pack(side=tk.TOP, fill=tk.X, pady=int(5 * self.scale))

        params = [
            ("Интенсивность заявок (λ):", "2.0"),
            ("Интенсивность обслуж. (μ):", "1.0"),
            ("Кол-во приборов (n):", "2"),
            ("Мест в очереди (K):", "3"),
            ("Макс. время ожидания:", "2.5"),
            ("Время моделирования:", "1000")
        ]

        self.entries = {}
        for i, (label_text, default_val) in enumerate(params):
            lbl = ttk.Label(input_frame, text=label_text)
            lbl.grid(row=i, column=0, sticky=tk.W, pady=int(5 * self.scale), padx=int(5 * self.scale))
            
            entry = ttk.Entry(input_frame, width=int(10 * self.scale))
            entry.insert(0, default_val)
            entry.grid(row=i, column=1, sticky=tk.E, pady=int(5 * self.scale), padx=int(5 * self.scale))
            self.entries[label_text] = entry

        self.btn_run = ttk.Button(input_frame, text="Запустить симуляцию", command=self.start_simulation)
        self.btn_run.grid(row=len(params), column=0, columnspan=2, pady=int(15 * self.scale))

        self.stats_frame = ttk.LabelFrame(left_frame, text=" Статистика симуляции ", padding=int(10 * self.scale))
        self.stats_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=int(5 * self.scale))

        self.stat_labels = {
            'total': "Всего заявок: —",
            'successful': "Успешные: —",
            'rejected_full': "Отказ (нет мест): —",
            'rejected_impatient': "Не дождались: —",
            'avg_queue': "Ср. длина очереди: —"
        }
        
        self.stat_widgets = {}
        for k, text in self.stat_labels.items():
            lbl = ttk.Label(self.stats_frame, text=text, anchor=tk.W)
            lbl.pack(fill=tk.X, pady=int(4 * self.scale))
            self.stat_widgets[k] = lbl

        right_frame = ttk.Frame(self.root, padding=int(10 * self.scale))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        fig_width = 5.5 * self.scale
        fig_height = 4.5 * self.scale
        plt.rcParams.update({'font.size': int(10 * self.scale)})

        self.fig, self.ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.draw_histogram(0, 0, 0, 0)

    def start_simulation(self):
        try:
            lambda_rate = float(self.entries["Интенсивность заявок (λ):"].get())
            mu_rate = float(self.entries["Интенсивность обслуж. (μ):"].get())
            n = int(self.entries["Кол-во приборов (n):"].get())
            max_queue = int(self.entries["Мест в очереди (K):"].get())
            max_wait = float(self.entries["Макс. время ожидания:"].get())
            sim_time = float(self.entries["Время моделирования:"].get())

            if min(lambda_rate, mu_rate, n, max_queue, max_wait, sim_time) <= 0:
                raise ValueError("Все параметры должны быть больше нуля.")

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Проверьте корректность введенных данных.\n{e}")
            return

        sim = Simulation(lambda_rate, mu_rate, n, max_queue, max_wait, sim_time)
        results = sim.run()

        self.stat_widgets['total'].config(text=f"Всего заявок: {results['total']}")
        self.stat_widgets['successful'].config(text=f"Успешные: {results['successful']}")
        self.stat_widgets['rejected_full'].config(text=f"Отказ (нет мест): {results['rejected_full']}")
        self.stat_widgets['rejected_impatient'].config(text=f"Не дождались: {results['rejected_impatient']}")
        self.stat_widgets['avg_queue'].config(text=f"Ср. длина очереди: {results['avg_queue']}")

        self.draw_histogram(results['emp_p0'], results['emp_p1'], results['theor_p0'], results['theor_p1'])

    def draw_histogram(self, emp_p0, emp_p1, theor_p0, theor_p1):
        self.ax.clear()

        categories = ['P0 (Свободен)', 'P1 (Занят)']
        x = [0, 1]
        width = 0.3

        self.ax.bar([pos - width/2 for pos in x], [emp_p0, emp_p1], width, label='Эмпирическая', color='#2ecc71')
        self.ax.bar([pos + width/2 for pos in x], [theor_p0, theor_p1], width, label='Теоретическая', color='#3498db')

        self.ax.set_ylabel('Вероятность')
        self.ax.set_title('Вероятности состояний отдельного прибора')
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(categories)
        self.ax.set_ylim(0, 1.15)
        self.ax.legend(loc='upper right')
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)

        font_size_text = int(9 * self.scale)
        for pos, val in zip(x, [emp_p0, emp_p1]):
            self.ax.text(pos - width/2, val + 0.02, f'{val:.2f}', ha='center', va='bottom', fontsize=font_size_text)
        for pos, val in zip(x, [theor_p0, theor_p1]):
            self.ax.text(pos + width/2, val + 0.02, f'{val:.2f}', ha='center', va='bottom', fontsize=font_size_text)

        self.fig.tight_layout() 
        self.canvas.draw()

    def on_closing(self):
        try:
            plt.close('all')
        except Exception:
            pass
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    MY_SCREEN_SCALE = 1
    app = SimulationUI(root, scale=MY_SCREEN_SCALE)
    root.mainloop()