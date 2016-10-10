channels = {}


def new_channel(channel_id):
    """Logging a new channel"""

    channels[channel_id] = {
        'player1': "",
        'player2': "",
        'players': set(),
        'accepted_invite': False,
        'turn': "",
        'winner': "",
        'ongoing_game': []
    }


def create_memberlist(r):
    existing_users = []
    for i in r:
        for key, value in i.iteritems():
            if key == "name":
                existing_users.append(str(value))
    return existing_users


def game_finder(channel_id):
    """Logs all channels that have instantiated bot and opens ongoing game"""
    if channel_id not in channels.keys():
        new_channel(channel_id)
    else:
        ongoing_game = channels[channel_id]

    return channels[channel_id]


def print_instruction():
    return "\t| %s | %s | %s |\t\n-------------\n| %s | %s | %s |\t\n-------------\n| %s | %s | %s |" % (1, 2, 3, 4, 5, 6, 7, 8, 9)


def current_board(ongoing_game):
    ongoing_game = [' '] * 9 
    instructions = [1,2,3,4,5,6,7,8,9]
    possible_moves = 9

    board = "\t| %s | %s | %s |\t\n-------------\n| %s | %s | %s |\t\n-------------\n| %s | %s | %s |" % instructions
    return board


def check_win(board=None):
    winning_combos = (
        [6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    )
    board = [' '] * 9
    form = "\t| %s | %s | %s |\t\n-------------\n| %s | %s | %s |\t\n-------------\n| %s | %s | %s |"
    if board is None:
        return form % tuple(board[6:9] + board[3:6] + board[0:3])
    else:
            # when the game starts, display numbers on all the grids
        return form % tuple(board[6:9] + board[3:6] + board[0:3])


def who_move():
    """Returns True if it is the user's turn"""
    pass


def end():
    """Ends the game without a winner"""
    pass


def game_history():
    """Displays move history for a user"""
    pass


def user_history():
    """Displays users win/loss ratio"""
    pass
