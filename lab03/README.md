## Клеточные автоматы. Лесные пожары (GUI)

**Задание:**  
Реализовать моделирование возникновения и распространения лесных пожаров с использованием двумерного клеточного автомата.

## Реализация: ##

**Состояния клеток:**
``` pyhton
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
```
Помимо обычных TREE, FIRE и EMPTY были так же добавлены состояния WATER, BIG_TREE и BIG_FIRE. Первая является буквально водой, гореть и исчезать не может, так же не пропускает огонь. Второй, большое дерево, имеет свойство гореть по двойной области Мура, специально для реализации данной механики было добавлено третье состояние - BIG_FIRE, большое дерево горит большим огнём и уже большой огонь можеть поджечь клетки в двойной области Мура

**Молния, вероятность возгарания:**

Катализатором лесного пожара является молния, которая с некоторой вероятностью может ударить в любую клетку, из-за чего начнётся возгорание
``` python
def apply_lightning(self):
    if random.random() < self.lightning_probability:
        x = random.randint(0, self.grid_width - 1)
        y = random.randint(0, self.grid_height - 1)
        if self.current_grid[y][x] == self.TREE:
            self.current_grid[y][x] = self.FIRE
        elif self.current_grid[y][x] == self.BIG_TREE:
            self.current_grid[y][x] = self.BIG_FIRE
```
**Рост деревьев:**

Дерево вырастает на месте пустой клетки с некоторой вероятностью, которая, как и в случае с молнией, выбирается пользователем
``` pyhton
if random.random() < self.growth_rate:
    self.next_grid[y][x] = self.TREE
    self.tree_age[y][x] = 1
else:
    self.next_grid[y][x] = self.EMPTY
    self.tree_age[y][x] = 0 
```

**Большие деревья:**

Большое дерево появляется на месте обычного после 30 итераций. для этого в коде реализована дополнительная сетка, которая в каждой клетке хранит значение возраста дерева. Если дерева в клетке нет, возраст дерева равен 0.
``` python
elif current_cell in [self.TREE, self.BIG_TREE]:
    self.tree_age[y][x] += 1
    
    if current_cell == self.TREE and self.tree_age[y][x] >= self.big_tree_age:
        self.next_grid[y][x] = self.BIG_TREE
    else:
        self.next_grid[y][x] = current_cell
```

**Дополнительное правильно - ветер:**

Ветер имеет правое направление и три основных значения: 0 - ветра нет, огонь распространяется равномерно во все стороны; <0.5 - ветер заставляет огонь меньше распространяться влево, на отметке в 0.5 распространение ветра в лево отсутствует; >0.5 - огонь всё также не может распространяться влево, однако в этом случае его распространение в другие стороны затрудняется, а на отметке в 1 он не распространяется вообще
``` pyhton
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

```

