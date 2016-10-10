from flask import Flask, jsonify, request

import util
import game
app = Flask(__name__)
from werkzeug.serving import run_simple


@app.route('/', methods=['POST'])
def main():
    text = request.form.get('text')
    channel_id = str(request.form.get('channel_id'))

    print util.game_finder(channel_id)
    # print util.channels.values()
    channel = util.channels[channel_id]
    print channel['players']

    if text == "game":
        players = channel['players']

        if len(players) < 2:
            print "this works"
            res = {
                "response_type": "ephemeral",
                "text": "To start a game type 'challenge @username'"
            }
        else:
            print "passing"

    if 'challenge' in text:
        user_id = request.form.get('user_id')
        user_name = str(request.form.get('user_name'))
        player2 = str(text[10:])
        if user_name in player2:
            res = {
                "response_type": "ephemeral",

                "attachments": [
                  {
                      "text": "You cannot challenge yourself",
                      "mrkdwn_in": "text"
                  }
                ]
            }
        else:
            channel['player1'] = user_name
            channel['player2'] = player2
            channel['players'] = user_id
            res = {
                "response_type": "ephemeral",

                "attachments": [
                    {
                        "text": "Challenging %s to a match" % player2,
                        "mrkdwn_in": "text"
                    }
                ]
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
    # else:
    #     res = {
    #         "response_type": "ephemeral",
    #         "text": "Sorry, I did not understand that. To see what I can do type 'help'"
    #     }

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
