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
        'game_ended': False,
        'ongoing_game': [' '] * 9
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
