from flask import Flask, jsonify, request
from slacker import Slacker

import util
import secret
import game
import os
app = Flask(__name__)
from werkzeug.serving import run_simple
slacker = Slacker(secret.SECRET_KEY)

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

    if text == "game":
        players = channel['players']

        if len(players) < 2:
            res = {
                "response_type": "ephemeral",
                "text": "To start a game type 'challenge @username'"
            }

        else:
            print "passing"

    if 'challenge' in text:
        user_id = request.form.get('user_id')
        user_name = str(request.form.get('user_name'))
        player2 = str(text[11:])
        players = channel['players']
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
            players.add(user_id)
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
          players.add(user_id)
          res = {
              "response_type": "in_channel",
              "text": "Challenge accepted",
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
                    "text": util.print_instruction(),
                    "pretext": "Please use the following cell numbers to make your move",
                    "mrkdwn_in": ["text"]
                }
            ]
        }

    return jsonify(res)

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app, use_reloader=True)
