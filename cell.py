from typing import List
import time

from pygame import Rect

from ui import UI

class CellMatrix:
    def __init__(self, matrix_size: int, window_size: int):
        self.matrix_size = matrix_size
        self.matrix = self._generate_matrix(matrix_size, window_size)
        self.last_update = 0
        self.history = []

    def _generate_matrix(self, matrix_size: int, window_size: int):
        matrix = [[] for _ in range(matrix_size)]
        cell_size = (window_size / matrix_size) - UI.get_line_width()
        x_pos, y_pos = 0, 0
        for row in matrix:
            for index in range(matrix_size):
                row.append(Cell(Rect(x_pos, y_pos, cell_size, cell_size)))
                if (index + 1) % matrix_size == 0:
                    x_pos = 0
                    y_pos += cell_size + UI.get_line_width()
                else:
                    x_pos += cell_size + UI.get_line_width()

        return matrix

    def _save_current_state(self):
        if len(self.history) >= 30:
            del self.history[0]
            
        self.history.append([
            [cell.alive for cell in row] for row in self.matrix
        ])

    def get_cells(self):
        return [cell for row in self.matrix for cell in row] # Flatten 2D matrix

    def reset(self):
        for row in self.matrix:
            for cell in row:
                cell.alive = False

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

        self._save_current_state()
        print(len(self.history))
        
        # Update cell states
        for row in self.matrix:
            for cell in row:
                if cell.next_state is not None:
                    cell.alive = bool(cell.next_state)
                    cell.next_state = None

        # Determine cell states for next generation
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

    def step_back(self):
        if len(self.history) > 0:
            for (i, row) in enumerate(self.history[-1]):
                for (j, state) in enumerate(row):
                    cell = self.matrix[i][j]
                    cell.alive = state
                    cell.next_state = None
            del self.history[-1]



class Cell:
    DEAD = 0
    ALIVE = 1

    def __init__(self, rect: Rect):
        self.alive = False
        self.next_state = None
        self.rect = rect

    def toggle(self):
        self.alive = not self.alive
