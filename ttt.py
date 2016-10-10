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

    print util.game_finder(channel_id)
    channel = util.channels[channel_id]
    print channel['players']
    possible_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    if text == "game":
        players = channel['players']

        if len(players) < 2:
          res = {
            "response_type": "ephemeral",
            "text": "To start a game type 'challenge @username'"
          }

        if len(players) < 2 and channel['accepted_invite'] == False:
            res = {
                "response_type": "ephemeral",
                "text": "Waiting for %s to accept a game. To cancel invite type 'end'" % channel['player2']
            }

        else:
            ongoing_game = channel['ongoing_game']
            res = {
                "response_type": "in_channel",
                "text": "Here is the current gameboard:\n For instructions type 'instructions'\n" + game.print_board()
            }

    if 'move' in text:
        players = channel['players']

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

            res = {
                "response_type": "in_channel",
                "text": "Challenging %s to a match, to accept this match type 'accept'" % player2,
            }

        else:
            res = {
                "response_type": "ephemeral",
                "text": "Sorry, I did not understand that. To see what I can do type 'help'"
            }

    if text == "accept":
        user_id = request.form.get('user_id')
        user_name = str(request.form.get('user_name'))
        players = channel['players']
        player2 = channel['player2']

        if user_name == player2:
            players |= {user_id}
            res = {
                "response_type": "in_channel",
                "attachments": [
                    {
                        "text": "Please use the following cell number to make your move. \n To make a move type 'move #'\n" + game.instructions() + "\nHere is the current game board:\n" + game.print_board(),
                        "pretext": "Challenge accepted. Please read the instructions below:",
                        "mrkdwn_in": ["text", "pretext"]
                    }
                ]
            }

        else:
            res = {
                "response_type": "ephemeral",
                "text": "You were not the challenge player.",
            }

    if text == "help":
        res = {
            "response_type": "ephemeral",

            "attachments": [
                {
                    "text": "Help",
                    "pretext": "Here are all of the actions that I can do.",
                    "mrkdwn_in": ["text", "pretext"]
                }
            ]
        }

    if text == "instructions":
        res = {
            "response_type": "ephemeral",

            "attachments": [
                {
                    "text": game.instructions(),
                    "pretext": "Please use the following cell numbers to make your move. To make a move type 'move #'",
                    "mrkdwn_in": ["text", "pretext"]
                }
            ]
        }

    return jsonify(res)


if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app, use_reloader=True)
