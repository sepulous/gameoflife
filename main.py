import time
import sys
import os

import pygame

from cell import *
from ui import UI


VERSION = '0.1.0'
WINDOW_TITLE = f'Game of Life v{VERSION}'

STATE_RUNNING = 0
STATE_PAUSED = 1
STATE_RESET = 2


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    
    os.environ['SDL_VIDEO_CENTERED'] = '1' # Center the window

    window_height = int(pygame.display.Info().current_h * 0.8)
    window_width = window_height
    window = pygame.display.set_mode((window_width, window_height))

    font = pygame.font.SysFont('consolas', 18)
    
    matrix_order = 30

    cell_size = (window_width / matrix_order) - UI.get_line_width()
    cell_matrix = CellMatrix(matrix_order, cell_size, (window_width, window_height))

    game_state = STATE_RESET
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_state == STATE_RUNNING:
                        game_state = STATE_PAUSED
                    else:
                        game_state = STATE_RUNNING
                elif event.key == pygame.K_ESCAPE:
                    game_state = STATE_RESET
                    cell_matrix.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
                if game_state != STATE_RUNNING:
                    mouse_x, mouse_y = event.pos[0], event.pos[1]
                    for cell in cell_matrix.get_cells():
                        between_x_bounds = cell.x_pos <= mouse_x <= cell.x_pos + cell_size + UI.get_line_width()
                        between_y_bounds = cell.y_pos <= mouse_y <= cell.y_pos + cell_size + UI.get_line_width()
                        if between_x_bounds and between_y_bounds:
                            cell.toggle()
                            break


        if game_state == STATE_RUNNING and cell_matrix.should_update():
            cell_matrix.update()

        # Draw cells
        window.fill(0)
        for cell in cell_matrix.get_cells():
            color = 0x0 if cell.alive else 0xffffff
            pygame.draw.rect(window, color, pygame.Rect(cell.x_pos, cell.y_pos, cell.size, cell.size))

        # Draw menu
        pygame.draw.rect(window, 0xffffff, pygame.Rect(0, 0, int(window_width * 0.35), 50))
        text_surface = font.render(f'[SPACE] {"Pause" if game_state == STATE_RUNNING else "Start"}  [ESC] Reset', True, (0, 0, 0))
        window.blit(text_surface, (10, 15))

        pygame.display.flip()


if __name__ == "__main__":
    main()