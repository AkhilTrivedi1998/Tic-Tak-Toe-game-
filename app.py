import pygame
import socket
import tkinter
from tkinter import ttk
from tkinter import messagebox
from server import *
from client import *
from setting import *
from button import *
from _thread import *
from ai import *
from multiplayer import *

pygame.init()

class App:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH + 2*TOP_DOWN_BUFFER, WIDTH + 2*TOP_DOWN_BUFFER))
        pygame.display.set_caption("TIC TAK TOE")
        self.running = True
        # state can be 'playing', 'start_menu', 'menu', 'rules', 'host_join_menu', 'host', 'join', 'ai'
        self.state = 'start_menu'
        self.board = None
        self.playing_buttons = []
        self.start_menu_buttons = []
        self.rules_buttons = []
        self.menu_buttons = []
        self.host_join_menu_buttons = []
        self.loadButtons()
        self.loadBoard()

    def run(self):
        while self.running:
            if self.state == 'start_menu':
                self.start_menu_draw()
                self.start_menu_event()
                self.start_menu_update()
            elif self.state == 'rules':
                self.rules_draw()
                self.rules_event()
                self.rules_update()
            elif self.state == 'menu':
                self.menu_draw()
                self.menu_event()
                self.menu_update()
            elif self.state == 'playing':
                self.playing_update()
                self.playing_draw()
                self.playing_event()
            elif self.state == 'host_join_menu':
                self.host_join_menu_update()
                self.host_join_menu_draw()
                self.host_join_menu_event()
            elif self.state == 'pause':
                self.pause_event()
        pygame.quit()
        quit()

####################################  HOST JOIN MENU   #####################################################

    def host_join_menu_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.mouse_hover_and_click()

    def host_join_menu_update(self):
        pygame.display.update()

    def host_join_menu_draw(self):
        self.win.fill(GREENSHADE)
        for btn in self.host_join_menu_buttons:
            btn.draw()

###############################  START MENU   #####################################################

    def start_menu_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.mouse_hover_and_click()

    def start_menu_update(self):
        pygame.display.update()

    def start_menu_draw(self):
        self.win.fill(GREENSHADE)
        for btn in self.start_menu_buttons:
            btn.draw()

#######################################  RULES   ####################################################

    def rules_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.mouse_hover_and_click()

    def rules_draw(self):
        self.win.fill(GREENSHADE)
        for btn in self.rules_buttons:
            btn.draw()
        self.draw_text('Based on the rules of simple Tic Tak Toe Game', BLUE, center=True, y_displacement=-100)

    def rules_update(self):
        pygame.display.update()

######################################  MENU  ####################################################

    def menu_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.mouse_hover_and_click()

    def menu_draw(self):
        self.win.fill(GREENSHADE)
        for btn in self.menu_buttons:
            btn.draw()

    def menu_update(self):
        pygame.display.update()

#################################  PAUSE STATE   ####################################################
    
    def pause_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = 'playing'
    
    def draw_pause(self, color):
        text = LARGEFONT.render('PAUSE', True, color)
        text_rect = text.get_rect(center=((WIDTH + 2*TOP_DOWN_BUFFER) // 2, (WIDTH + 2*TOP_DOWN_BUFFER) // 2))
        self.win.blit(text, text_rect)
        pygame.display.update()

##################################  PLAYING STATE  ###################################################

    def playing_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.draw_pause(BLACK)
                    self.state = 'pause'
        self.mouse_hover_and_click()

    def playing_update(self):
        pygame.display.update()
    
    def playing_draw(self):
        self.win.fill(GREENSHADE)
        for btn in self.playing_buttons:
            btn.draw()
        self.draw_grid()

    def draw_grid(self):
        self.win.fill(GREYISH, [TOP_DOWN_BUFFER, TOP_DOWN_BUFFER, WIDTH, WIDTH])
        pygame.draw.rect(self.win, WHITE, [TOP_DOWN_BUFFER, TOP_DOWN_BUFFER, WIDTH, WIDTH], 3)
        for i in range(3):
            pygame.draw.line(self.win, LIGHTBLUE, (i*CELL_WIDTH + TOP_DOWN_BUFFER, TOP_DOWN_BUFFER), (i*CELL_WIDTH + TOP_DOWN_BUFFER, TOP_DOWN_BUFFER + WIDTH), 3)
            pygame.draw.line(self.win, LIGHTBLUE, (TOP_DOWN_BUFFER, i * CELL_WIDTH + TOP_DOWN_BUFFER),
                             (TOP_DOWN_BUFFER + WIDTH, i * CELL_WIDTH + TOP_DOWN_BUFFER), 3)

######################################  HELPER FUNCTIONS  #####################################################

    def loadButtons(self):
        self.start_menu_buttons.append(
            Button(self.win, 200, 130, 100, 50, 'MENU', GREYISH, DARKGREY, 'start_menu_menu'))
        self.start_menu_buttons.append(
            Button(self.win, 200, 230, 100, 50, 'RULES', GREYISH, DARKGREY, 'start_menu_rules'))
        self.start_menu_buttons.append(
            Button(self.win, 200, 330, 100, 50, 'QUIT', GREYISH, DARKGREY, 'start_menu_quit'))
        self.playing_buttons.append(Button(self.win, 50, 25, 100, 30, 'RESTART', GREYISH, DARKGREY, 'playing_restart'))
        self.playing_buttons.append(Button(self.win, 350, 25, 100, 30, 'QUIT', GREYISH, DARKGREY, 'playing_quit'))
        self.rules_buttons.append(Button(self.win, 50, 25, 100, 30, 'MENU', GREYISH, DARKGREY, 'rules_menu'))
        self.rules_buttons.append(Button(self.win, 350, 25, 100, 30, 'QUIT', GREYISH, DARKGREY, 'rules_quit'))
        self.host_join_menu_buttons.append(Button(self.win, 50, 150, 100, 30, 'HOST', GREYISH, DARKGREY, 'host_join_menu_host'))
        self.host_join_menu_buttons.append(Button(self.win, 350, 150, 100, 30, 'JOIN', GREYISH, DARKGREY, 'host_join_menu_join'))
        self.host_join_menu_buttons.append(
            Button(self.win, 350, 450, 100, 30, 'MENU', GREYISH, DARKGREY, 'host_join_menu_menu'))
        self.menu_buttons.append(Button(self.win, 50, 100, 400, 30, 'MULTIPLAYER', GREYISH, DARKGREY, 'menu_multiplayer'))
        self.menu_buttons.append(Button(self.win, 50, 250, 400, 30, 'COMPUTER', GREYISH, DARKGREY, 'menu_computer'))
        self.menu_buttons.append(Button(self.win, 50, 400, 400, 30, 'NETWORK', GREYISH, DARKGREY, 'menu_network'))
        self.menu_buttons.append(Button(self.win, 50, 25, 100, 30, 'MENU', GREYISH, DARKGREY, 'menu_menu'))
        self.menu_buttons.append(Button(self.win, 350, 25, 100, 30, 'QUIT', GREYISH, DARKGREY, 'menu_quit'))

    def pop_up_error(self, msg):
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror("ERROR", msg)
        root.destroy()

    def action(self, window, var, ip_val):
        ip_val.append(var.get())
        window.destroy()

    def enter_ip(self, ip_val):
        window = tkinter.Tk()
        label1 = ttk.Label(window, text="Enter ip : ")
        label2 = ttk.Label(window, text="")
        var = tkinter.StringVar()
        entry1 = ttk.Entry(window, textvariable=var)
        submit = ttk.Button(window, text="submit", command=lambda : self.action(window, var, ip_val))
        label1.grid(column=0, row=0)
        entry1.grid(column=0, row=1)
        submit.grid(column=0, row=3)
        label2.grid(column=0, row=4)
        window.mainloop()

    def loadBoard(self):
        self.board = BOARD
        
    def draw_text(self, msg, color, pos=None, center=False, y_displacement=0):
        text = LARGEFONT.render(msg, True, color)
        if center == True:
            text_rect = text.get_rect(center=((WIDTH + 2*TOP_DOWN_BUFFER) // 2, (WIDTH + 2*TOP_DOWN_BUFFER) // 2 + y_displacement))
            self.win.blit(text, text_rect)
        else:
            self.win.blit(text, pos)

    def mouse_hover_and_click(self):
        mousePos = pygame.mouse.get_pos()
        if self.state == 'start_menu':
            for i, btn in enumerate(self.start_menu_buttons):
                dim = btn.get_dimension()
                if dim[0] < mousePos[0] < dim[0] + dim[2] and dim[1] < mousePos[1] < dim[1] + dim[3]:
                    btn.change_state('active')
                    btnClick = pygame.mouse.get_pressed()
                    if btnClick[0] == 1:
                        if btn.get_button_id() == 'start_menu_menu':
                            self.state = 'menu'
                        elif btn.get_button_id() == 'start_menu_rules':
                            self.state = 'rules'
                        elif btn.get_button_id() == 'start_menu_quit':
                            self.running = False
                else:
                    btn.change_state('inactive')
        elif self.state == 'playing':
            for i, btn in enumerate(self.playing_buttons):
                dim = btn.get_dimension()
                if dim[0] < mousePos[0] < dim[0] + dim[2] and dim[1] < mousePos[1] < dim[1] + dim[3]:
                    btn.change_state('active')
                    btnClick = pygame.mouse.get_pressed()
                    if btnClick[0] == 1:
                        if btn.get_button_id() == 'playing_restart':
                            self.loadBoard()
                        elif btn.get_button_id() == 'playing_quit':
                            self.running = False
                else:
                    btn.change_state('inactive')
        elif self.state == 'host_join_menu':
            for i, btn in enumerate(self.host_join_menu_buttons):
                dim = btn.get_dimension()
                if dim[0] < mousePos[0] < dim[0] + dim[2] and dim[1] < mousePos[1] < dim[1] + dim[3]:
                    btn.change_state('active')
                    btnClick = pygame.mouse.get_pressed()
                    if btnClick[0] == 1:
                        if btn.get_button_id() == 'host_join_menu_host':
                            ip = socket.gethostbyname(socket.gethostname())
                            port = 5557
                            start_new_thread(Server, (ip, port))
                            pygame.time.wait(int(0.5 * 1000))
                            c = Client(self.win, ip, port)
                        elif btn.get_button_id() == 'host_join_menu_join':
                            ip = []
                            port = 5557
                            self.enter_ip(ip)
                            pygame.event.clear()
                            print(ip[-1])
                            c1 = Client(self.win, ip[-1], port)
                            if not c1.check_connected():
                                self.pop_up_error('wrong address')
                                pygame.event.clear()
                        elif btn.get_button_id() == 'host_join_menu_menu':
                            self.state = 'menu'
                else:
                    btn.change_state('inactive')
        elif self.state == 'rules':
            for i, btn in enumerate(self.rules_buttons):
                dim = btn.get_dimension()
                if dim[0] < mousePos[0] < dim[0] + dim[2] and dim[1] < mousePos[1] < dim[1] + dim[3]:
                    btn.change_state('active')
                    btnClick = pygame.mouse.get_pressed()
                    if btnClick[0] == 1:
                        if btn.get_button_id() == 'rules_menu':
                            self.state = 'start_menu'
                        elif btn.get_button_id() == 'rules_quit':
                            self.running = False
                else:
                    btn.change_state('inactive')
        elif self.state == 'menu':
            for i, btn in enumerate(self.menu_buttons):
                dim = btn.get_dimension()
                if dim[0] < mousePos[0] < dim[0] + dim[2] and dim[1] < mousePos[1] < dim[1] + dim[3]:
                    btn.change_state('active')
                    btnClick = pygame.mouse.get_pressed()
                    if btnClick[0] == 1:
                        if btn.get_button_id() == 'menu_multiplayer':
                            z1 = Multiplayer(self.win)
                        elif btn.get_button_id() == 'menu_computer':
                            z = Ai(self.win)
                        elif btn.get_button_id() == 'menu_network':
                            self.state = 'host_join_menu'
                        elif btn.get_button_id() == 'menu_menu':
                            self.state = 'start_menu'
                        elif btn.get_button_id() == 'menu_quit':
                            self.running = False
                else:
                    btn.change_state('inactive')
