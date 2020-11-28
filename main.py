import time
import sys
import os

import pygame

from cells import *


VERSION = '0.1.0'
WINDOW_TITLE = f'Game of Life v{VERSION}'

STATE_RUNNING = 0
STATE_PAUSED = 1
STATE_STOPPED = 2


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    
    os.environ['SDL_VIDEO_CENTERED'] = '1' # Center window

    window_height = int(pygame.display.Info().current_h * 0.8)
    window_width = window_height

    window = pygame.display.set_mode((window_width, window_height))

    font = pygame.font.SysFont('Comic Sans MS', 18)
    
    matrix_order = 30
    line_width = 2

    cell_size = (window_width / matrix_order) - line_width
    cell_matrix = CellMatrix(matrix_order)

    rectangles = []
    x_pos = 0
    y_pos = 0
    for index in range(matrix_order**2):
        rectangles.append(pygame.Rect(x_pos, y_pos, cell_size, cell_size))
        if (index + 1) % matrix_order == 0:
            x_pos = 0
            y_pos += cell_size + line_width
        else:
            x_pos += cell_size + line_width


    game_state = STATE_STOPPED
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 32: # Space
                    if game_state == STATE_RUNNING:
                        game_state = STATE_PAUSED
                    else:
                        game_state = STATE_RUNNING
                elif event.key == 27: # Escape
                    game_state = STATE_STOPPED
                    cell_matrix.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
                if game_state != STATE_RUNNING:
                    mouse_x, mouse_y = event.pos[0], event.pos[1]
                    i, j = 0, 0
                    for (count, rect) in enumerate(rectangles, start=1):
                        if (rect.x <= mouse_x <= rect.x + cell_size) and (rect.y <= mouse_y <= rect.y + cell_size):
                            break

                        if count % matrix_order == 0:
                            i += 1
                            j = 0
                        else:
                            j += 1

                    if (0 <= i < matrix_order) and (0 <= j < matrix_order):
                        cell_matrix.toggle_cell(i, j)


        if game_state == STATE_RUNNING:
            time.sleep(0.2)
            cell_matrix.update()

        window.fill(0);
        for (rect, cell) in zip(rectangles, cell_matrix.get_cells()):
            if cell.alive:
                pygame.draw.rect(window, 0, rect) 
            else:
                pygame.draw.rect(window, 0xffffff, rect)


        pygame.draw.rect(window, 0xffffff, pygame.Rect(0, 0, int(window_width * 0.35), 50))
        text_surface = font.render(f'[SPACE] {"Pause" if game_state == STATE_RUNNING else "Start"}     [ESC] Reset', False, (0, 0, 0))
        window.blit(text_surface, (0, 10))

        pygame.display.flip()


if __name__ == "__main__":
    main()