import numpy as np
import random
import time
import re

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
BOUND = 2

TYPE_NUMBER = 19
# assign scores to different chess type
OTHER = 0
LIVE_ONE = 1  # 1
SLEEP_TWO_A = 2  # -11
SLEEP_TWO_B = 3  # 101
SLEEP_TWO_C = 4  # 1001
LIVE_TWO = 5  # 11
SLEEP_THREE_A = 6  # -111
SLEEP_THREE_B = 7  # -1011
SLEEP_THREE_C = 8  # -1101
LIVE_THREE_A = 9  # 111
LIVE_THREE_B = 10  # 1011
FLUSH_FOUR_A = 11  # -11110
FLUSH_FOUR_B = 12  # -10111
FLUSH_FOUR_C = 13  # -11011
FLUSH_FOUR_D = 14  # -11101
LIVE_FOUR_A = 15  # 1111
LIVE_FOUR_B = 16  # 10111
LIVE_FOUR_C = 17  # 11011
INTO_FIVE = 18  # 11111

CHESS_TYPE = {
    INTO_FIVE: [[re.compile(r'11111')], [re.compile(r'-----')]],
    LIVE_FOUR_A: [[re.compile(r'011110')], [re.compile(r'0----0')]],
    LIVE_FOUR_B: [[re.compile(r'10111'), re.compile(r'11101')],
                  [re.compile(r'-0---'), re.compile(r'---0-')]],
    LIVE_FOUR_C: [[re.compile(r'11011')], [re.compile(r'--0--')]],
    FLUSH_FOUR_A: [[re.compile(r'-11110'), re.compile(r'01111-')],
                   [re.compile(r'1----0'), re.compile(r'0----1')]],
    FLUSH_FOUR_B: [[re.compile(r'-10111'), re.compile(r'11101-')],
                   [re.compile(r'1-0---'), re.compile(r'---0-1')]],
    FLUSH_FOUR_C: [[re.compile(r'-11011'), re.compile(r'11011-')],
                   [re.compile(r'1--0--'), re.compile(r'--0--1')]],
    FLUSH_FOUR_D: [[re.compile(r'-11101'), re.compile(r'10111-')],
                   [re.compile(r'1---0-'), re.compile(r'-0---1')]],
    LIVE_THREE_A: [[re.compile(r'01110')], [re.compile(r'0---0')]],
    LIVE_THREE_B: [[re.compile(r'01011'), re.compile(r'11010'), re.compile(r'10110'), re.compile(r'01101')],
                   [re.compile(r'0-0--'), re.compile(r'--0-0'), re.compile(r'-0--0'), re.compile(r'0--0-')]],
    SLEEP_THREE_A: [[re.compile(r'-11100'), re.compile(r'00111-')],
                    [re.compile(r'1---00'), re.compile(r'00---1')]],
    SLEEP_THREE_B: [[re.compile(r'-10110'), re.compile(r'01101-')],
                    [re.compile(r'1-0--0'), re.compile(r'0--0-1')]],
    SLEEP_THREE_C: [[re.compile(r'-11010'), re.compile(r'01011-')],
                    [re.compile(r'1--0-0'), re.compile(r'0-0--1')]],
    LIVE_TWO:   [[re.compile(r'01100'), re.compile(r'00110')],
                 [re.compile(r'0--00'), re.compile(r'00--0')]],
    SLEEP_TWO_A: [[re.compile(r'-11000'), re.compile(r'00011-')],
                  [re.compile(r'1--000'), re.compile(r'000--1')]],
    SLEEP_TWO_B: [[re.compile(r'01010')], [re.compile(r'0-0-0')]],
    SLEEP_TWO_C: [[re.compile(r'010010')], [re.compile(r'0-00-0')]],
    LIVE_ONE: [[re.compile(r'00100'), re.compile(r'01000'), re.compile(r'00010')],
               [re.compile(r'00-00'), re.compile(r'0-000'), re.compile(r'000-0')]]
}

SCORE_TABLE = {
    INTO_FIVE: 1000000,
    LIVE_FOUR_A: 100000,
    LIVE_FOUR_B: 3250,
    LIVE_FOUR_C: 3150,
    FLUSH_FOUR_A: 2600,
    FLUSH_FOUR_B: 3000,
    FLUSH_FOUR_C: 2650,
    FLUSH_FOUR_D: 2501,
    LIVE_THREE_A: 3001,
    LIVE_THREE_B: 2750,
    SLEEP_THREE_A: 500,
    SLEEP_THREE_B: 800,
    SLEEP_THREE_C: 800,
    LIVE_TWO: 1000,
    SLEEP_TWO_A: 150,
    SLEEP_TWO_B: 550,
    SLEEP_TWO_C: 300,
    LIVE_ONE: 50,
    OTHER: 0
}

# to record if a point has been visited before in specific direction
# 0: horizon    1: vertical     2: left diagonal    3: right diagonal
DIRECTION = [(1, 0), (0, 1), (1, 1), (1, -1)]


# don't change the class name


class AI(object):
    # This dict is for storing different shapes of chessboard and corresponding score
    # chessboard_size, color, time_out passed from agent、、
    pos_score = None

    def __init__(self, chessboard_size, color, time_out):

        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []

    # The input is current chessboard.

    def go(self, chessboard):
        # print('AI color is : ', self.color)
        # Clear candidate_list
        # ==================================================================
        # initialize the hash table, zobrist algorithm used
        half = self.chessboard_size // 2
        self.pos_score = [[half-max(abs(x-half), abs(y-half)) for x in range(
            self.chessboard_size)] for y in range(self.chessboard_size)]
        new_pos = self.best_point(chessboard)
        print(new_pos, chessboard)
        # print(new_pos,chessboard,sep='\n')
        # print(chessboard)
        #print('new pos',new_pos)
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)

    def evaluate(self, chessboard):
        # to store the information of chess types of both ai and enemy
        chess_type = [[0 for i in range(TYPE_NUMBER)] for j in range(2)]

        visit_record = np.zeros(
            (self.chessboard_size, self.chessboard_size, 4), dtype=np.int)
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i, j] != COLOR_NONE and self.has_neighbor(chessboard, [i, j], dis=4):
                    color = chessboard[i, j]
                    self.evaluate_point(
                        chessboard, [i, j], color, chess_type, visit_record)
                    # some details here. To deal with all the conditions of important type

        return chess_type

    # one step prediction
    def best_point(self, chessboard):
        # to store the information of chess types of both ai and enemy
        chess_type = [[0 for i in range(TYPE_NUMBER)] for j in range(2)]
        best = -float('inf')
        new_pos = [-1, -1]
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i, j] == COLOR_NONE and self.has_neighbor(chessboard, [i, j]):
                    #print('testing ', [i,j],end = '\t')
                    chessboard[i, j] = self.color
                    self_score = self.evaluate_point(
                        chessboard, [i, j], self.color, chess_type)
                    #print('self score is ',self_score,end = '\t')
                    chessboard[i, j] = -self.color
                    enemy_score = self.evaluate_point(
                        chessboard, [i, j], -self.color, chess_type)
                    #print('enemy score is ',enemy_score,end = '\n')
                    chessboard[i, j] = COLOR_NONE
                    if self.color == COLOR_BLACK:
                        score = self_score + 0.8 * \
                            enemy_score + self.pos_score[i][j]
                    else:
                        score = self_score + 0.95 * \
                            enemy_score + self.pos_score[i][j]
                    #print([i,j], self_score, enemy_score, score)
                    if best < score:
                        new_pos = [i, j]
                        best = score
        # print('score',best)
        if best == -float('inf'):
            new_pos = [self.chessboard_size//2, self.chessboard_size//2]

        return new_pos
    '''
    def gen(self, chessboard, pos, color, chess_type, visit_record):
        moves = []
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i,j] == COLOR_NONE and self.has_neighbor(chessboard,[i,j]):
                    #print('testing ', [i,j],end = '\t')
                    chessboard[i,j] = self.color
                    self_score = self.evaluate_point(chessboard,[i,j],self.color,chess_type,visit_record)
                    #print('self score is ',self_score,end = '\t')
                    chessboard[i,j] = -self.color
                    enemy_score = self.evaluate_point(chessboard,[i,j],-self.color,chess_type,visit_record)
                    #print('enemy score is ',enemy_score,end = '\n')
                    chessboard[i,j] = COLOR_NONE
                    score = self_score + enemy_score + self.pos_score[i][j]
                    moves.append((score,[i,j]))
        moves.sort(key = lambda one_tuple: one_tuple[0], reverse = True)
        return moves
    '''

    def evaluate_point(self, chessboard, pos, color, chess_type):
        total_score = 0
        lines = self.get_lines(chessboard, pos, color)
        #print(pos,lines[0],sep = '\t')
        for index in range(4):
            total_score += self.eval_line(
                lines[index], pos, color, index)

        return total_score

    def eval_line(self, line, pos, color, index):
        s_color = None
        if color == COLOR_WHITE:
            s_color = 0
        elif color == COLOR_BLACK:
            s_color = 1
        else:
            return OTHER
        score = SCORE_TABLE[OTHER]
        for one_type in CHESS_TYPE:
            one_list = CHESS_TYPE[one_type][s_color]
            for one_item in one_list:
                search = one_item.search(line)
                if search != None:  # found a matched type
                    (l, r) = search.span()
                    for offset in range(l, r):  # record "visited"
                        (x, y) = (pos[0]+(offset-4)*DIRECTION[index]
                                  [0], pos[1]+(offset-4)*DIRECTION[index][1])
                    #print('the type is ', one_type, pos, index,sep = '\t')
                    score = max(score, SCORE_TABLE[one_type])
                else:   # if not, check another
                    continue
        return score

    def get_lines(self, chessboard, pos, color):
        line_str = ['' for i in range(4)]
        index = 0
        x, y = pos

        while(index < len(DIRECTION)):
            for offset in range(-4, 5):
                off_x, off_y = (
                    x+offset*DIRECTION[index][0], y+offset*DIRECTION[index][1])
                if off_x not in range(self.chessboard_size) or off_y not in range(self.chessboard_size):
                    line_str[index] += str(BOUND)   # '2' represents BOUND
                elif (off_x, off_y) == pos:
                    if color == COLOR_BLACK:
                        # '-' represents COLOR_BLACK
                        line_str[index] += '-'
                    else:
                        # '1' represents COLOR_WHITE and '0' represents COLOR_NONE
                        line_str[index] += str(color)
                else:
                    c_color = chessboard[off_x, off_y]
                    if c_color == COLOR_BLACK:
                        line_str[index] += '-'
                    else:
                        line_str[index] += str(c_color)
            index += 1
        return line_str

    def has_neighbor(self, chessboard, pos, dis=1):
        if chessboard[pos[0], pos[1]] != COLOR_NONE:
            return False
        for offset_x in range(-dis, dis+1):
            for offset_y in range(-dis, dis+1):
                if (offset_x, offset_y) == (0, 0) or \
                        pos[0] + offset_x not in range(0, self.chessboard_size) or \
                        pos[1] + offset_y not in range(0, self.chessboard_size):
                    continue
                if chessboard[pos[0]+offset_x, pos[1]+offset_y] != COLOR_NONE:
                    return True
        return False
