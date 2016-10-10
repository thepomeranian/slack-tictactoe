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
    market(ongoing_game)

    return "\t| %s | %s | %s |\t\n-------------\n| %s | %s | %s |\t\n-------------\n| %s | %s | %s |" % (1, 2, 3, 4, 5, 6, 7, 8, 9)


def marker(ongoing_game):
    player1 = ongoing_game[1::2]
    player2 = ongoing_game[::2]

    if play in player1:
        return "x"

    if play in player2:
        return "o"


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
