import math
from typing import Tuple, List, Optional

from game_board import GameBoard 
from game_data import GameData
from config import red, yellow 
 

PLAYER_PIECE = 1
AI_PIECE = 2



def get_valid_locations(board: GameBoard) -> List[int]:
    """
   ترجع الاعمده اللى ينفع اجط فيها coin
    """
    valid_locations: List[int] = []
    for col in range(board.cols):
        if board.is_valid_location(col):
            valid_locations.append(col)
    return valid_locations

def drop_piece_on_copy(board: GameBoard, row: int, col: int, piece: int) -> GameBoard:
    """
   يحط القطعه ويعمل copy بعدين يرجع شكل ال board الجديده
    """
    # استخدام .copy() لضمان عدم تغيير اللوحة الأصلية أثناء اللعبة
    temp_board = GameBoard(board.rows, board.cols)
    temp_board.board = board.board.copy()
    temp_board.drop_piece(row, col, piece)
    return temp_board

# --- وظيفة تقييم اللوحة (Scoring) ---
def evaluate_window(window: List[int], piece: int) -> int:
    """
    تقيّم نافذة (مجموعة من 4 خانات متتالية) وتُرجع درجة التقييم.
    """
    score = 0
    # تحديد قطعة الخصم
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    # 4 قطع متتالية للذكاء الاصطناعي هي فوز فوري
    if window.count(piece) == 4:
        score += 100000 
    # 3 قطع للذكاء الاصطناعي مع خانة فارغة (فرصة للفوز)
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5 
    # 2 قطعة للذكاء الاصطناعي مع خانتين فارغتين
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # منع الخصم من الفوز (3 قطع متتالية للخصم مع خانة فارغة)
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4 # قيمة أقل من فرصة الفوز، لكنها مهمة للمنع

    return score

def score_position(board: GameBoard, piece: int) -> int:
    """
    تحسب درجة التقييم الإجمالية للوحة الحالية.
    """
    score = 0
    R = board.rows
    C = board.cols

    # ال center هو افضل مكان (يسهل تحقيق 4 متتالية)
    center_array = list(board.board[:, C // 2]) 
    center_count = center_array.count(piece)  #عدد ال coins اللى حطها ال ai
    score += center_count * 3 

    #الافقى
    for r in range(R):
        row_array = list(board.board[r, :])
        for c in range(C - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    #العمودى
    for c in range(C):
        col_array = list(board.board[:, c])
        for r in range(R - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    #الأقطار + 
    for r in range(R - 3):
        for c in range(C - 3):
            window = [board.board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    #  الأقطار السالبة (/)
    for r in range(R - 3):
        for c in range(C - 3, C):
            window = [board.board[r + i][c - i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# --- خوارزمية Minimax ---

def minimax(board: GameBoard, depth: int, alpha: float, beta: float, maximizing_player: bool) -> Tuple[Optional[int], int]:
    """
    خوارزمية Minimax مع تقليم ألفا-بيتا (Alpha-Beta Pruning).
    
    :param board: لوحة اللعبة الحالية.
    :param depth: العمق المتبقي للبحث.
    :param alpha: أفضل قيمة وجدها اللاعب المُعظِّم (Maximizer) حتى الآن.
    :param beta: أفضل قيمة وجدها اللاعب المُقلِّل (Minimizer) حتى الآن.
    :param maximizing_player: هل الدور الحالي للاعب المُعظِّم (AI)؟
    :return: زوج (أفضل عمود, أفضل درجة تقييم).
    """
    
    valid_locations = get_valid_locations(board)
    is_terminal = board.winning_move(PLAYER_PIECE) or board.winning_move(AI_PIECE) or board.tie_move()

    # حالات الإنهاء (Terminal Cases):
    if depth == 0 or is_terminal:
        if is_terminal:
            if board.winning_move(AI_PIECE):
                # فوز الذكاء الاصطناعي (قيمة عالية جداً)
                return (None, 100000000000000)
            elif board.winning_move(PLAYER_PIECE):
                # فوز اللاعب (قيمة منخفضة جداً)
                return (None, -100000000000000)
            else: # تعادل (Tie Move)
                return (None, 0)
        else: # وصل إلى أقصى عمق بحث
            return (None, score_position(board, AI_PIECE))

    # --- دور اللاعب المُعظِّم (AI) ---
    if maximizing_player:
        value = -math.inf
        column = valid_locations[0] # تعيين عمود مبدئي
        
        for col in valid_locations:
            row = board.get_next_open_row(col)
            #   يحط القطعه ويعمل copy بعدين يرجع شكل ال board الجديده

            new_board = drop_piece_on_copy(board, row, col, AI_PIECE)
            
            # استدعاء Minimax للمستوى التالي (دور اللاعب المُقلِّل)
            new_score = minimax(new_board, depth - 1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
            
            alpha = max(alpha, value)
            if alpha >= beta:
                break # تقليم ألفا-بيتا (Alpha-Beta Pruning)

        return (column, value)

    # --- دور اللاعب المُقلِّل (Player) ---
    else: # minimizing_player
        value = math.inf
        column = valid_locations[0] # تعيين عمود مبدئي
        
        for col in valid_locations:
            row = board.get_next_open_row(col)
            # إنشاء لوحة جديدة مع حركة محاكاة
            new_board = drop_piece_on_copy(board, row, col, PLAYER_PIECE)
            
            # استدعاء Minimax للمستوى التالي (دور اللاعب المُعظِّم)
            new_score = minimax(new_board, depth - 1, alpha, beta, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
            
            beta = min(beta, value)
            if alpha >= beta:
                break # تقليم ألفا-بيتا (Alpha-Beta Pruning)
                
        return (column, value)
        
def find_best_move(game_data: GameData, depth: int) -> int:
    """
    تجد أفضل عمود للعب الذكاء الاصطناعي باستخدام خوارزمية Minimax.
    
     :param game_data: بيانات اللعبة الحالية.
    :param depth: العمق.
    :return: أفضل عمود لاختيار الحركة.
    """
    # Minimax يبدأ دائماً كـ maximizing_player
    best_col, _ = minimax(game_data.game_board, depth, -math.inf, math.inf, True)
    return best_col