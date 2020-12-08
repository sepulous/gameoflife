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

    window_size = int(pygame.display.Info().current_h * 0.8)
    window = pygame.display.set_mode((window_size, window_size))

    font = pygame.font.SysFont('consolas', 18)
    
    matrix_order = 30
    cell_matrix = CellMatrix(matrix_order, window_size)

    game_state = STATE_RESET
    while True:
        if game_state == STATE_RUNNING:
            pygame.time.Clock().tick(UI.get_updates_per_second())
            cell_matrix.update()
            
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
                        between_x_bounds = cell.rect.x <= mouse_x <= cell.rect.x + cell.rect.size[0] + UI.get_line_width()
                        between_y_bounds = cell.rect.y <= mouse_y <= cell.rect.y + cell.rect.size[0] + UI.get_line_width()
                        if between_x_bounds and between_y_bounds:
                            cell.toggle()
                            break

        # Draw cells
        window.fill(0)
        for cell in cell_matrix.get_cells():
            color = 0x0 if cell.alive else 0xffffff
            pygame.draw.rect(window, color, cell.rect)

        # Draw menu
        pygame.draw.rect(window, 0xffffff, pygame.Rect(0, 0, int(window_size * 0.35), 50))
        text_surface = font.render(f'[SPACE] {"Pause" if game_state == STATE_RUNNING else "Start"}  [ESC] Reset', True, (0, 0, 0))
        window.blit(text_surface, (10, 15))

        pygame.display.flip()


if __name__ == "__main__":
    main()