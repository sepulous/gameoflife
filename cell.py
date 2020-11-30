from typing import List, Tuple
import time

from ui import UI

class CellMatrix:
    def __init__(self, matrix_size: int, cell_size: int, window_size: Tuple[int, int]):
        self.matrix_size = matrix_size
        self.matrix = self._generate_matrix(matrix_size, cell_size, window_size)
        self.last_update = 0

    def _generate_matrix(self, matrix_size: int, cell_size: int, window_size: Tuple[int, int]):
        matrix = [[] for _ in range(matrix_size)]
        x_pos, y_pos = 0, 0
        for row in matrix:
            for index in range(matrix_size):
                row.append(Cell(cell_size, x_pos, y_pos))
                if (index + 1) % matrix_size == 0:
                    x_pos = 0
                    y_pos += cell_size + UI.get_line_width()
                else:
                    x_pos += cell_size + UI.get_line_width()

        return matrix

    def get_cells(self):
        return [cell for row in self.matrix for cell in row]

    def reset(self):
        for row in self.matrix:
            for cell in row:
                cell.alive = False

    def should_update(self):
        interval = 1 / UI.get_updates_per_second()
        current_time = time.time()
        if current_time - self.last_update >= interval:
            self.last_update = current_time
            return True
        else:
            return False

    def update(self):
        def get_live_neighbor_count(i: int, j: int) -> List[Cell]:
            neighbor_coords = [
                (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                (i,     j - 1),             (i,     j + 1),
                (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)
            ]
            neighbor_coords = [c for c in neighbor_coords if (0 <= c[0] < self.matrix_size) and (0 <= c[1] < self.matrix_size)]
            neighbors = [self.matrix[coord[0]][coord[1]] for coord in neighbor_coords]
            live_neighbors = [neighbor for neighbor in neighbors if neighbor.alive]
            return len(live_neighbors)
        
        # Update cell states
        for row in self.matrix:
            for cell in row:
                if cell.next_state is not None:
                    cell.alive = bool(cell.next_state)
                    cell.next_state = None

        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                cell = self.matrix[i][j]
                live_neighbor_count = get_live_neighbor_count(i, j)
                if cell.alive:
                    if live_neighbor_count not in [2, 3]:
                        cell.next_state = Cell.DEAD
                else:
                    if live_neighbor_count == 3:
                        cell.next_state = Cell.ALIVE
        

class Cell:
    DEAD = 0
    ALIVE = 1

    def __init__(self, size: int, x_pos: int, y_pos: int):
        self.alive = False
        self.next_state = None
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = size

    def toggle(self):
        self.alive = not self.alive
