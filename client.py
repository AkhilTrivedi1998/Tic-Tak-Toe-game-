import pickle
import pygame
from game import *
from network import *
from setting import *

pygame.init()

class Client:
    def __init__(self, win, ip, port):
        self.win = win
        self.ip = ip
        self.port = port
        self.n = Network(self.ip, self.port)
        self.player_id = None
        self.g = None
        self.playing = True
        if self.n.get_connected():
            self.interact()

    def check_connected(self):
        if self.n.get_connected():
            return True
        else:
            return False

    def interact(self):
        data = self.n.recv(2048)
        self.player_id = int(data.decode('utf-8'))
        self.g = pickle.loads(self.n.recv(4096))
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
                quit()
            elif self.g.whose_turn() == self.player_id:
                mousePos = pygame.mouse.get_pos()
                if TOP_DOWN_BUFFER < mousePos[0] < TOP_DOWN_BUFFER + WIDTH and TOP_DOWN_BUFFER < mousePos[1] < TOP_DOWN_BUFFER + WIDTH:
                    clicked = pygame.mouse.get_pressed()
                    if clicked[0] == 1:
                        i = (mousePos[0] - TOP_DOWN_BUFFER) // CELL_WIDTH
                        j = (mousePos[1] - TOP_DOWN_BUFFER) // CELL_WIDTH
                        if self.g.is_empty(i, j):
                            self.n.send('move')
                            self.n.send_obj(pickle.dumps([i, j]))
                            self.g = pickle.loads(self.n.recv(2048))

    def update(self):
        pygame.display.update()

    def draw(self):
        self.win.fill(GREENSHADE)
        if self.g.start_game():
            self.draw_grid()
            self.draw_board()
            if self.g.get_winner() != -1:
                if self.g.get_winner() == self.player_id:
                    self.draw_text_with_timer('YOU WON', 2, BLACK)
                elif self.g.get_winner() == (self.player_id + 1) % 2:
                    self.draw_text_with_timer('YOU LOSE', 2, BLACK)
                else:
                    self.draw_text_with_timer('TIE GAME', 2, BLACK)
                self.playing = False
            elif self.g.is_terminate():
                self.draw_text_with_timer('connection got terminated', 2, BLACK)
                self.playing = False
            elif self.g.whose_turn() == self.player_id:
                self.draw_text('make a move', BLUE, center=True, y_displacement=200)
            else:
                self.draw_text('opponents turn', BLUE, center=True, y_displacement=200)
                self.n.send('get')
                self.g = pickle.loads(self.n.recv(2048))
        else:
            self.draw_text("game hasn't started yet...", BLUE, center=True)
            self.draw_text('ip = '+self.ip, BLUE, center=True, y_displacement=200)
            self.n.send('get')
            self.g = pickle.loads(self.n.recv(2048))

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
                if self.g.get_board_value(i, j) == 'X':
                    pygame.draw.line(self.win, BLACK, (i * CELL_WIDTH + TOP_DOWN_BUFFER + 5, j * CELL_WIDTH + TOP_DOWN_BUFFER + 5), ((i + 1) * CELL_WIDTH + TOP_DOWN_BUFFER - 5, (j + 1) * CELL_WIDTH + TOP_DOWN_BUFFER - 5), 2)
                    pygame.draw.line(self.win, BLACK, ((i + 1) * CELL_WIDTH + TOP_DOWN_BUFFER - 5, j * CELL_WIDTH + TOP_DOWN_BUFFER + 5), (i * CELL_WIDTH + TOP_DOWN_BUFFER + 5, (j + 1) * CELL_WIDTH + TOP_DOWN_BUFFER - 5), 2)
                elif self.g.get_board_value(i, j) == 'O':
                    pygame.draw.circle(self.win, BLACK, (i * CELL_WIDTH + TOP_DOWN_BUFFER + (CELL_WIDTH // 2), j * CELL_WIDTH + TOP_DOWN_BUFFER + (CELL_WIDTH // 2)), CELL_WIDTH // 2 - 10, 2)
