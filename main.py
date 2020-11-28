import time
import sys
import os

import pygame

from cells import *


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

    font = pygame.font.SysFont('Comic Sans MS', 18)
    
    matrix_order = 40
    line_width = 1

    cell_size = (window_width / matrix_order) - line_width
    cell_matrix = CellMatrix(matrix_order)

    rectangles = []
    x_pos, y_pos = 0, 0
    for index in range(matrix_order**2):
        rectangles.append(pygame.Rect(x_pos, y_pos, cell_size, cell_size))
        if (index + 1) % matrix_order == 0:
            x_pos = 0
            y_pos += cell_size + line_width
        else:
            x_pos += cell_size + line_width


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
                    i, j = 0, 0
                    for (count, rect) in enumerate(rectangles, start=1):
                        between_x_bounds = rect.x <= mouse_x <= rect.x + cell_size + line_width
                        between_y_bounds = rect.y <= mouse_y <= rect.y + cell_size + line_width
                        if between_x_bounds and between_y_bounds:
                            break
                        elif count % matrix_order == 0:
                            i += 1
                            j = 0
                        else:
                            j += 1

                    cell_matrix.toggle_cell(i, j)


        if game_state == STATE_RUNNING:
            time.sleep(0.2)
            cell_matrix.update()

        window.fill(0)
        for (rect, cell) in zip(rectangles, cell_matrix.get_cells()):
            color = 0x0 if cell.alive else 0xffffff
            pygame.draw.rect(window, color, rect)


        pygame.draw.rect(window, 0xffffff, pygame.Rect(0, 0, int(window_width * 0.35), 50))
        text_surface = font.render(f'[SPACE] {"Pause" if game_state == STATE_RUNNING else "Start"}     [ESC] Reset', False, (0, 0, 0))
        window.blit(text_surface, (0, 10))

        pygame.display.flip()


if __name__ == "__main__":
    main()