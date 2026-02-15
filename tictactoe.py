import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SQUARE_SIZE = 150
WIDTH = SQUARE_SIZE * 3
HEIGHT = SQUARE_SIZE * 3 + 150  # Increased height for name input/restart
LINE_COLOR = (20, 20, 20)  # Deep charcoal, elegant contrast
BG_COLOR = (30, 30, 60)  # Dark indigo blue, gives neon glow backdrop
CIRCLE_COLOR = (0, 255, 255)  # Cyan (bright & modern)
CROSS_COLOR = (255, 105, 180)  # Hot pink (pops out beautifully)
FONT_SIZE = 40
FONT_COLOR = (255, 255, 255)  # White, stands out on dark BG
BUTTON_COLOR = (0, 191, 255)  # Deep Sky Blue
BUTTON_HOVER_COLOR = (0, 140, 255)  # Richer Blue on hover
BUTTON_CLICK_COLOR = (0, 100, 200)  # Darker Blue on click
BUTTON_TEXT_COLOR = (255, 255, 255)  # Pure white for contrast
INPUT_BOX_COLOR = (50, 50, 70)  # Dark bluish-gray, subtle
INPUT_TEXT_COLOR = (255, 255, 255)  # White for clean visibility
INPUT_BOX_ACTIVE_COLOR = (70, 70, 100)  # Slightly lighter bluish-gray
CURSOR_COLOR = (0, 255, 127)  # Neon green cursor
CURSOR_BLINK_RATE = 500
WIN_LINE_COLOR = (255, 255, 0)  # Bright yellow for win effect
WIN_LINE_WIDTH = 5
THICK_LINE_WIDTH = 7  # Increased line thickness

# New font
COOL_FONT_PATH = "font/Movie_font.ttf"  # Download from (dafont.com)
try:
    COOL_FONT = pygame.font.Font(COOL_FONT_PATH, 32)
except FileNotFoundError:
    print(f"Font file {COOL_FONT_PATH} not found. Using default font.")
    COOL_FONT = pygame.font.Font(None, FONT_SIZE)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, FONT_SIZE)

# Game variables
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False
winner = None
player1_name = ""
player2_name = ""
winning_line_start = None
winning_line_end = None
first_player = None  # To store who starts first

# Game state
in_menu = True
in_name_input = False
in_player_select = False # Added for player select state
in_game = False

# Menu variables
menu_options = ["Play", "Quit"]
menu_rects = []
current_button_color = [BUTTON_COLOR, BUTTON_COLOR]
# Name input variables
input_box1 = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 3, 200, 50)
input_box2 = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2, 200, 50)
color1 = INPUT_BOX_COLOR
color2 = INPUT_BOX_COLOR
active_box = None
cursor_visible = False
cursor_timer = 0
message_text = ""  # Added for displaying messages

# End game buttons
restart_button_rect = None
restart_button_color = BUTTON_COLOR
main_menu_button_rect = None
main_menu_button_color = BUTTON_COLOR

# Player selection variables
x_button_rect = None
o_button_rect = None
x_button_color = BUTTON_COLOR
o_button_color = BUTTON_COLOR

# Load sound effects  (all sound downloaded from pixabay.com)
click_sound = pygame.mixer.Sound("click.wav")
win_music = pygame.mixer.Sound("win.wav")

# New sound effects
menu_click_sound = pygame.mixer.Sound("menu_click.mp3")
name_input_click_sound = pygame.mixer.Sound("name_input_click.mp3")
game_start_sound = pygame.mixer.Sound("game_start.mp3")

# Function to draw the board
def draw_board():
    for row in range(3):
        for col in range(3):
            pygame.draw.rect(screen, BG_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0)
            # Increased line thickness here
            pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, 3 * SQUARE_SIZE), THICK_LINE_WIDTH)
            # Increased line thickness here
            pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (3 * SQUARE_SIZE, row * SQUARE_SIZE), THICK_LINE_WIDTH)

            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3, 7) # Increased thickness
            elif board[row][col] == "X":
                # Increased thickness here
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), THICK_LINE_WIDTH)
                # Increased thickness here
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), THICK_LINE_WIDTH)

# Function to check for a win
def check_win():
    global winning_line_start, winning_line_end
    # Check rows
    for row in range(3):
        if all(board[row][0] == board[row][col] and board[row][col] != "" for col in range(3)):
            winning_line_start = (0, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            winning_line_end = (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            return board[row][0]

    # Check columns
    for col in range(3):
        if all(board[0][col] == board[row][col] and board[row][col] != "" for row in range(3)):
            winning_line_start = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 0)
            winning_line_end = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 150)
            return board[0][col]

    # Check diagonals
    if all(board[i][i] == board[0][0] and board[i][i] != "" for i in range(3)):
        winning_line_start = (0, 0)
        winning_line_end = (WIDTH, HEIGHT - 150)
        return board[0][0]
    if all(board[i][2 - i] == board[0][2] and board[i][2 - i] != "" for i in range(3)):
        winning_line_start = (WIDTH, 0)
        winning_line_end = (0, HEIGHT - 150)
        return board[0][2]

    # Check for a tie
    if all("" not in row for row in board):
        return "Tie"
    return None

# Function to handle a click
def handle_click(pos):
    global current_player, game_over, winner
    if not game_over:
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        if board[row][col] == "":
            board[row][col] = current_player
            winner = check_win()
            pygame.mixer.Sound.play(click_sound)  # Play click sound
            if winner:
                game_over = True
                pygame.mixer.Sound.play(win_music)
            else:
                current_player = "O" if current_player == "X" else "X"

# Function to draw the main menu
def draw_menu():
    screen.fill(BG_COLOR)
    # Title
    title_text = COOL_FONT.render("Tic Tac Toe", True, FONT_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # Menu options
    menu_rects.clear()
    for i, option in enumerate(menu_options):
        text_color = BUTTON_TEXT_COLOR
        option_text = COOL_FONT.render(option, True, text_color)
        option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))  # Increased spacing
        pygame.draw.rect(screen, current_button_color[i], option_rect.inflate(60, 30), border_radius=10) # Added border radius
        screen.blit(option_text, option_rect)
        menu_rects.append(option_rect)

    pygame.display.flip()

# Function to handle menu clicks
def handle_menu_click(pos):
    global in_menu, in_name_input, current_button_color
    for i, rect in enumerate(menu_rects):
        if rect.collidepoint(pos):
            current_button_color[i] = BUTTON_CLICK_COLOR
            pygame.display.flip()
            pygame.time.delay(100)
            pygame.mixer.Sound.play(menu_click_sound)
            current_button_color[i] = BUTTON_HOVER_COLOR

            if i == 0:  # Play
                in_menu = False
                in_name_input = True
            elif i == 1:  # Quit
                pygame.quit()
                sys.exit()
            break

# Function to draw the name input screen
def draw_name_input():
    global cursor_visible, message_text
    screen.fill(BG_COLOR)
    title_text = COOL_FONT.render("Enter Player Names", True, FONT_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))  # Positioned title
    screen.blit(title_text, title_rect)

    text1 = COOL_FONT.render("X's Name:", True, FONT_COLOR)
    screen.blit(text1, (input_box1.x - text1.get_width() - 10, input_box1.y + 10)) # Adjusted X position
    pygame.draw.rect(screen, color1, input_box1, 2, border_radius=5)
    text_surface1 = COOL_FONT.render(player1_name, True, INPUT_TEXT_COLOR)
    screen.blit(text_surface1, (input_box1.x + 10, input_box1.y + 10))
    if active_box == 1 and cursor_visible:
        cursor_pos = input_box1.x + 10 + text_surface1.get_width() + 2
        pygame.draw.line(screen, CURSOR_COLOR, (cursor_pos, input_box1.y + 10), (cursor_pos, input_box1.y + 10 + text_surface1.get_height()), 2)

    text2 = COOL_FONT.render("O's Name:", True, FONT_COLOR)
    screen.blit(text2, (input_box2.x - text2.get_width() - 10, input_box2.y + 10)) # Adjusted O position
    pygame.draw.rect(screen, color2, input_box2, 2, border_radius=5)
    text_surface2 = COOL_FONT.render(player2_name, True, INPUT_TEXT_COLOR)
    screen.blit(text_surface2, (input_box2.x + 10, input_box2.y + 10))
    if active_box == 2 and cursor_visible:
        cursor_pos = input_box2.x + 10 + text_surface2.get_width() + 2
        pygame.draw.line(screen, CURSOR_COLOR, (cursor_pos, input_box2.y + 10), (cursor_pos, input_box2.y + 10 + text_surface2.get_height()), 2)

    start_button_text = COOL_FONT.render("Start Game", True, BUTTON_TEXT_COLOR)
    start_button_rect = start_button_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect.inflate(80, 30), border_radius=10)
    screen.blit(start_button_text, start_button_rect)

    # Display the message
    message_render = font.render(message_text, True, (255,0,0)) # Changed color to red
    message_rect = message_render.get_rect(center=(WIDTH // 2, HEIGHT - 100))  # Positioned above start button
    screen.blit(message_render, message_rect)

    return start_button_rect

# Function to handle name input
def handle_name_input(event, start_button_rect):
    global player1_name, player2_name, in_name_input, in_player_select, active_box, color1, color2, cursor_visible, cursor_timer, message_text
    if event.type == pygame.MOUSEBUTTONDOWN:
        if input_box1.collidepoint(event.pos):
            active_box = 1
            color1 = INPUT_BOX_ACTIVE_COLOR
            color2 = INPUT_BOX_COLOR
            pygame.mixer.Sound.play(name_input_click_sound)
            message_text = ""  # Clear message when switching input boxes
        elif input_box2.collidepoint(event.pos):
            active_box = 2
            color2 = INPUT_BOX_ACTIVE_COLOR
            color1 = INPUT_BOX_COLOR
            pygame.mixer.Sound.play(name_input_click_sound)
            message_text = ""  # Clear message when switching input boxes
        else:
            active_box = None
            color1 = INPUT_BOX_COLOR
            color2 = INPUT_BOX_COLOR
            cursor_visible = False
            message_text = "" #clear message

        if start_button_rect.collidepoint(event.pos):
            if not player1_name:
                player1_name = "X"
            if not player2_name:
                player2_name = "O"
            in_name_input = False
            in_player_select = True # Go to player select instead of in_game
            pygame.mixer.Sound.play(game_start_sound)
            cursor_visible = False
            message_text = ""

    if event.type == pygame.KEYDOWN:
        cursor_visible = True
        cursor_timer = pygame.time.get_ticks()

        if active_box == 1:
            if event.key == pygame.K_RETURN:
                active_box = 2
                color1 = INPUT_BOX_COLOR
                color2 = INPUT_BOX_ACTIVE_COLOR
                message_text = ""  # Clear message on Enter
            elif event.key == pygame.K_BACKSPACE:
                player1_name = player1_name[:-1]
                message_text = "" #clear message
            else:
                if len(player1_name) < 5:  # Limit to 5 characters
                    player1_name += event.unicode
                else:
                    message_text = "Maximum character limit reached"
        elif active_box == 2:
            if event.key == pygame.K_RETURN:
                if not player1_name:
                    player1_name = "X"
                if not player2_name:
                    player2_name = "O"
                in_name_input = False
                in_player_select = True # Go to player select.
                pygame.mixer.Sound.play(game_start_sound)
                cursor_visible = False
                message_text = ""  # Clear message on Enter
            elif event.key == pygame.K_BACKSPACE:
                player2_name = player2_name[:-1]
                message_text = "" # clear message
            else:
                if len(player2_name) < 5:  # Limit to 5 characters
                    player2_name += event.unicode
                else:
                    message_text = "Maximum character limit reached"

# Function to draw the player selection screen
def draw_player_select():
    global x_button_rect, o_button_rect, x_button_color, o_button_color
    screen.fill(BG_COLOR)
    title_text = COOL_FONT.render("Who goes first?", True, FONT_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)

    x_text = COOL_FONT.render(f"{player1_name} (X)", True, BUTTON_TEXT_COLOR)
    x_button_width = x_text.get_width() + 60
    x_button_height = x_text.get_height() + 20
    x_button_x = WIDTH // 4 - x_button_width // 2
    x_button_y = HEIGHT // 2
    x_button_rect = pygame.Rect(x_button_x, x_button_y, x_button_width, x_button_height)
    pygame.draw.rect(screen, x_button_color, x_button_rect, border_radius=10)
    screen.blit(x_text, (x_button_x + 30, x_button_y + 10))

    o_text = COOL_FONT.render(f"{player2_name} (O)", True, BUTTON_TEXT_COLOR)
    o_button_width = o_text.get_width() + 60
    o_button_height = o_text.get_height() + 20
    o_button_x = 3 * WIDTH // 4 - o_button_width // 2
    o_button_y = HEIGHT // 2
    o_button_rect = pygame.Rect(o_button_x, o_button_y, o_button_width, o_button_height)
    pygame.draw.rect(screen, o_button_color, o_button_rect, border_radius=10)
    screen.blit(o_text, (o_button_x + 30, o_button_y + 10))

    pygame.display.flip()

# Function to handle player selection
def handle_player_select(pos):
    global current_player, in_player_select, in_game, first_player, x_button_color, o_button_color
    if x_button_rect.collidepoint(pos):
        x_button_color = BUTTON_CLICK_COLOR
        pygame.display.flip()
        pygame.time.delay(100)
        pygame.mixer.Sound.play(menu_click_sound)
        x_button_color = BUTTON_HOVER_COLOR
        current_player = "X"
        first_player = "X" # Store who goes first
        in_player_select = False
        in_game = True
    elif o_button_rect.collidepoint(pos):
        o_button_color = BUTTON_CLICK_COLOR
        pygame.display.flip()
        pygame.time.delay(100)
        pygame.mixer.Sound.play(menu_click_sound)
        o_button_color = BUTTON_HOVER_COLOR
        current_player = "O"
        first_player = "O"
        in_player_select = False
        in_game = True

# Function to draw the game screen
def draw_game():
    global restart_button_rect, main_menu_button_rect, main_menu_button_color, winning_line_start, winning_line_end
    screen.fill(BG_COLOR)
    draw_board()
    # Display player names
    player_x_text = COOL_FONT.render(f"X: {player1_name}", True, CROSS_COLOR)
    player_o_text = COOL_FONT.render(f"O: {player2_name}", True, CIRCLE_COLOR)
    screen.blit(player_x_text, (10, HEIGHT - 140))
    screen.blit(player_o_text, (10, HEIGHT - 100))

    if game_over:
        if winner == "Tie":
            result_text = COOL_FONT.render("It's a Tie!", True, FONT_COLOR)
        else:
            winner_name = player1_name if winner == "X" else player2_name
            result_text = COOL_FONT.render(f"{winner_name} wins!", True, FONT_COLOR)
        result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        screen.blit(result_text, result_rect)

        if winning_line_start and winning_line_end:
            pygame.draw.line(screen, WIN_LINE_COLOR, winning_line_start, winning_line_end, WIN_LINE_WIDTH)

        restart_text = COOL_FONT.render("Restart", True, BUTTON_TEXT_COLOR)
        restart_button_width = restart_text.get_width() + 60
        restart_button_height = restart_text.get_height() + 20
        restart_button_x = WIDTH // 4 - restart_button_width // 2
        restart_button_y = HEIGHT - 35 - restart_button_height // 2
        restart_button_rect = pygame.Rect(restart_button_x, restart_button_y, restart_button_width, restart_button_height)
        pygame.draw.rect(screen, restart_button_color, restart_button_rect, border_radius=10)
        screen.blit(restart_text, (restart_button_x + 30, restart_button_y + 10))
    else:
        current_player_name = player1_name if current_player == "X" else player2_name
        turn_text = COOL_FONT.render(f"{current_player_name}'s turn", True, FONT_COLOR)
        turn_rect = turn_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
        screen.blit(turn_text, turn_rect)
        restart_button_rect = None
        winning_line_start = None
        winning_line_end = None

    # Always draw Main Menu button
    main_menu_text = COOL_FONT.render("Main Menu", True, BUTTON_TEXT_COLOR)
    main_menu_button_width = main_menu_text.get_width() + 10
    main_menu_button_height = main_menu_text.get_height() + 20
    main_menu_button_x = 3 * WIDTH // 4 - main_menu_button_width // 2
    main_menu_button_y = HEIGHT - 35 - main_menu_button_height // 2
    main_menu_button_rect = pygame.Rect(main_menu_button_x+30, main_menu_button_y, main_menu_button_width, main_menu_button_height)
    pygame.draw.rect(screen, main_menu_button_color, main_menu_button_rect, border_radius=10)
    screen.blit(main_menu_text, (main_menu_button_x + 30, main_menu_button_y + 10))

    pygame.display.flip()

# Function to handle restart button click
def handle_restart_click(pos):
    global game_over, board, current_player, winner, restart_button_color, in_game, winning_line_start, winning_line_end, first_player
    if restart_button_rect and restart_button_rect.collidepoint(pos):
        restart_button_color = BUTTON_CLICK_COLOR
        pygame.display.flip()
        pygame.time.delay(100)
        pygame.mixer.Sound.play(menu_click_sound)
        restart_button_color = BUTTON_HOVER_COLOR

        game_over = False
        board = [["" for _ in range(3)] for _ in range(3)]
        current_player = first_player # Start with the player who was selected first.
        winner = None
        in_game = True
        pygame.mixer.music.stop()
        winning_line_start = None
        winning_line_end = None

# Function to handle main menu button click
def handle_main_menu_click(pos):
    global game_over, in_game, in_menu, board, current_player, winner, main_menu_button_color, winning_line_start, winning_line_end
    if main_menu_button_rect and main_menu_button_rect.collidepoint(pos):
        main_menu_button_color = BUTTON_CLICK_COLOR
        pygame.display.flip()
        pygame.time.delay(100)
        pygame.mixer.Sound.play(menu_click_sound)
        main_menu_button_color = BUTTON_HOVER_COLOR

        game_over = False
        in_game = False
        in_menu = True
        board = [["" for _ in range(3)] for _ in range(3)]
        current_player = "X"
        winner = None
        pygame.mixer.music.stop()
        winning_line_start = None
        winning_line_end = None

# Game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_menu:
            for i, rect in enumerate(menu_rects):
                if rect.collidepoint(mouse_pos):
                    current_button_color[i] = BUTTON_HOVER_COLOR
                else:
                    current_button_color[i] = BUTTON_COLOR

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                handle_menu_click(pos)
            draw_menu()

        elif in_name_input:
            start_button_rect_name_input = draw_name_input()
            handle_name_input(event, start_button_rect_name_input)
            pygame.display.flip()

        elif in_player_select: # Handle player select page
            draw_player_select()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                handle_player_select(pos)
            for button, color in [(x_button_rect, x_button_color), (o_button_rect, o_button_color)]:
                if button and button.collidepoint(mouse_pos):
                    if button == x_button_rect:
                        x_button_color = BUTTON_HOVER_COLOR
                    else:
                        o_button_color = BUTTON_HOVER_COLOR
                else:
                    if button == x_button_rect:
                        x_button_color = BUTTON_COLOR
                    else:
                        o_button_color = BUTTON_COLOR

        elif in_game:
            # Always handle hover over Main Menu button
            if main_menu_button_rect and main_menu_button_rect.collidepoint(mouse_pos):
                main_menu_button_color = BUTTON_HOVER_COLOR
            else:
                main_menu_button_color = BUTTON_COLOR

            if game_over:
                if restart_button_rect and restart_button_rect.collidepoint(mouse_pos):
                    restart_button_color = BUTTON_HOVER_COLOR
                else:
                    restart_button_color = BUTTON_COLOR

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Handle Main Menu click at all times
                if main_menu_button_rect and main_menu_button_rect.collidepoint(pos):
                    handle_main_menu_click(pos)
                elif game_over and restart_button_rect and restart_button_rect.collidepoint(pos):
                    handle_restart_click(pos)
                elif pos[1] < 3 * SQUARE_SIZE and not game_over:
                    handle_click(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_game = False
                    in_menu = True
                    pygame.mixer.music.stop()

    # Cursor blinking
    if active_box is not None:
        if current_time - cursor_timer > CURSOR_BLINK_RATE:
            cursor_timer = current_time
            cursor_visible = not cursor_visible

    if in_game:
        draw_game()

pygame.quit()
sys.exit()
