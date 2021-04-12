class Game:
    def __init__(self, gameID):
        self.game_id = gameID
        self.players_present = [False, False]
        self.players_terminate = [False, False]
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        self.turn = 0
        self.winner = -1

    def print_board(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    print('_', end=' ')
                else:
                    print(self.board[i][j], end=' ')
            print('')

    def get_board_value(self, i, j):
        return self.board[i][j]

    def is_terminate(self):
        if self.players_terminate[0] == True or self.players_terminate[1] == True:
            return True
        else:
            return False

    def get_winner(self):
        return self.winner

    def is_empty(self, i, j):
        if self.board[i][j] == '':
            return True
        else:
            return False

    def whose_turn(self):
        return self.turn

    def start_game(self):
        if self.players_present[0] == True and self.players_present[1] == True:
            return True
        else:
            return False

    def change_players_terminate(self, playerID):
        self.players_terminate[playerID] = True

    def change_players_present(self, playerID):
        self.players_present[playerID] = True

    def change_turn(self):
        self.turn = (self.turn + 1) % 2

    def make_move(self, playerID, move):
        self.board[move[0]][move[1]] = 'X' if playerID == 0 else 'O'

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != '':
                self.winner = 0 if self.board[i][0] == 'X' else 1
                break
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != '':
                self.winner = 0 if self.board[0][i] == 'X' else 1
                break
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '':
            self.winner = 0 if self.board[0][0] == 'X' else 1
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '':
            self.winner = 0 if self.board[0][2] == 'X' else 1
        if self.winner == -1:
            k = 1
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '':
                        k = 0
                        break
            if k == 1:
                self.winner = 2
