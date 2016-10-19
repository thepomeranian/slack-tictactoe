#Slack TicTacToe

###A slack command that allows two users in the same team to engage in a game of tictactoe.

###Commands
- ***'/ttt game'*** - Returns the current game status, game board, and whose turn it is if there is an ongoing game.
- ***'/ttt move #'*** - Returns a draw, winner, or prints the new board after a player makes a move
- ***'/ttt accept'*** - Allows the challenged player to accept a challenge
- ***'/ttt end'*** - Ends the game regardless of it's current state.
- ***'/ttt help'*** - Returns all of the possible moves for the slash command
- ***'/ttt instructions'*** - Returns the instructions for the game
- ***'/ttt challenge @username'*** - Challenges another player in the same channel to a game of tictactoe

###Tech Stack
This information can be found in `Requirements.txt`
```
click==6.6
Flask==0.11.1
itsdangerous==0.24
Jinja2==2.8
MarkupSafe==0.23
requests==2.11.1
slacker==0.9.25
tabulate==0.7.5
Werkzeug==0.11.11
```

###Screenshots
![](http://i.imgur.com/5liv5Cs.gif)

###Wakatime Log
https://wakatime.com/@kawaiiru/projects/pgnacjtppp?start=2016-10-05&end=2016-10-18

###Psuedocode
```
commands = ['game', 'challenge', 'end', 'accept', 'help', 'instructions', 'move']

if text in commands

  if game in text
    if not ongoing_game
      print /ttt challenge @username to start a game
    if ongoing_game and not accepted_invite
      print waiting for player2 to accept the game, to end the game type '/ttt end'
    if ongoing_game
      print current board and whose turn it is, to end the game type '/ttt end'

  if challenge in text
    if ongoing_game
      print current board and whose turn it is, to end the game type '/ttt end'
    if not ongoing_game
      if player2 not in channel
        print user not in channel
      if player2 is player1
        print cannot challenge self
      if player2 and player1 in channel
        ongoing_game = True
        accepted_invite = True
        print challenging player2, player2 to accept the match type '/ttt accept' 

  if end in text
    if ongoing_game
      ongoing_game = False
      print game between player1 and player2 has been ended

  if accept in text
    if ongoing_game
      if username == player2
        print challenge accepted, player1
        print instructions
        print board
      if username != player2
        print sorry, you were not the challenged player. to end the game type '/ttt end'
    if not ongoing_game
      print sorry, there is no game initiated in this channel. To start a game type '/ttt challenge @username'

  if help in text
    print all possible actions
      /ttt game - print the current game
      /ttt challenge @username - to challenge another player in the same channel
      /ttt end - ends the current game
      /ttt accept - accept a challenge

  if instructions in text
    print sample board
    print game instructions
      /ttt move # - to make a move
      /ttt end - to end the game

  if move in text
    if accepted_invite = True
      if user_id in players
        if # in possible_moves
          make_move()
          print new board
        if # not in possible_moves
          print sorry, that is not a valid move. here are the possible moves left
      if user_id not in players
        print sorry, this is a game between player1 and player2. to end their game, type '/ttt end'
    if not ongoing_game
      print /ttt challenge @username to start a game

else
  print sorry, i did not understand that. type '/ttt help for a list of possible commands'
```
