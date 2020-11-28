from typing import List
import time

class CellMatrix:
    def __init__(self, size: int):
        self.size = size
        self.matrix = [
            [Cell() for _ in range(size)] for _ in range(size)
        ]
        self.last_update = 0


    def get_cells(self):
        return [cell for row in self.matrix for cell in row]


    def toggle_cell(self, i: int, j: int):
        cell = self.matrix[i][j]
        cell.alive = not cell.alive


    def reset(self):
        for row in self.matrix:
            for cell in row:
                cell.alive = False


    def should_update(self, updates_per_second: int):
        interval = 1 / updates_per_second
        current_time = time.time()
        if current_time - self.last_update >= interval:
            self.last_update = current_time
            return True
        else:
            return False


    def update(self):
        def get_neighbors(i: int, j: int) -> List[Cell]:
            neighbor_coords = [
                (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                (i,     j - 1),             (i,     j + 1),
                (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)
            ]
            neighbor_coords = [c for c in neighbor_coords if (0 <= c[0] < self.size) and (0 <= c[1] < self.size)]
            neighbors = [self.matrix[coord[0]][coord[1]] for coord in neighbor_coords]
            return neighbors
        
        for row in self.matrix:
            for cell in row:
                if cell.next_state is not None:
                    cell.alive = bool(cell.next_state)
                    cell.next_state = None

        for i in range(self.size):
            for j in range(self.size):
                cell = self.matrix[i][j]
                neighbors = get_neighbors(i, j)
                live_neighbors = [n for n in neighbors if n.alive]
                if cell.alive:
                    if len(live_neighbors) not in [2, 3]:
                        cell.next_state = Cell.DEAD
                else:
                    if len(live_neighbors) == 3:
                        cell.next_state = Cell.ALIVE
        

class Cell:
    DEAD = 0
    ALIVE = 1

    def __init__(self):
        self.alive = False
        self.next_state = None