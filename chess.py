import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT = (255, 255, 0)

# Font for pieces (using Unicode chess symbols)
font = pygame.font.SysFont('segoeuisymbol', 50)

# Chess pieces Unicode
PIECES = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

# Initial board setup (8x8, rows 0-7, cols 0-7)
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# Game state
selected_square = None
turn = 'white'  # 'white' or 'black'

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            if selected_square and selected_square == (row, col):
                color = HIGHLIGHT
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.':
                text = font.render(PIECES[piece], True, BLACK if piece.isupper() else WHITE)
                screen.blit(text, (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 5))

def is_valid_move(start, end):
    # Simplified validation: just check if destination is empty or enemy piece, and basic piece movement
    piece = board[start[0]][start[1]]
    target = board[end[0]][end[1]]
    
    # Can't move to own piece
    if target != '.' and (piece.isupper() == target.isupper()):
        return False
    
    # Basic movement (not full rules, e.g., no check for path blocking)
    dr = end[0] - start[0]
    dc = end[1] - start[1]
    
    if piece.lower() == 'p':  # Pawn
        direction = -1 if piece.isupper() else 1
        if dc == 0 and target == '.' and abs(dr) == 1 and dr == direction:
            return True
        if dc == 0 and target == '.' and abs(dr) == 2 and dr == 2 * direction and start[0] == (6 if piece.isupper() else 1):
            return True
        if abs(dc) == 1 and abs(dr) == 1 and target != '.' and (piece.isupper() != target.isupper()):
            return True
    elif piece.lower() == 'r':  # Rook
        if (dr == 0 or dc == 0) and abs(dr + dc) > 0:
            return True
    elif piece.lower() == 'n':  # Knight
        if (abs(dr) == 2 and abs(dc) == 1) or (abs(dr) == 1 and abs(dc) == 2):
            return True
    elif piece.lower() == 'b':  # Bishop
        if abs(dr) == abs(dc) and abs(dr) > 0:
            return True
    elif piece.lower() == 'q':  # Queen
        if (abs(dr) == abs(dc) or dr == 0 or dc == 0) and abs(dr + dc) > 0:
            return True
    elif piece.lower() == 'k':  # King
        if abs(dr) <= 1 and abs(dc) <= 1 and (dr != 0 or dc != 0):
            return True
    
    return False

def game_loop():
    global selected_square, turn
    running = True
    while running:
        screen.fill(WHITE)
        draw_board()
        draw_pieces()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                if selected_square is None:
                    piece = board[row][col]
                    if piece != '.' and ((turn == 'white' and piece.isupper()) or (turn == 'black' and piece.islower())):
                        selected_square = (row, col)
                else:
                    if is_valid_move(selected_square, (row, col)):
                        # Move piece
                        board[row][col] = board[selected_square[0]][selected_square[1]]
                        board[selected_square[0]][selected_square[1]] = '.'
                        turn = 'black' if turn == 'white' else 'white'
                    selected_square = None
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

# Start the game
game_loop()
