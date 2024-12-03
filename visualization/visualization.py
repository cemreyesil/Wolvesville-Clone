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
TEXT_BOX_HEIGHT = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 0)
BUTTON_HOVER_COLOR = (0, 180, 0)
TEXT_COLOR = (255, 255, 255)
GRAY = (200, 200, 200)

# Initialize Pygame
pygame.init()

# Create the main game window
main_window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + TEXT_BOX_HEIGHT))
pygame.display.set_caption('Wolvesville Main Game')

# Load images
program_icon = pygame.image.load(os.path.join("visualization", "images", "program_icon.png"))
pygame.display.set_icon(program_icon)

profile_picture = pygame.image.load(os.path.join("visualization", "images", "default_profile.png"))
profile_picture = pygame.transform.scale(profile_picture, (PLAYER_SIZE, PLAYER_SIZE))

werewolf_icon = pygame.image.load(os.path.join("visualization", "images", "werewolf.png"))
werewolf_icon = pygame.transform.scale(werewolf_icon, (PLAYER_SIZE // 4, PLAYER_SIZE // 4))

villager_icon = pygame.image.load(os.path.join("visualization", "images", "villager.png"))
villager_icon = pygame.transform.scale(villager_icon, (PLAYER_SIZE // 4, PLAYER_SIZE // 4))

voting_hand_icon = pygame.image.load(os.path.join("visualization", "images", "Voting_Hand.png"))
voting_hand_icon = pygame.transform.scale(voting_hand_icon, (PLAYER_SIZE // 2.8, PLAYER_SIZE // 2.8))  # Adjust the size to fit

# Message Log
messages = []

# Draw the text box for player input
def draw_text_box(window, current_input, scroll_position, max_scroll, game, selected_player):
    # Define text box and message log areas
    text_box_rect = pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, TEXT_BOX_HEIGHT)
    pygame.draw.rect(window, GRAY, text_box_rect)

    # Draw current input text
    font = pygame.font.SysFont("cambria", 20) # For player numbers: "arialblack", for dead "kristenitc"
    input_text = font.render(current_input, True, BLACK)
    input_rect = pygame.Rect(0, WINDOW_SIZE + TEXT_BOX_HEIGHT - 40, WINDOW_SIZE, 40)
    pygame.draw.rect(window, WHITE, input_rect)  # Background for the input area
    window.blit(input_text, (10, WINDOW_SIZE + TEXT_BOX_HEIGHT - 30))

    # Define the visible area for the message log
    log_height = TEXT_BOX_HEIGHT - 40  # Reserve 40px for the input area
    visible_messages = log_height // 20  # Number of messages visible at once

    # Calculate the range of messages to display
    end_index = min(len(messages), len(messages) - scroll_position)
    start_index = max(0, end_index - visible_messages)

    # Draw message log
    y_offset = WINDOW_SIZE  # Start drawing at the top of the log area
    player = game.players[selected_player] if selected_player is not None else None
    if len(messages) == 0 and game.current_day is False and (selected_player is None or player.role == "Villager"):
        restricted_message = "You cannot talk or see messages at night."
        message_text = font.render(restricted_message, True, BLACK)
        window.blit(message_text, (10, y_offset))
    else:
        for message in messages[start_index:end_index]:
            if game.current_day or (selected_player is not None and player.role == "Werewolf"):
                # Only display messages to werewolves at night or to everyone during the day
                message_text = font.render(message, True, BLACK)
                window.blit(message_text, (10, y_offset))
                y_offset += 20
            else:
                restricted_message = "You cannot talk or see messages at night."
                message_text = font.render(restricted_message, True, BLACK)
                window.blit(message_text, (10, y_offset))
                break

    # Draw the scrollbar
    scrollbar_rect = pygame.Rect(WINDOW_SIZE - 20, WINDOW_SIZE, 10, log_height)
    pygame.draw.rect(window, BLACK, scrollbar_rect)

    # Draw the scroll thumb
    if max_scroll > 0:
        thumb_height = max(20, log_height // max_scroll)  # Minimum size of the thumb
        thumb_position = ((max_scroll - scroll_position) / max_scroll) * (log_height - thumb_height)
        thumb_rect = pygame.Rect(WINDOW_SIZE - 20, WINDOW_SIZE + thumb_position, 10, thumb_height)
        pygame.draw.rect(window, WHITE, thumb_rect)

    pygame.display.update()

# Draw start screen
def draw_start_screen(window):
    window.fill(WHITE)
    font = pygame.font.SysFont("timesnewroman", 74)
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

# Draw the player grid on the main window
def draw_grid(window, players, selected_player=None):
    window.fill(WHITE, (0, 0, WINDOW_SIZE, WINDOW_SIZE))
    playernumber_font = pygame.font.SysFont("arialblack", 18)

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

                # Draw the player's number at the bottom-left with a white border
                shown_number = str(index+1)
                number_text = playernumber_font.render(shown_number, True, BLACK)  # Convert index to 1-based numbering
                number_x = x + 5  # Slight offset for padding
                number_y = y + PLAYER_SIZE - number_text.get_height() - 5  # Adjust position slightly above the edge
                # Render white border by drawing text multiple times slightly offset
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                    border_text = playernumber_font.render(shown_number, True, WHITE)
                    window.blit(border_text, (number_x + dx, number_y + dy))
                window.blit(number_text, (number_x, number_y))

                # Draw the number of votes that player got
                if player.votes_taken > 0: # Only show if the player has votes
                    hand_x = x + PLAYER_SIZE - voting_hand_icon.get_width() - 100
                    hand_y = y - 9  # Top-right corner
                    window.blit(voting_hand_icon, (hand_x, hand_y))

                    # Overlay the vote count on top of the hand
                    shown_vote = str(player.votes_taken)
                    print(shown_vote)
                    vote_text = playernumber_font.render(shown_vote, True, BLACK)  # Convert index to 1-based numbering
                    vote_x = x + PLAYER_SIZE - vote_text.get_width() - 120  # Align to the top-right corner
                    vote_y = y + 5  # Slight offset from the top edge
                    # Render white border by drawing text multiple times slightly offset
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                        border_vote_text = playernumber_font.render(shown_vote, True, WHITE)
                        window.blit(border_vote_text, (vote_x + dx, vote_y + dy))
                    window.blit(vote_text, (vote_x, vote_y))

                # Highlight the selected player
                if selected_player == index:
                    pygame.draw.rect(window, (255, 0, 0), (x, y, PLAYER_SIZE, PLAYER_SIZE), 3)
                    print('-'*10+'\n'+players[selected_player].name+'\n'+players[selected_player].role+'\n'+'-'*10)

    pygame.display.update()

def main():
    game_started = False
    run = True
    selected_player = None
    current_input = ""
    scroll_position = 0
    game = None

    button_rect = draw_start_screen(main_window)

    while run:
        if game_started:
            max_scroll = max(0, len(messages) - ((TEXT_BOX_HEIGHT - 40) // 20))
            draw_text_box(main_window, current_input, scroll_position, max_scroll, game, selected_player)

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
                elif game_started and mouse_pos[1] < WINDOW_SIZE:
                    '''
                      1 - left click
                      2 - middle click
                      3 - right click
                      4 - scroll up
                      5 - scroll down
                    '''
                    if event.button == 1 or event.button == 3:  # Left mouse button or Right mouse button
                        # Check for clicks on the player grid
                        for row in range(GRID_SIZE):
                            for col in range(GRID_SIZE):
                                x = OFFSET + col * PLAYER_SIZE
                                y = OFFSET + row * PLAYER_SIZE
                                index = row * GRID_SIZE + col
                                if index < len(game.players):
                                    rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
                                    if rect.collidepoint(mouse_pos):
                                        if event.button == 3 and (game.current_day or (selected_player is not None and game.players[selected_player].role == "Werewolf")):
                                            boolean = game.get_votes(selected_player, index)
                                            if boolean: # If voting occured
                                                draw_grid(main_window, game.players, selected_player)

                                        elif event.button == 1:
                                            selected_player = index
                                            draw_grid(main_window, game.players, selected_player)           
                    
            elif event.type == pygame.KEYDOWN:
                if game_started:
                    if event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1] # backspace key -> delete last letter
                    elif event.key == pygame.K_RETURN:
                        # Submit the current message
                        if selected_player is not None:
                            player = game.players[selected_player]
                            if game.current_day or player.role == "Werewolf":
                                messages.append(f"{player.name}: {current_input}")
                        current_input = ""                        
                    else:
                        current_input += event.unicode
            elif event.type == pygame.MOUSEWHEEL:
                # Adjust scroll position with the mouse wheel
                scroll_position += event.y  # Reverse the scroll direction
                scroll_position = max(0, min(scroll_position, len(messages) - ((TEXT_BOX_HEIGHT - 40) // 20)))

    pygame.quit()

if __name__ == "__main__":
    main()
