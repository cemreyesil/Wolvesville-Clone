import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from game import Game

# Constants
WINDOW_SIZE = 620
CONTROL_PANEL_SIZE = 400
GRID_SIZE = 4
OFFSET = 10
PLAYER_SIZE = (WINDOW_SIZE - 2 * OFFSET) // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 0)
BUTTON_HOVER_COLOR = (0, 180, 0)
TEXT_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Create the main game window
main_window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Wolvesville Main Game')

# Create the control panel window
control_panel_window = pygame.Surface((CONTROL_PANEL_SIZE, CONTROL_PANEL_SIZE))
control_panel_rect = control_panel_window.get_rect(topleft=(WINDOW_SIZE + 10, 0))  # Position next to the main window

# Load images
program_icon = pygame.image.load(os.path.join("visualization", "images", "program_icon.png"))
pygame.display.set_icon(program_icon)

profile_picture = pygame.image.load(os.path.join("visualization", "images", "default_profile.png"))
profile_picture = pygame.transform.scale(profile_picture, (PLAYER_SIZE, PLAYER_SIZE))

werewolf_icon = pygame.image.load(os.path.join("visualization", "images", "werewolf.png"))
werewolf_icon = pygame.transform.scale(werewolf_icon, (PLAYER_SIZE // 4, PLAYER_SIZE // 4))

villager_icon = pygame.image.load(os.path.join("visualization", "images", "villager.png"))
villager_icon = pygame.transform.scale(villager_icon, (PLAYER_SIZE // 4, PLAYER_SIZE // 4))

# Draw start screen
def draw_start_screen(window):
    window.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render('Start', True, TEXT_COLOR)

    button_rect = pygame.Rect(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 - 50, 200, 100)

    # Highlight button if hovered
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR

    pygame.draw.rect(window, button_color, button_rect, border_radius=20)

    text_rect = text.get_rect(center=button_rect.center)
    window.blit(text, text_rect)

    pygame.display.update()

    return button_rect

# Draw grid in the main game window
def draw_grid(window, players, selected_player=None):
    window.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = OFFSET + col * PLAYER_SIZE
            y = OFFSET + row * PLAYER_SIZE
            window.blit(profile_picture, (x, y))
            pygame.draw.rect(window, BLACK, (x, y, PLAYER_SIZE, PLAYER_SIZE), 1)

            index = row * GRID_SIZE + col
            if index < len(players):
                player = players[index]
                if player.role == "Werewolf":
                    window.blit(werewolf_icon, (x + PLAYER_SIZE - werewolf_icon.get_width(), y + PLAYER_SIZE - werewolf_icon.get_height()))
                elif player.role == "Villager":
                    window.blit(villager_icon, (x + PLAYER_SIZE - villager_icon.get_width(), y + PLAYER_SIZE - villager_icon.get_height()))

                # Highlight the selected player
                if selected_player == index:
                    pygame.draw.rect(window, (255, 0, 0), (x, y, PLAYER_SIZE, PLAYER_SIZE), 3)
                    print('-'*10+'\n'+players[selected_player].name+'\n'+players[selected_player].role+'\n'+'-'*10)

    pygame.display.update()

# Draw control panel
def draw_control_panel(control_panel, players):
    control_panel.fill(WHITE)
    font = pygame.font.Font(None, 36)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = OFFSET + col * PLAYER_SIZE
            y = OFFSET + row * PLAYER_SIZE
            index = row * GRID_SIZE + col

            if index < len(players):
                player = players[index]
                pygame.draw.rect(control_panel, BLACK, (x, y, PLAYER_SIZE, PLAYER_SIZE), 1)

                # Display player name
                text = font.render(player.name, True, BLACK)
                text_rect = text.get_rect(center=(x + PLAYER_SIZE // 2, y + PLAYER_SIZE // 2))
                control_panel.blit(text, text_rect)

    pygame.display.update()

def main():
    game_started = False
    run = True
    selected_player = None
    game = None
    button_rect = draw_start_screen(main_window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not game_started:
                    if button_rect.collidepoint(mouse_pos):
                        # Start the game
                        game_started = True
                        game = Game()
                        game.init_players()  # Initialize roles and players
                        draw_grid(main_window, game.players)
                        draw_control_panel(control_panel_window, game.players)
                elif game_started:
                    # Check for clicks on the control panel
                    for row in range(GRID_SIZE):
                        for col in range(GRID_SIZE):
                            x = OFFSET + col * PLAYER_SIZE
                            y = OFFSET + row * PLAYER_SIZE
                            index = row * GRID_SIZE + col
                            if index < len(game.players):
                                rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
                                if rect.collidepoint(mouse_pos):
                                    selected_player = index
                                    draw_grid(main_window, game.players, selected_player)

        # Display both windows
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
