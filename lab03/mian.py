import tkinter as tk
from tkinter import ttk
import random
import numpy as np
import math

class ForestFireSimulator:
    def __init__(self, root):
        self.root = root
        
        self.cell_size = 12
        self.grid_width = 50
        self.grid_height = 50
        self.canvas_width = self.grid_width * self.cell_size
        self.canvas_height = self.grid_height * self.cell_size
        
        self.EMPTY = 0
        self.TREE = 1
        self.BIG_TREE = 2
        self.FIRE = 3          
        self.BIG_FIRE = 4    
        self.WATER = 5
        
        self.colors = {
            self.EMPTY: "white",
            self.TREE: "light green",
            self.BIG_TREE: "dark green",
            self.FIRE: "orange red",
            self.BIG_FIRE: "orange red",
            self.WATER: "blue"
        }
        
        self.lightning_probability = 0.01
        self.growth_rate = 0.01
        self.wind_strength = 0
        self.speed = 100
        self.big_tree_age = 30
        
        self.tree_age = np.zeros((self.grid_height, self.grid_width), dtype=int)
        self.current_grid = np.zeros((self.grid_height, self.grid_width), dtype=int)
        self.next_grid = np.zeros((self.grid_height, self.grid_width), dtype=int)
        
        self.setup_ui()
        self.initialize_grid()
        self.update()
    
    def create_water_circle(self):
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                distance = math.sqrt((x - self.grid_height // 2) ** 2 + (y - self.grid_height // 2) ** 2)
                if 10 <= distance <= 14:
                    self.current_grid[y][x] = self.WATER
                    self.tree_age[y][x] = 0
    
    def initialize_grid(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if random.random() < 0.7:
                    self.current_grid[y][x] = self.TREE
                    self.tree_age[y][x] = random.randint(0, 10)
                else:
                    self.current_grid[y][x] = self.EMPTY
                    self.tree_age[y][x] = 0
        
        self.create_water_circle()
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.current_grid[y][x] == self.TREE and self.tree_age[y][x] >= self.big_tree_age:
                    self.current_grid[y][x] = self.BIG_TREE
        
        self.draw_grid()
    
    def setup_ui(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.reset_button = ttk.Button(control_frame, text="Сброс", command=self.reset_grid)
        self.reset_button.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Label(control_frame, text="Вер. молнии:").pack(side=tk.LEFT, padx=(0, 5))
        self.lightning_scale = ttk.Scale(control_frame, from_=0, to=0.5, orient=tk.HORIZONTAL, 
                                        value=self.lightning_probability, length=80)
        self.lightning_scale.pack(side=tk.LEFT, padx=2)
        self.lightning_label = ttk.Label(control_frame, text=f"{self.lightning_probability:.3f}", width=5)
        self.lightning_label.pack(side=tk.LEFT, padx=(2, 10))
        self.lightning_scale.configure(command=self.update_lightning_probability)
        
        ttk.Label(control_frame, text="Вер. роста:").pack(side=tk.LEFT, padx=(0, 5))
        self.growth_scale = ttk.Scale(control_frame, from_=0, to=0.5, orient=tk.HORIZONTAL, 
                                     value=self.growth_rate, length=80)
        self.growth_scale.pack(side=tk.LEFT, padx=2)
        self.growth_label = ttk.Label(control_frame, text=f"{self.growth_rate:.3f}", width=5)
        self.growth_label.pack(side=tk.LEFT, padx=(2, 10))
        self.growth_scale.configure(command=self.update_growth_rate)
        
        ttk.Label(control_frame, text="Сила ветра:").pack(side=tk.LEFT, padx=(0, 5))
        self.wind_scale = ttk.Scale(control_frame, from_=0, to=1, orient=tk.HORIZONTAL, 
                                   value=self.wind_strength, length=80)
        self.wind_scale.pack(side=tk.LEFT, padx=2)
        self.wind_label = ttk.Label(control_frame, text=f"{self.wind_strength:.2f}", width=5)
        self.wind_label.pack(side=tk.LEFT, padx=(2, 10))
        self.wind_scale.configure(command=self.update_wind_strength)
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Label(control_frame, text="Скорость:").pack(side=tk.LEFT, padx=(0, 5))
        self.speed_scale = ttk.Scale(control_frame, from_=1, to=500, orient=tk.HORIZONTAL, 
                                    value=self.speed, length=80)
        self.speed_scale.pack(side=tk.LEFT, padx=2)
        self.speed_label = ttk.Label(control_frame, text=f"{self.speed} мс", width=6)
        self.speed_label.pack(side=tk.LEFT, padx=2)
        self.speed_scale.configure(command=self.update_speed)
        
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="gray")
        self.canvas.pack(pady=10)
    
    def reset_grid(self):
        self.initialize_grid()
    
    def update_lightning_probability(self, value):
        self.lightning_probability = float(value)
        self.lightning_label.config(text=f"{self.lightning_probability:.3f}")
    
    def update_growth_rate(self, value):
        self.growth_rate = float(value)
        self.growth_label.config(text=f"{self.growth_rate:.3f}")
    
    def update_wind_strength(self, value):
        self.wind_strength = float(value)
        self.wind_label.config(text=f"{self.wind_strength:.2f}")
    
    def update_speed(self, value):
        self.speed = int(float(value))
        self.speed_label.config(text=f"{self.speed} мс")
    
    def apply_lightning(self):
        if random.random() < self.lightning_probability:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if self.current_grid[y][x] == self.TREE:
                self.current_grid[y][x] = self.FIRE
            elif self.current_grid[y][x] == self.BIG_TREE:
                self.current_grid[y][x] = self.BIG_FIRE
    
    def get_spread_probability(self, dx, dy):
        if dx > 0:
            if self.wind_strength <= 0.5:
                return 1.0 + self.wind_strength
            else:
                return 3.0 * (1.0 - self.wind_strength)
        
        elif dx < 0:
            if self.wind_strength <= 0.5:
                return 1.0 - 2.0 * self.wind_strength
            else:
                return 0.0
        
        else:
            if self.wind_strength <= 0.5:
                return 1.0
            else:
                return 2.0 * (1.0 - self.wind_strength)
            
    def fire_spread(self, dy, dx, y, x):
        ny, nx = y + dy, x + dx
        if 0 <= ny < self.grid_height and 0 <= nx < self.grid_width:
            if self.current_grid[ny][nx] == self.TREE:
                if random.random() < self.get_spread_probability(dx, dy):
                    self.next_grid[ny][nx] = self.FIRE
            elif self.current_grid[ny][nx] == self.BIG_TREE:
                if random.random() < self.get_spread_probability(dx, dy):
                    self.next_grid[ny][nx] = self.BIG_FIRE

    
    def update_grid(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                current_cell = self.current_grid[y][x]
                
                if current_cell == self.WATER:
                    self.next_grid[y][x] = self.WATER
                    self.tree_age[y][x] = 0
                
                elif current_cell in [self.FIRE, self.BIG_FIRE]:
                    self.next_grid[y][x] = self.EMPTY
                    self.tree_age[y][x] = 0
                
                elif current_cell in [self.TREE, self.BIG_TREE]:
                    self.tree_age[y][x] += 1
                    
                    if current_cell == self.TREE and self.tree_age[y][x] >= self.big_tree_age:
                        self.next_grid[y][x] = self.BIG_TREE
                    else:
                        self.next_grid[y][x] = current_cell
                
                else:
                    if random.random() < self.growth_rate:
                        self.next_grid[y][x] = self.TREE
                        self.tree_age[y][x] = 1
                    else:
                        self.next_grid[y][x] = self.EMPTY
                        self.tree_age[y][x] = 0
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.current_grid[y][x] == self.FIRE:
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:
                                    continue
                            self.fire_spread(dy, dx, y, x)
                            
    
                elif self.current_grid[y][x] == self.BIG_FIRE:
                    for dy in range(-2, 3):
                        for dx in range(-2, 3):
                            if dy == 0 and dx == 0:
                                continue
                            self.fire_spread(dy, dx, y, x)
        
        self.current_grid, self.next_grid = self.next_grid, self.current_grid
        
        self.apply_lightning()
    
    def draw_grid(self):
        self.canvas.delete("all")
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell_state = self.current_grid[y][x]
                color = self.colors[cell_state]
                
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=1)
    
    def update(self):
        self.update_grid()
        self.draw_grid()
        self.root.after(self.speed, self.update)

def main():
    root = tk.Tk()
    app = ForestFireSimulator(root)
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()