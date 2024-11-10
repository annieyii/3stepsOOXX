import pygame
import numpy as np

# 初始化 Pygame
pygame.init()
width, height = 450, 600  # 調整畫面高度以加入按鈕區域
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("OOXX 遊戲")
font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 40)

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_GRAY = (200, 200, 200)
BUTTON_COLOR = (100, 200, 100)  # 按鈕顏色

# 按鈕位置與尺寸
button_rect = pygame.Rect(150, 500, 200, 50)

# 遊戲變數
board = np.full((3, 3), '', dtype=str)
player_moves = {'X': [], 'O': []}
current_player = 'X'
game_over = False

def draw_board():
    screen.fill(WHITE)
    
    # 畫直線和橫線，確保居中
    line_thickness = 5
    line_length = 450
    
    # 畫直線
    for i in range(1, 3):
        x = i * 150
        pygame.draw.line(screen, BLACK, (x, 0), (x, line_length), line_thickness)
        
    # 畫橫線
    for i in range(1, 3):
        y = i * 150
        pygame.draw.line(screen, BLACK, (0, y), (line_length, y), line_thickness)
    
    # 繪製 X 和 O，並置中
    for i in range(3):
        for j in range(3):
            if board[i, j] == 'X':
                color = BLUE if (i, j) in player_moves['X'] else LIGHT_GRAY
                text = font.render('X', True, color)
                text_rect = text.get_rect(center=(j * 150 + 75, i * 150 + 75))  # 字母居中
                screen.blit(text, text_rect)
            elif board[i, j] == 'O':
                color = RED if (i, j) in player_moves['O'] else LIGHT_GRAY
                text = font.render('O', True, color)
                text_rect = text.get_rect(center=(j * 150 + 75, i * 150 + 75))  # 字母居中
                screen.blit(text, text_rect)
    
    # 繪製按鈕並讓文字置中
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    button_text = button_font.render("New Game", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)  # 將文字置中在按鈕中
    screen.blit(button_text, button_text_rect)

    pygame.display.flip()
     
# 檢查勝利條件
def check_victory(player):
    for i in range(3):
        if np.all(board[i, :] == player) or np.all(board[:, i] == player):
            return True
    if board[0, 0] == board[1, 1] == board[2, 2] == player or board[0, 2] == board[1, 1] == board[2, 0] == player:
        return True
    return False

# 處理玩家移動
def make_move(x, y):
    global current_player, game_over
    
    if board[x, y] == '' and not game_over:
        board[x, y] = current_player
        player_moves[current_player].append((x, y))
        
        # 如果步數超過三步，移除最早的一步
        if len(player_moves[current_player]) > 3:
            old_move = player_moves[current_player].pop(0)
            board[old_move] = ''  # 刪除最早的一步
        
        # 檢查是否勝利
        if check_victory(current_player):
            print(f"玩家 {current_player} 勝利!")
            game_over = True
            return
        
        # 切換玩家
        current_player = 'O' if current_player == 'X' else 'X'
    else:
        print("該位置已被佔用，請選擇其他位置。")

# 遊戲重置
def reset_game():
    global board, player_moves, current_player, game_over
    board = np.full((3, 3), '', dtype=str)
    player_moves = {'X': [], 'O': []}
    current_player = 'X'
    game_over = False
    draw_board()

# 主函式
def main():
    draw_board()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_x, mouse_y):  # 檢查是否點擊了按鈕
                    reset_game()
                elif not game_over and mouse_y < 450:  # 只在點擊棋盤範圍內時處理移動
                    row, col = mouse_y // 150, mouse_x // 150
                    make_move(row, col)
                    draw_board()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 按下 R 鍵重置遊戲
                    reset_game()
    
    pygame.quit()

if __name__ == "__main__":
    main()