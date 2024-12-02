import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
import random
from game import Game

# Check Current Working Directory
print("Current working directory: ", os.getcwd())

# Constants
WINDOW_SIZE = 620
GRID_SIZE = 4
OFFSET = 10
PLAYER_SIZE = (WINDOW_SIZE - 2*OFFSET) // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 0)
BUTTON_HOVER_COLOR = (0, 180, 0)
TEXT_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
program_icon = pygame.image.load(os.path.join("visualization", "images", "program_icon.png"))

# Load program icon
pygame.display.set_icon(program_icon)
pygame.display.set_caption('Wolvesville Player Visualization')

# Load default profile picture
profile_picture = pygame.image.load(os.path.join("visualization", "images", "default_profile.png"))
profile_picture = pygame.transform.scale(profile_picture, (PLAYER_SIZE, PLAYER_SIZE))

# Load role pictures
werewolf_icon = pygame.image.load(os.path.join("visualization", "images", "werewolf.png"))
werewolf_icon = pygame.transform.scale(werewolf_icon, (PLAYER_SIZE // 4, PLAYER_SIZE // 4))  # Scale to fit in the corner

villager_icon = pygame.image.load(os.path.join("visualization", "images", "villager.png"))
villager_icon = pygame.transform.scale(villager_icon, (PLAYER_SIZE // 4, PLAYER_SIZE // 4))  # Scale to fit in the corner

# Draw menu
def draw_start_screen():
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

# Draw players on the screen
def draw_grid(players):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = OFFSET + col * PLAYER_SIZE
            y = OFFSET + row * PLAYER_SIZE
            window.blit(profile_picture, (x, y)) # blit(source, dest, area=None, special_flags=0) -> Rect: draws a source Surface onto dest Surface
            pygame.draw.rect(window, BLACK, (x, y, PLAYER_SIZE, PLAYER_SIZE), 1)

            # Determine the player's role and draw the corresponding icon at right bottom
            index = row * GRID_SIZE + col
            if index < len(players):  
                player = players[index]
                if player.role == "Werewolf":
                    window.blit(werewolf_icon, (x + PLAYER_SIZE - werewolf_icon.get_width(), y + PLAYER_SIZE - werewolf_icon.get_height()))
                elif player.role == "Villager":
                    window.blit(villager_icon, (x + PLAYER_SIZE - villager_icon.get_width(), y + PLAYER_SIZE - villager_icon.get_height()))

    pygame.display.update()

def main():
    game_started = False
    run = True

    while run:
        if not game_started:
            button_rect = draw_start_screen()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if not game_started and button_rect.collidepoint(mouse_pos):
                    # Start the game
                    game_started = True
                    game = Game()
                    game.init_players()  # Initialize roles and players
                    draw_grid(game.players)  
        
    pygame.quit()

if __name__ == "__main__":
    main()
