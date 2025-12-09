import math 
import os
import sys

import pygame

from config import black
from events import GameOver, MouseClickEvent, PieceDropEvent, bus
from game_data import GameData
from game_renderer import GameRenderer


class ConnectGame:
    """
    Holds all of the game logic and game data.
    """

    game_data: GameData
    renderer: GameRenderer
    "بيشاورو على الكلاسات اللى عملنالها import "

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
        pygame.draw.rect(
            self.renderer.screen,
            black,
            (0, 0, self.game_data.width, self.game_data.sq_size),
        )

        col: int = int(math.floor(event.posx / self.game_data.sq_size))
        "يحسب رقم العمود اللي تم النقر عليه، عن طريق تقسيم إحداثي X للنقر على حجم المربع (square size). "


        if self.game_data.game_board.is_valid_location(col):
            row: int = self.game_data.game_board.get_next_open_row(col)
            "بيحدد هيحط القطعه فى انهى صف فى العمود"
            self.game_data.last_move_row.append(row)
            self.game_data.last_move_col.append(col)
            "بيسجل اخر حركة حصلت (للصف والعمود )"

            self.game_data.game_board.drop_piece(row, col, self.game_data.turn + 1)
            "بينزل الكوين فى المكان المناسب ، turn +1 يعنى الدور الحالى" 
            
            
            
            self.draw()

            bus.emit(
                "piece:drop", PieceDropEvent(self.game_data.game_board.board[row][col])
            )
            "بيعمل ال piece drop"
            self.print_board()
            "بيطبع حالة اللوحة "
            if self.game_data.game_board.winning_move(self.game_data.turn + 1):
                bus.emit(
                    "game:over", self.renderer, GameOver(False, self.game_data.turn + 1)
                )
                self.game_data.game_over = True
            "بيتأكد لو الحركة دى ادت الى الفوز"

            pygame.display.update()
            "بيحدث الشاشه"

            self.game_data.turn += 1
            self.game_data.turn = self.game_data.turn % 2
            "يغير الدور الى اللاعب التانى"

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
            "بيشيل الحركة السابقه من اللوحة"

        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2
        "ويخلى اللاعب يلعب تانى"

    def update(self):
        """
        Checks the game state, dispatching events as needed.
        """
        if self.game_data.game_board.tie_move():
            bus.emit("game:over", self.renderer, GameOver(was_tie=True))

            self.game_data.game_over = True
            "بيتحقق لو اللعبة انتهت بالتعادل يعنى كل الاماكن مليانه ، ويطلع game over ويغير حالة اللعبه"

        if self.game_data.game_over:
            print(os.getpid())
            pygame.time.wait(1000)
            os.system("game.py")
            "سواء اللعبة انتهت بالتعادل او الفوز ينتظر ثوانى  ويشغل الملف من اول وجديد"

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
        