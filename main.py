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
    
    os.environ["SDL_VIDEO_CENTERED"] = "1" # Center the window

    window_size = int(pygame.display.Info().current_h * 0.8)
    window = pygame.display.set_mode((window_size, window_size))

    font = pygame.font.SysFont("consolas", 18)
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    
    cell_matrix = CellMatrix(30, window_size)

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
                elif event.key == pygame.K_h:
                    UI.set_menu_shown(not UI.get_menu_shown())
                elif event.key == pygame.K_RIGHT:
                    if game_state != STATE_RUNNING:
                        cell_matrix.update()
                elif event.key == pygame.K_LEFT:
                    if game_state != STATE_RUNNING:
                        cell_matrix.step_back()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
                if game_state != STATE_RUNNING:
                    mouse_x, mouse_y = event.pos[0], event.pos[1]
                    for cell in cell_matrix.get_cells():
                        between_x_bounds = cell.rect.x <= mouse_x <= cell.rect.x + cell.rect.size[0] + UI.get_line_width()
                        between_y_bounds = cell.rect.y <= mouse_y <= cell.rect.y + cell.rect.size[0] + UI.get_line_width()
                        if between_x_bounds and between_y_bounds:
                            cell.toggle()
                            break

        # Render cells
        window.fill(0)
        for cell in cell_matrix.get_cells():
            color = 0x0 if cell.alive else 0xffffff
            pygame.draw.rect(window, color, cell.rect)

        # Render menu
        if UI.get_menu_shown():
            menu_background = pygame.Surface((int(window_size * 0.25), int(window_size * 0.20)))
            menu_background.set_alpha(200)
            menu_background.fill((0, 0, 0))
            window.blit(menu_background, (10, 10))

            menu_text = [
                "  [ESC]  Reset",
                "[SPACE]  {}".format("Pause" if game_state == STATE_RUNNING else "Start"),
                "[<] [>]  Single Step"
            ]
            text_offset_y = window_size * 0.025
            for text in menu_text:
                text_surface = font.render(text, True, (255, 255, 255))
                window.blit(text_surface, (20, text_offset_y))
                text_offset_y += 25

            text_surface = font.render("[H] Hide Menu", True, (255, 255, 255))
            window.blit(text_surface, (20, window_size * 0.18))

        pygame.display.flip()


if __name__ == "__main__":
    main()