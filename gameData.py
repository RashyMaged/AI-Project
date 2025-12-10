from typing import Tuple
from game_board import GameBoard

class Connect4Data:
    """
    Contains all the data needed for a Connect 4 game.
    """

    
    cell_size: int
    board_width: int
    board_height: int
    piece_radius: int
    screen_size: Tuple[int, int]

    
    is_game_over: bool
    current_turn: int
    last_rows: list[int]
    last_cols: list[int]
    board: GameBoard
    last_action: str

    def __init__(self):
        
        self.is_game_over = False
        self.current_turn = 0
        self.last_rows = []
        self.last_cols = []
        self.board = GameBoard()
        self.last_action = None


        self.cell_size = 100
        self.board_width = 7 * self.cell_size
        self.board_height = 7 * self.cell_size
        self.screen_size = (self.board_width, self.board_height)
        self.piece_radius = int(self.cell_size / 2 - 5)
