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


def board_positions(one=1, two=2, three=3, four=4, five=5, six=6, seven=7, eight=8, nine=9):
    """Displays the positions board"""

    return "|\t%s\t|\t%s\t|\t%s\t|\n|\t%s\t|\t%s\t|\t%s\t|\n|\t%s\t|\t%s\t|\t%s\t|\n" % (one, two, three, four, five, six, seven, eight, nine)


def print_instruction():
    return board_positions()


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
