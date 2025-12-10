import math
import os
import sys

import pygame

from config import black
from events import GameOver, MouseClickEvent, PieceDropEvent, bus
from game_data import GameData
from game_renderer import GameRenderer
from minimax_ai import find_best_move, AI_PIECE


class ConnectGame:
    """
    Holds all of the game logic and game data.
    """

    game_data: GameData
    renderer: GameRenderer

    def __init__(self, game_data: GameData, renderer: GameRenderer):
        """
        Initializes the connect game.
        :param game_data: A reference to the game data object.
        :param renderer: A reference to the game renderer.
        """
        self.game_data = game_data
        self.renderer = renderer

    def quit(self):
        """
        Exits the game.
        """
        sys.exit()

    @bus.on("mouse:click")
    def mouse_click(self, event: MouseClickEvent):
        """
        Handles a mouse click event.
        :param event: Data about the mouse click
        """
        if self.game_data.turn != 0:
            return
        pygame.draw.rect(
            self.renderer.screen,
            black,
            (0, 0, self.game_data.width, self.game_data.sq_size),
        )

        col: int = int(math.floor(event.posx / self.game_data.sq_size))

        if self.game_data.game_board.is_valid_location(col):
            row: int = self.game_data.game_board.get_next_open_row(col)

            self.game_data.last_move_row.append(row)
            self.game_data.last_move_col.append(col)
            self.game_data.game_board.drop_piece(row, col, self.game_data.turn + 1)

            self.draw()

            bus.emit(
                "piece:drop", PieceDropEvent(self.game_data.game_board.board[row][col])
            )

            self.print_board()

            if self.game_data.game_board.winning_move(self.game_data.turn + 1):
                bus.emit(
                    "game:over", self.renderer, GameOver(False, self.game_data.turn + 1)
                )
                self.game_data.game_over = True

            pygame.display.update()

            self.game_data.turn += 1
            self.game_data.turn = self.game_data.turn % 2

    @bus.on("game:undo")
    def undo(self):
        """
        Handles the Ctrl+Z keyboard sequence, which
        is used to roll back the last move.
        :return:
        """
        if self.game_data.last_move_row:
            self.game_data.game_board.drop_piece(
                self.game_data.last_move_row.pop(),
                self.game_data.last_move_col.pop(),
                0,
            )

        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2

    def update(self):
        """
        Checks the game state, dispatching events as needed.
        """
        if self.game_data.turn == 1 and not self.game_data.game_over:
            # يمكن تعديل العمق (4 هنا) للتحكم في صعوبة اللعبة
            # عمق أكبر = أصعب وأبطأ
            col = find_best_move(self.game_data, depth=4) 
            
            if self.game_data.game_board.is_valid_location(col):
                row: int = self.game_data.game_board.get_next_open_row(col)

                self.game_data.last_move_row.append(row)
                self.game_data.last_move_col.append(col)
                # استخدام AI_PIECE بدلاً من self.game_data.turn + 1 لضمان القيمة 2
                self.game_data.game_board.drop_piece(row, col, AI_PIECE) 

                self.draw()

                bus.emit(
                    "piece:drop", PieceDropEvent(self.game_data.game_board.board[row][col])
                )

                self.print_board()

                if self.game_data.game_board.winning_move(AI_PIECE):
                    bus.emit(
                        "game:over", self.renderer, GameOver(False, AI_PIECE)
                    )
                    self.game_data.game_over = True

                pygame.display.update()

                # بعد انتهاء دور الذكاء الاصطناعي
                self.game_data.turn += 1
                self.game_data.turn = self.game_data.turn % 2 
        # ----------------------------------------------------------------------------------
        if self.game_data.game_board.tie_move():
            bus.emit("game:over", self.renderer, GameOver(was_tie=True))

            self.game_data.game_over = True

        if self.game_data.game_over:
            print(os.getpid())
            pygame.time.wait(1000)
            os.system("game.py")

    def draw(self):
        """
        Directs the game renderer to 'render' the game state to the audio and video devices.
        """
        self.renderer.draw(self.game_data)

    def print_board(self):
        """
        Prints the state of the board to the console.
        """
        self.game_data.game_board.print_board()
