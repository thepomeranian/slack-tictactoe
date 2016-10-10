class Game:
    """Tic-Tac-Toe class"""

    def __init__(self):
        self.board = [' '] * 9
        self.player1 = ''
        self.player2 = ''
        self.winning_combos = (
            [6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6],
        )
        self.corners = [0, 2, 6, 8]
        self.sides = [1, 3, 5, 7]
        self.middle = 4
        self.game_board = '\t| %s | %s | %s |\t\n-------------\n| %s | %s | %s |\t\n-------------\n| %s | %s | %s |'

    def instructions(self):
      return self.game_board % (1,2,3,4,5,6,7,8,9)