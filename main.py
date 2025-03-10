import pygame
import numpy as np

# Initialize
pygame.init()
width, height = 450, 600  # Adjust screen height to add button area
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("OOXX Game")
font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_GRAY = (200, 200, 200)
BUTTON_COLOR = (100, 200, 100)  # Button color

# Button position and size
button_rect = pygame.Rect(150, 500, 200, 50)

# Game variables
board = np.full((3, 3), '', dtype=str)
player_moves = {'X': [], 'O': []}
current_player = 'O'
game_over = False

def draw_board():
    screen.fill(WHITE)
    
    # Draw vertical and horizontal lines
    line_thickness = 5
    line_length = 450
    
    # Vertical lines
    for i in range(1, 3):
        x = i * 150
        pygame.draw.line(screen, BLACK, (x, 0), (x, line_length), line_thickness)
        
    # Horizontal lines
    for i in range(1, 3):
        y = i * 150
        pygame.draw.line(screen, BLACK, (0, y), (line_length, y), line_thickness)
    
    # Draw X and O, centered in the grid
    for i in range(3):
        for j in range(3):
            if board[i, j] == 'X':
                color = BLUE if (i, j) in player_moves['X'] else LIGHT_GRAY
                text = font.render('X', True, color)
                text_rect = text.get_rect(center=(j * 150 + 75, i * 150 + 75))  # Center the letter
                screen.blit(text, text_rect)
            elif board[i, j] == 'O':
                color = RED if (i, j) in player_moves['O'] else LIGHT_GRAY
                text = font.render('O', True, color)
                text_rect = text.get_rect(center=(j * 150 + 75, i * 150 + 75))  # Center the letter
                screen.blit(text, text_rect)
    
    # Draw the button and center the text
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    button_text = button_font.render("New Game", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)  # Center the text in the button
    screen.blit(button_text, button_text_rect)

    pygame.display.flip()
     
# Check victory conditions
def check_victory(player):
    for i in range(3):
        if np.all(board[i, :] == player) or np.all(board[:, i] == player):  # Check rows and columns
            return True
    if board[0, 0] == board[1, 1] == board[2, 2] == player or board[0, 2] == board[1, 1] == board[2, 0] == player:  # Check diagonals
        return True
    return False

# Handle player moves
def make_move(x, y):
    global current_player, game_over
    
    if board[x, y] == '' and not game_over:  # Check if the cell is empty and the game is not over
        board[x, y] = current_player
        player_moves[current_player].append((x, y))
        
        # If more than three moves, remove the earliest move
        if len(player_moves[current_player]) > 3:
            old_move = player_moves[current_player].pop(0)
            board[old_move] = ''  # Remove the earliest move
        
        # Check if the current player wins
        if check_victory(current_player):
            print(f"Player {current_player} wins!")
            game_over = True
            return
        
        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'
    else:
        print("Position already occupied, choose another.")

# Reset the game
def reset_game():
    global board, player_moves, current_player, game_over
    board = np.full((3, 3), '', dtype=str)  # Reset the board
    player_moves = {'X': [], 'O': []}  # Reset moves
    current_player = 'X'  # Reset current player
    game_over = False  # Reset game over status
    draw_board()  # Redraw the board

# Main function
def main():
    draw_board()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit event
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_x, mouse_y):  # Check if the button is clicked
                    reset_game()
                elif not game_over and mouse_y < 450:  # Handle clicks within the board area
                    row, col = mouse_y // 150, mouse_x // 150
                    make_move(row, col)
                    draw_board()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press R to reset the game
                    reset_game()
    
    pygame.quit()

if __name__ == "__main__":
    main()
