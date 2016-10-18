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


@app.route('/', methods=['POST'])
def main():
    text = request.form.get('text')
    channel_id = str(request.form.get('channel_id'))

    util.game_finder(channel_id)
    channel = util.channels[channel_id]
    res = {
        "response_type": "ephemeral",
        "text": "Sorry, I did not understand that.\nTo see what I can do type '/ttt help'"
    }

    if text == 'game':
        players = channel['players']
        res = game_status(players, channel)

    if 'challenge' in text:
        # have it repopulate existing users
        user_id = request.form.get('user_id')
        user_name = str(request.form.get('user_name'))
        player2 = str(text[11:])
        res = challenge(user_id, user_name, player2, channel)

    if text == 'accept':
        user_id = request.form.get('user_id')
        user_name = str(request.form.get('user_name'))
        res = accept(user_id, user_name, channel)

    if text == 'help':
        res = help()

    if text == 'instructions':
        res = instructions()

    if text == 'end':
        res = end(channel)

    if 'move' in text:
        players = channel['players']
        user_id = request.form.get('user_id')
        if channel['ongoing_game'] is True:
            if channel['accepted_invite'] is True:
                if len(text) < 5:
                    res = {
                        "response_type": "ephemeral",
                        "text": "Sorry, please enter a legitimate move."
                    }
                else:
                    cell = int(text[5:])
                user_name = str(request.form.get('user_name'))
                turn = channel['turn']
                possible_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                player2 = channel['player2']
                player1 = channel['player1']
                res = move(user_id, players, user_name, turn,
                           possible_moves, player1, player2, channel, cell)

        else:
            res = {
                "response_type": "ephemeral",
                "text": "Sorry, please enter a legitimate move."
            }

    return jsonify(res)


def game_status(players, channel):
    """Returns the current game status, game board, and whose turn it is if there is an ongoing game."""
    if channel['ongoing_game'] is True:
        if not channel['accepted_invite']:
            res = {
                "response_type": "ephemeral",
                "text": "Waiting for %s to accept a game. To cancel invite type '/ttt end'" % channel['player2']
            }
        if channel['accepted_invite'] is True:
            game_board = game.print_board(channel['board'])
            user_name = str(request.form.get('user_name'))
            turn = channel['turn']
            res = {
                "response_type": "in_channel",
                "text": "It is " + turn + "'s turn.\nHere is the current gameboard:\n For instructions type '/ttt instructions'\n" + "```" + game.print_board(channel['board']) + "```"
            }

    if channel['ongoing_game'] is False:
        res = {
            "response_type": "ephemeral",
            "text": "To start a game type '/ttt challenge @username'"
        }
    return res


def move(user_id, players, user_name, turn, possible_moves, player1, player2, channel, cell):
    """Returns a draw, winner, or prints the new board after a player makes a move"""
    if channel['accepted_invite'] is False:
        res = {
            "response_type": "ephemeral",
            "text": "To start a game type '/ttt challenge @username'"
        }
    if channel['accepted_invite'] is True:
        if user_id in players:
            if turn == user_name:
                if cell in possible_moves:
                    game_moves = channel['possible_moves']
                    if cell not in game_moves:
                        res = {
                            "response_type": "ephemeral",
                            "text": "Sorry, that is not a legitimate move."
                        }
                    if cell in game_moves:
                        game_board = game.make_move(
                            cell, turn, channel['board'])
                        channel['board'] = game_board
                        game_moves.remove(cell)

                        if len(game_moves) > 0 and game.is_winner(game_board, cell) is True:
                            channel['board'] = [' '] * 9
                            channel['ongoing_game'] = False
                            channel['accepted_invite'] = False
                            channel['possible_moves'] = [
                                0, 1, 2, 3, 4, 5, 6, 7, 8]
                            res = {
                                "response_type": "in_channel",
                                "text": turn + " has won the game!\n" + "```" + game.print_board(game_board) + "```"
                            }

                        if len(game_moves) > 0 and game.is_winner(game_board, cell) is False:
                            if turn == player1:
                                channel['turn'] = player2
                            else:
                                channel['turn'] = player1

                            res = {
                                "response_type": "in_channel",
                                "text": "You selected cell  " + str(cell) + "\nIt is now " + channel['turn'] + "'s turn.\n" + "Here is the current gameboard:\n" + "```" + game.print_board(game_board) + "```"
                            }

                        if len(game_moves) == 0:
                            channel['board'] = [' '] * 9
                            channel['ongoing_game'] = False
                            channel['accepted_invite'] = False
                            channel['possible_moves'] = [
                                0, 1, 2, 3, 4, 5, 6, 7, 8]
                            res = {
                                "response_type": "in_channel",
                                "text": "DRAW!\n " + "```" + game.print_board(game_board) + "```"
                            }

            if turn != user_name:
                res = {
                    "response_type": "ephemeral",
                    "text": "Sorry, it is not your turn."
                }
        if user_id not in players:
            player1 = channel['player1']
            player2 = channel['player2']
            res = {
                "response_type": "in_channel",
                "text": "Sorry, this is a game between %s and %s. To end their game type '/ttt end'" % (player1, player2)
            }

    # if channel['game_ended'] is True:
    #     res = {
    #         "response_type": "ephemeral",
    #         "text": "To start a new game type '/ttt challenge @username'"
    #     }

    if channel['accepted_invite'] is False and channel['ongoing_game'] is True:
        res = {
            "response_type": "in_channel",
            "text": "Waiting for %s to accept a game. To cancel invite type '/ttt end'" % channel['player2']
        }

    return res


def challenge(user_id, user_name, player2, channel):
    """Challenges another player in the same channel to a game of tictactoe"""
    if channel['ongoing_game'] is True:
        res = {
            "response_type": "ephemeral",
            "text": "There is already an ongoing game in this channel.",
        }

    if channel['ongoing_game'] is False:
        existing_users = util.create_memberlist(r)
        print existing_users
        if player2 not in existing_users:
            res = {
                "response_type": "ephemeral",
                "text": "That user is not in this channel",
            }

        if user_name and player2 in existing_users:
            channel['player1'] = user_name
            channel['player2'] = player2
            if user_name == player2:
                res = {
                    "response_type": "ephemeral",
                    "text": "You cannot challenge yourself",
                }
            if user_name != player2:
                players = channel['players']
                players |= {user_id}
                channel['ongoing_game'] = True
                res = {
                    "response_type": "in_channel",
                    "text": "Challenging %s to a match, to accept this match type '/ttt accept'" % player2,
                }

    return res


def accept(user_id, user_name, channel):
    players = channel['players']
    player2 = channel['player2']
    player1 = channel['player1']

    if channel['ongoing_game'] is False:
        res = {
            "response_type": "ephemeral",
            "text": "To start a game type '/ttt challenge @username'"
        }

    if channel['ongoing_game'] is True:
        if user_name == player2:
            players |= {user_id}
            channel['ongoing_game'] = True
            channel['accepted_invite'] = True
            channel['turn'] = player2
            game.initialize(player1, player2)
            res = {
                "response_type": "in_channel",
                "attachments": [
                    {
                        "text": "Please use the following cell number to make your move.\n/ttt move # - to make a move\n/ttt end - to end the game\n" + "```" + game.instructions() + "```" + "\nHere is the current game board:\n" + "```" + game.print_board(channel['board']) + "```",
                        "pretext": "Challenge accepted. %s starts the game. Your marker is 'O'. Please read the instructions below:" % player2,
                        "mrkdwn_in": ["text", "pretext"]
                    }
                ]
            }

        if user_name != player2:
            res = {
                "response_type": "ephemeral",
                "text": "You were not the challenged player.",
            }

    return res


def help():
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

    return res


def instructions():
    res = {
        "response_type": "ephemeral",

        "attachments": [
            {
                "text":  "```" + game.instructions() + "```",
                "pretext": "Please use the following cell numbers to make your move.\n/ttt move # - to make a move\n/ttt end - to end the game",
                "mrkdwn_in": ["text", "pretext"]
            }
        ]
    }

    return res


def end(channel):
    if channel['ongoing_game'] is False and channel['accepted_invite'] is False:
        res = {
            "response_type": "ephemeral",
            "text": "There's no ongoing game.",
        }

    if channel['accepted_invite'] is False and channel['ongoing_game'] is True:
        player2 = channel['player2']
        player1 = channel['player1']
        channel['ongoing_game'] = False
        res = {
            "response_type": "in_channel",
            "text": "Stopping challenge between %s and %s. To start a new game type '/ttt challenge @username'" % (player1, player2)
        }

    if channel['accepted_invite'] is True and channel['ongoing_game'] is True:
        player2 = channel['player2']
        player1 = channel['player1']
        channel['board'] = [' '] * 9
        channel['possible_moves'] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        channel['ongoing_game'] = False
        res = {
            "response_type": "in_channel",
            "text": "Game between %s and %s has been ended." % (player1, player2)
        }

    return res


def clear_game(channel):
    pass

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app, use_reloader=True)
