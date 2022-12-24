"""
randint - for toss coin,
sleep - for simulate flipping,
pprint - for print score,
wraps - for wrapper.
"""
from random import randint
from time import sleep
from pprint import pprint
from functools import wraps


def board_printer(board):
    """
    FUNC: print the playing field on the screen
    :param board: numbers on board
    :return: NONE
    """
    print("-------------")
    for i in range(0, 7, 3):
        print(f"| {board[1 + i]} | {board[2 + i]} | {board[3 + i]} |")
        print("-------------")


def toss_coin(func):
    """
       FUNC: flips a coin and returns the nicknames in the order of the moves
       INPUT: -
       OUTPUT: tuple with players nicknames, right order
        """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # player choice side of coin
        nicknames = func(*args, **kwargs)
        f_flip = input(f'{nicknames[0]}, choice \'head\' or \'tail\': ').lower()
        while f_flip not in 'headtail':
            print('input tail or head, register not important')
            f_flip = input(f'{nicknames[0]}, choice \'head\' or \'tail\': ').lower()

        # coin toss
        coin = randint(1, 100)
        print('Flipping', end='')
        for _ in range(1, randint(3, 5)):
            print('.', end='')
            sleep(1)

        # choice a winner
        if coin % 2:
            print('HEAD', (f'{nicknames[0]} win' if f_flip == 'head' else f'{nicknames[1]} win'))
            nicknames = nicknames if f_flip == 'head' else nicknames[::-1]
        else:
            print('TAIl', (f'{nicknames[0]} win' if f_flip == 'tail' else f'{nicknames[1]} win'))
            nicknames = nicknames if f_flip == 'tail' else nicknames[::-1]

        return nicknames

    return wrapper


@toss_coin
def get_names():
    """
    FUNC: Takes players names
    INPUT: NONE
    OUTPUT: tuple with players nicknames
    """
    f_name, s_name = input('First player name: '), input('Second player name: ')
    return f_name, s_name


def choice_marker(nicknames):
    """
    FUNC: the first player chooses a marker
    INPUT: tuple with players nicknames
    OUTPUT: tuple with players markers, in right order
    """
    f_marker = input(f'{nicknames[0]}, choice \'X\' or \'O\': ').upper()
    while f_marker not in 'XO':
        print('input X or O, register not important')
        f_marker = input(f'{nicknames[0]}, choice \'X\' or \'O\': ').upper()
    return ('X', 'O') if f_marker == 'X' else ('O', 'X')


def filling_board(board, move, field, markers):
    """
    FUNC: places a marker on the playing field
    INPUT: game board, counter moves, field input, players markers
    OUTPUT: board
    """
    if not move % 2:
        board[field] = markers[0]
    else:
        board[field] = markers[1]

    return board


def check_move(board, field):
    """
    FUNC: checks the correctness of the move
    :param board:
    :param field: place on board, what player choice
    :return: True - move is correct, False - not correct
    """
    return True if field in range(1, 10) and board[field].isdigit() else False


def check_result(board):
    """
    FUNC:
    :param board:
    :return: True - have result, end game. False - continue game
    """
    # checking strings
    for i in range(1, 10, 3):
        if board[i] == board[i + 1] == board[i + 2]:
            return True

    # checking columns
    for i in range(1, 4):
        if board[i] == board[i + 3] == board[i + 6]:
            return True

    # checking diagonals
    if board[1] == board[5] == board[9] or board[3] == board[5] == board[7]:
        return True

    return False


print('----------GAME IS START----------')
REWRITE_FL = False
RESULT_FL = False
names = get_names()
pl_markers = choice_marker(names)
score = {f'{names[0]}': 0, f'{names[1]}': 0}

while True:
    numbers_on_board = [''] + [str(num) for num in range(1, 10)]
    counter, pl_input = 0, 0
    print('\n' * 100)
    board_printer(numbers_on_board)

    # if players want to change names
    if REWRITE_FL:
        names = get_names()
        pl_markers = choice_marker(names)
        score = {f'{names[0]}': 0, f'{names[1]}': 0}

    while not RESULT_FL and counter < 9:

        while not check_move(numbers_on_board, pl_input):
            pl_input = int(input(f'{names[counter % 2]}, choice field 1-9: '))

        filling_board(numbers_on_board, counter, pl_input, pl_markers)
        counter += 1
        print('\n' * 100)
        board_printer(numbers_on_board)
        RESULT_FL = check_result(numbers_on_board)

    # print result game, and score
    print(f'{names[(counter - 1) % 2]} win' if RESULT_FL else 'Draw')
    if RESULT_FL:
        score[f'{names[(counter - 1) % 2]}'] += 1
    pprint(score)

    # ask for next round or end game
    rerun = input('One more round? ').lower()
    if rerun == 'yes':
        names = names[::-1]
        RESULT_FL = False
        REWRITE_FL = True if input('Rewrite names? ').lower() == 'yes' else False
    else:
        print('----------GAME IS OVER----------')
        break
