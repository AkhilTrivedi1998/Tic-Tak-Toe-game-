import pygame
from setting import *

pygame.init()

class Ai:
    def __init__(self, win):
        self.win = win
        self.turn = 0
        self.board = None
        self.playing = True
        self.winner = -1
        self.loadBoard()
        self.interact()

    def loadBoard(self):
        self.board = [x[:] for x in BOARD]

    def is_empty(self, i, j):
        if self.board[i][j] == '':
            return True
        else:
            return False

    def interact(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def get_board_value(self, i, j):
        return self.board[i][j]

    def get_winner(self):
        return self.winner

    def evaluate(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] and self.board[row][1] == self.board[row][2]:
                if self.board[row][0] == 'O':
                    return 10
                elif self.board[row][0] == 'X':
                    return -10
        for col in range(3):
            if self.board[0][col] == self.board[1][col] and self.board[1][col] == self.board[2][col]:
                if self.board[0][col] == 'O':
                    return 10
                elif self.board[0][col] == 'X':
                    return -10
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == 'O':
                return 10
            elif self.board[0][0] == 'X':
                return -10
        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == 'O':
                return 10
            elif self.board[0][2] == 'X':
                return -10
        return 0

    def isMovesLeft(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    return True
        return False

    def minimax(self, depth, isMax):
        score = self.evaluate()
        if score == 10:
            return score
        if score == -10:
            return score
        if self.isMovesLeft() == False:
            return 0
        if isMax:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'O'
                        best = max(best, self.minimax(depth + 1, not isMax))
                        self.board[i][j] = ''
            return best
        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'X'
                        best = min(best, self.minimax(depth + 1, not isMax))
                        self.board[i][j] = ''
            return best

    def findBestMove(self):
        bestVal = -1000
        bestMove = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'
                    moveVal = self.minimax(0, False)
                    self.board[i][j] = ''
                    if moveVal > bestVal:
                        bestMove = (i, j)
                        bestVal = moveVal
        return bestMove

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
                quit()
            elif self.turn == 0:
                mousePos = pygame.mouse.get_pos()
                if TOP_DOWN_BUFFER < mousePos[0] < TOP_DOWN_BUFFER + WIDTH and TOP_DOWN_BUFFER < mousePos[
                    1] < TOP_DOWN_BUFFER + WIDTH:
                    clicked = pygame.mouse.get_pressed()
                    if clicked[0] == 1:
                        i = (mousePos[0] - TOP_DOWN_BUFFER) // CELL_WIDTH
                        j = (mousePos[1] - TOP_DOWN_BUFFER) // CELL_WIDTH
                        if self.is_empty(i, j):
                            self.board[i][j] = 'X'
                            self.turn = (self.turn + 1) % 2
                            self.set_winner()
            elif self.turn == 1:
                bestMove = self.findBestMove()
                self.board[bestMove[0]][bestMove[1]] = 'O'
                self.turn = (self.turn + 1) % 2
                self.set_winner()

    def set_winner(self):
        z = self.evaluate()
        if z == 10:
            self.winner = 1
        elif z == -10:
            self.winner = 0
        elif z == 0:
            if not self.isMovesLeft():
                self.winner = 2

    def update(self):
        pygame.display.update()

    def draw_text(self, msg, color, pos=None, center=False, y_displacement=0):
        text = LARGEFONT.render(msg, True, color)
        if center == True:
            text_rect = text.get_rect(center=((WIDTH + 2*TOP_DOWN_BUFFER) // 2, (WIDTH + 2*TOP_DOWN_BUFFER) // 2 + y_displacement))
            self.win.blit(text, text_rect)
        else:
            self.win.blit(text, pos)

    def draw_text_with_timer(self, msg, sec, color, y_displacement=-200):
        text = LARGEFONT.render(msg, True, color)
        text_rect = text.get_rect(center=((WIDTH + 2 * TOP_DOWN_BUFFER) // 2, (WIDTH + 2 * TOP_DOWN_BUFFER) // 2 + y_displacement))
        self.win.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(sec*1000)

    def draw(self):
        self.win.fill(GREENSHADE)
        self.draw_grid()
        self.draw_board()
        if self.get_winner() != -1:
            if self.get_winner() == 0:
                self.draw_text_with_timer('YOU WON', 2, BLACK)
            elif self.get_winner() == 1:
                self.draw_text_with_timer('YOU LOSE', 2, BLACK)
            else:
                self.draw_text_with_timer('TIE GAME', 2, BLACK)
            self.playing = False
        elif self.turn == 0:
            self.draw_text('make a move', BLUE, center=True, y_displacement=200)
        else:
            self.draw_text('opponents turn', BLUE, center=True, y_displacement=200)

    def draw_grid(self):
        self.win.fill(GREYISH, [TOP_DOWN_BUFFER, TOP_DOWN_BUFFER, WIDTH, WIDTH])
        pygame.draw.rect(self.win, WHITE, [TOP_DOWN_BUFFER, TOP_DOWN_BUFFER, WIDTH, WIDTH], 3)
        for i in range(3):
            pygame.draw.line(self.win, LIGHTBLUE, (i*CELL_WIDTH + TOP_DOWN_BUFFER, TOP_DOWN_BUFFER), (i*CELL_WIDTH + TOP_DOWN_BUFFER, TOP_DOWN_BUFFER + WIDTH), 3)
            pygame.draw.line(self.win, LIGHTBLUE, (TOP_DOWN_BUFFER, i * CELL_WIDTH + TOP_DOWN_BUFFER),
                             (TOP_DOWN_BUFFER + WIDTH, i * CELL_WIDTH + TOP_DOWN_BUFFER), 3)

    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.get_board_value(i, j) == 'X':
                    pygame.draw.line(self.win, BLACK, (i * CELL_WIDTH + TOP_DOWN_BUFFER + 5, j * CELL_WIDTH + TOP_DOWN_BUFFER + 5), ((i + 1) * CELL_WIDTH + TOP_DOWN_BUFFER - 5, (j + 1) * CELL_WIDTH + TOP_DOWN_BUFFER - 5), 2)
                    pygame.draw.line(self.win, BLACK, ((i + 1) * CELL_WIDTH + TOP_DOWN_BUFFER - 5, j * CELL_WIDTH + TOP_DOWN_BUFFER + 5), (i * CELL_WIDTH + TOP_DOWN_BUFFER + 5, (j + 1) * CELL_WIDTH + TOP_DOWN_BUFFER - 5), 2)
                elif self.get_board_value(i, j) == 'O':
                    pygame.draw.circle(self.win, BLACK, (i * CELL_WIDTH + TOP_DOWN_BUFFER + (CELL_WIDTH // 2), j * CELL_WIDTH + TOP_DOWN_BUFFER + (CELL_WIDTH // 2)), CELL_WIDTH // 2 - 10, 2)
