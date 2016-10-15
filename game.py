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
        self.moves_left = 9
        self.game_board = '| %s | %s | %s |\t\n-------------\n| %s | %s | %s |\t\n-------------\n| %s | %s | %s |'

    def instructions(self):
      return self.game_board % (1,2,3,4,5,6,7,8,9)

    def print_board(self, board):
      return self.game_board % tuple(self.board[6:9] + self.board[3:6] + self.board[0:3])

    def initialize(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def make_move(self, cell, player, board):
        self.moves_left -= 1
        if player == self.player1:
            if self.is_winner(board, cell) == False:
                if self.is_board_full() == False:
                    board[cell] = 'X'
                if self.is_board_full() == True and self.is_winner(board,cell) == False:
                    return "Draw"
            if self.is_winner(board, cell) == True:
                return "Winner: Player1"

        if player == self.player2:
            if self.is_winner(board, cell) == False:
                if self.is_board_full() == False:
                    board[cell] = 'O'
                if self.is_board_full() == True and self.is_winner(board,cell) == False:
                    return "Draw"
            if self.is_winner(board, cell) == True:
                return "Winner: Player2"
        return self.print_board(board)

    def is_winner(self, board, cell):
        "check if this cell will win the game"
        for combo in self.winning_combos:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] == cell):
                return True
        return False

    def is_board_full(self):
        "checks if the board is full"
        for i in range(1,9):
            if self.is_space_free(self.board, i):
                return False
        return True

    def is_space_free(self, board, cell):
        "checks for free space of the board"
        return board[cell] == ' '