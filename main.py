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

    font = pygame.font.SysFont("consolas", 18)
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)    
    
    os.environ["SDL_VIDEO_CENTERED"] = "1" # Center the window
    initial_window_size = int(pygame.display.Info().current_h * 0.8)
    cell_matrix = CellMatrix(30, initial_window_size)
    cell_size = cell_matrix.get_cells()[0].rect.size[0]
    window_size = UI.get_line_width()*31 + 30*cell_size
    window = pygame.display.set_mode((window_size, window_size))

    current_toggled_cells = []
    current_iteration = 0
    max_iterations = 0
    game_state = STATE_RESET

    while True:
        if game_state == STATE_RUNNING:
            pygame.time.Clock().tick(UI.get_update_speed())
            cell_matrix.update()
            current_iteration += 1
            if current_iteration > max_iterations:
                max_iterations += 1
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Pause/reset
                if event.key == pygame.K_SPACE:
                    game_state = not game_state
                elif event.key == pygame.K_ESCAPE:
                    game_state = STATE_RESET
                    cell_matrix.reset()
                    current_iteration = max_iterations = 0
                # Show/hide menu
                elif event.key == pygame.K_h:
                    UI.set_menu_shown(not UI.get_menu_shown())
                # Single-stepping
                elif event.key == pygame.K_RIGHT:
                    if game_state == STATE_PAUSED:
                        cell_matrix.update()
                        current_iteration += 1
                        if current_iteration > max_iterations:
                            max_iterations += 1
                elif event.key == pygame.K_LEFT:
                    if game_state == STATE_PAUSED:
                        if cell_matrix.step_back():
                            if current_iteration > 0:
                                current_iteration -= 1
                # Adjusting update speed
                elif event.key == pygame.K_UP:
                    UI.set_update_speed(UI.get_update_speed() + 1)
                elif event.key == pygame.K_DOWN:
                    UI.set_update_speed(UI.get_update_speed() - 1)
            # Toggling cells
            elif pygame.mouse.get_pressed()[0]:
                if game_state != STATE_RUNNING:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for cell in cell_matrix.get_cells():
                        between_x_bounds = cell.rect.x <= mouse_x <= cell.rect.x + cell.rect.size[0] + UI.get_line_width()
                        between_y_bounds = cell.rect.y <= mouse_y <= cell.rect.y + cell.rect.size[0] + UI.get_line_width()
                        if (between_x_bounds and between_y_bounds) and (id(cell) not in current_toggled_cells):
                            cell.toggle()
                            current_toggled_cells.append(id(cell))
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                current_toggled_cells.clear()


        # Render cells
        window.fill(0)
        for cell in cell_matrix.get_cells():
            color = 0x0 if cell.alive else 0xffffff
            pygame.draw.rect(window, color, cell.rect)

        # Render menu
        if UI.get_menu_shown():
            menu_background = pygame.Surface((int(window_size * 0.28), int(window_size * 0.28)))
            menu_background.set_alpha(200)
            menu_background.fill((0, 0, 0))
            window.blit(menu_background, (10, 10))

            menu_text = [
                "Iteration: {}/{}".format(current_iteration, max_iterations),
                "Update Speed: {}/s".format(UI.get_update_speed()),
                "",
                "  [ESC]  Reset",
                "[SPACE]  {}".format("Pause" if game_state == STATE_RUNNING else "Start"),
                "[<] [>]  Single Step",
                "[Ʌ] [V]  Update Speed",
            ]
            text_offset_y = window_size * 0.025
            for text in menu_text:
                text_surface = font.render(text, True, (255, 255, 255))
                window.blit(text_surface, (20, text_offset_y))
                text_offset_y += 25

            text_surface = font.render("[H] Hide Menu", True, (255, 255, 255))
            window.blit(text_surface, (20, text_offset_y + 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()