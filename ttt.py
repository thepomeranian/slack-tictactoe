from flask import Flask, jsonify, request
from slacker import Slacker

import util
import secret
import game
import os

app = Flask(__name__)
from werkzeug.serving import run_simple
slacker = Slacker(secret.SECRET_KEY)
game = game.Game()

response = slacker.users.list()
r = response.body['members']
existing_users = util.create_memberlist(r)


@app.route('/', methods=['POST'])
def main():
    text = request.form.get('text')
    channel_id = str(request.form.get('channel_id'))

    util.game_finder(channel_id)
    channel = util.channels[channel_id]
    commands = ['game', 'challenge', 'end',
                'accept', 'help', 'instructions', 'move']

    if text in commands:

        if text == 'game':
            players = channel['players']

            if channel['ongoing_game']:
                if not channel['accepted_invite']:
                    res = {
                        "response_type": "ephemeral",
                        "text": "Waiting for %s to accept a game. To cancel invite type 'end'" % channel['player2']
                    }
                if channel['accepted_invite']:
                    res = {
                        "response_type": "in_channel",
                        "text": "Here is the current gameboard:\n For instructions type '/ttt instructions'\n" + game.print_board()
                    }

            if channel['ongoing_game'] is False:
                res = {
                    "response_type": "ephemeral",
                    "text": "To start a game type 'challenge @username'"
                }

        if 'move' in text:
            players = channel['players']
            user_id = request.form.get('user_id')
            cell = str(text[5:])

            if channel['accepted_invite']:
                if user_id in players:
                    if turn:
                        if cell in possible_moves:
                            game.make_move(cell)
                            next_player = game.next_player()
                            res = {
                                "response_type": "in_channel",
                                "text": "You selected cell" + cell + "\nIt is now" + next_player + "'s turn.\n" + "Here is the current gameboard:\n" + game.print_board()
                            }
                        if cell not in possible_moves:
                            res = {
                                "response_type": "ephemeral",
                                "text": "Sorry, that is not a legitimate move."
                            }

            if channel['game_ended'] == True and len(players) < 2:
                res = {
                    "response_type": "ephemeral",
                    "text": "To start a new game type 'challenge @username'"
                }

            if channel['accepted_invite'] == False:
                res = {
                    "response_type": "ephemeral",
                    "text": "Waiting for %s to accept a game. To cancel invite type 'end'" % channel['player2']
                }

            res = {
                "response_type": "in_channel",
                "pretext": "For instrutions type 'instructions'",
                "text": "Here is the current gameboard:\n" + game.print_board()
            }

        if 'challenge' in text:
            user_id = request.form.get('user_id')
            user_name = str(request.form.get('user_name'))
            player2 = str(text[11:])
            if channel['ongoing_game']:
                res = {
                    "response_type": "ephemeral",
                    "text": "There is already an ongoing game in this channel.",
                }
            if channel['ongoing_game'] is False:

                if player2 not in existing_users:
                    res = {
                        "response_type": "ephemeral",
                        "text": "That user is not in this channel",
                    }

                if user_name in player2:
                    res = {
                        "response_type": "ephemeral",
                        "text": "You cannot challenge yourself",
                    }

                if user_name and player2 in existing_users:
                    channel['player1'] = user_name
                    channel['player2'] = player2
                    players = channel['players']
                    players |= {user_id}
                    channel['ongoing_game'] = True
                    res = {
                        "response_type": "in_channel",
                        "text": "Challenging %s to a match, to accept this match type 'accept'" % player2,
                    }

        if text == 'end':

            if channel['ongoing_game']:
                player2 = channel['player2']
                player1 = channel['player1']
                channel['ongoing_game'] = False
                res = {
                    "response_type": "in_channel",
                    "text": "Game between %s and %s has been ended." % (player1, player2)
                }

        if text == 'accept':
            user_id = request.form.get('user_id')
            user_name = str(request.form.get('user_name'))
            players = channel['players']
            player2 = channel['player2']
            player1 = channel['player1']

            if channel['ongoing_game'] is False:
                res = {
                    "response_type": "ephemeral",
                    "text": "To start a game type '/ttt challenge @username'"
                }
            if channel['ongoing_game']:
                if user_name == player2:
                    players |= {user_id}
                    channel['ongoing_game'] = True
                    channel['accepted_invite'] = True
                    res = {
                        "response_type": "in_channel",
                        "attachments": [
                            {
                                "text": "Please use the following cell number to make your move.\n/ttt move # - to make a move\n/ttt end - to end the game\n" + game.instructions() + "\nHere is the current game board:\n" + game.print_board(),
                                "pretext": "Challenge accepted. Please read the instructions below:",
                                "mrkdwn_in": ["text", "pretext"]
                            }
                        ]
                    }

                if user_name != player2:
                    res = {
                        "response_type": "ephemeral",
                        "text": "You were not the challenged player.",
                    }

        if text == 'help':
            res = {
                "response_type": "ephemeral",

                "attachments": [
                    {
                        "text": "/ttt game - print the current game\n/ttt challenge @username - to challenge another player in the same channel\n/ttt end - ends the current game\n/ttt accept - accept a challenge",
                        "pretext": "Here are all of the actions that I can do.",
                        "mrkdwn_in": ["text", "pretext"]
                    }
                ]
            }

        if text == 'instructions':
            res = {
                "response_type": "ephemeral",

                "attachments": [
                    {
                        "text": game.instructions(),
                        "pretext": "Please use the following cell numbers to make your move.\n/ttt move # - to make a move\n/ttt end - to end the game",
                        "mrkdwn_in": ["text", "pretext"]
                    }
                ]
            }

    else:
        res = {
            "response_type": "ephemeral",
            "text": "Sorry, I did not understand that.\nTo see what I can do type '/ttt helphelp'"
        }

    return jsonify(res)

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app, use_reloader=True)
