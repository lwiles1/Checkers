import pygame
import sys  # Added for clean exiting

# Game Settings
WIDTH = 600
HEIGHT = 600
ROWS = COLS = 8
SQUARE_SIZE = WIDTH // COLS

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False  # Initially not a king
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = self.col * SQUARE_SIZE
        self.y = self.row * SQUARE_SIZE

    def draw(self, screen):
        radius = SQUARE_SIZE // 2 - SQUARE_SIZE // 10  # For a slightly smaller circle
        pygame.draw.circle(screen, self.color, (self.x + SQUARE_SIZE // 2, self.y + SQUARE_SIZE // 2), radius)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position()
    
    def get_valid_moves(self, board):
        """Returns a list of valid moves for the piece."""
        moves = {}
        left = self.col - 1
        right = self.col + 1
        row = self.row

        # Determine direction based on piece color
        direction = -1 if self.color == WHITE else 1 
        
        # Simple moves
        if board[row + direction][left] == 0 and 0 <= row + direction < ROWS:
            moves[(row + direction, left)] = []
        if board[row + direction][right] == 0 and 0 <= row + direction < ROWS:
            moves[(row + direction, right)] = []

        # Jump moves
        # ... (We'll add jump move logic here shortly) ... 

        return moves

class Game:
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.red_left = self.white_left = 12  # Track remaining pieces
        self.create_board()
        self.turn = WHITE  # White starts first
        self.selected_piece = None

    def change_turn(self):
        self.turn = WHITE if self.turn == RED else RED 

    def get_clicked_piece(self, pos):
        """Given a screen position (pos), returns the Piece object at that location if there is one."""
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        if row < ROWS and col < COLS and self.board[row][col] != 0:
            return self.board[row][col] if self.board[row][col].color == self.turn else None
        return None

    def update_piece_position(self, piece, pos):
        """Updates the piece's position based on the mouse position (pos)."""
        piece.x = pos[0] - SQUARE_SIZE // 2  # Center piece to mouse
        piece.y = pos[1] - SQUARE_SIZE // 2

    def try_move_piece(self, piece):
        """Attempts to move the piece to its current (x, y) position. Will implement simple moves first."""
        row = int(round(piece.y / SQUARE_SIZE))  # Determine square of release
        col = int(round(piece.x / SQUARE_SIZE))

        # Get valid moves for the piece
        valid_moves = piece.get_valid_moves(self.board)

        if (row, col) in valid_moves:  # If it's a valid empty square
            # Check if the move is a jump
            if abs(row - piece.row) == 2 and abs(col - piece.col) == 2:
                # Check if there's an opponent's piece in the middle
                mid_row = (row + piece.row) // 2
                mid_col = (col + piece.col) // 2
                if self.board[mid_row][mid_col] is not None and self.board[mid_row][mid_col].color != piece.color:
                    # Remove the opponent's piece
                    self.board[mid_row][mid_col] = 0
                    # Move the piece to the new position
                    self.board[piece.row][piece.col] = 0
                    piece.move(row, col)
                    self.board[row][col] = piece
                    self.change_turn()
                else:
                    # If it's not a valid jump, don't move the piece
                    return
            else:
                # If it's not a jump, move the piece normally
                self.board[piece.row][piece.col] = 0
                piece.move(row, col)
                self.board[row][col] = piece
                self.change_turn()
    
    def create_board(self):
        # Place red pieces
        for row in range(3):
            for col in range((row + 1) % 2, COLS, 2):
                self.board[row][col] = Piece(row, col, RED)

        # Place white pieces
        for row in range(ROWS - 3, ROWS):
            for col in range((row + 1) % 2, COLS, 2):
                self.board[row][col] = Piece(row, col, WHITE)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")

    game = Game()  # Create a Game instance
    selected_piece = None

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selected_piece is None:  # No piece currently selected
                    selected_piece = game.get_clicked_piece(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION:
                if selected_piece:
                    game.update_piece_position(selected_piece, pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_piece:
                    game.try_move_piece(selected_piece)
                    selected_piece = None

        draw_board(screen, game)
        pygame.display.update()

def draw_board(screen, game):
        # Fill background
        screen.fill(WHITE)

        # Draw checkerboard pattern
        for row in range(ROWS):
            for col in range((row + 1) % 2, COLS, 2):
                pygame.draw.rect(screen, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw pieces
        for row in range(ROWS):
            for col in range(COLS):
                piece = game.board[row][col]
                if piece != 0:
                    piece.draw(screen) 

if __name__ == "__main__":
    main()
