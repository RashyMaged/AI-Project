import numpy as np

# 1. Create board
def create_board(rows=6, cols=7):
    board = np.zeros((rows, cols), dtype=int)
    return board

# 2. Print board
def print_board(board):
    print(np.flip(board, 0))  
# 3. Drop piece
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# 4. Is valid location
def is_valid_location(board, col):
    return board[-1][col] == 0  

# 5. Next open row
def get_next_open_row(board, col):
    for r in range(board.shape[0]):
        if board[r][col] == 0:
            return r
    return None

# 6. Check piece at position
def check_piece(board, row, col, piece):
    return board[row][col] == piece

# 7. Check horizontal
def check_horizontal(board, piece):
    rows, cols = board.shape
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r, c+i] == piece for i in range(4)):
                return True
    return False

# 8. Check vertical
def check_vertical(board, piece):
    rows, cols = board.shape
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i, c] == piece for i in range(4)):
                return True
    return False

# 9. Check diagonal
def check_diagonal(board, piece):
    rows, cols = board.shape
    for r in range(rows - 3):

        for c in range(cols - 3):
            if all(board[r+i, c+i] == piece for i in range(4)):
                return True

    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r+i, c-i] == piece for i in range(4)):
                return True
    return False

# 10. Check win
def winning_move(board, piece):
    return check_horizontal(board, piece) or check_vertical(board, piece) or check_diagonal(board, piece)

# 11. Check draw
def is_draw(board):
    return all(board[-1, c] != 0 for c in range(board.shape[1]))  

if __name__ == "__main__":
    board = create_board()
    game_over = False
    turn = 0

    while not game_over:
        print_board(board)
        col = int(input(f"Player {turn+1} choose column (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, turn+1)

            if winning_move(board, turn+1):
                print_board(board)
                print(f"Player {turn+1} wins!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("Game is a draw!")
                game_over = True

            turn = (turn + 1) % 2
        else:
            print("Column full! Choose another one.")
