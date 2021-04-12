import pygame
from setting import *

pygame.init()

class Button:
    def __init__(self, win, x, y, w, h, msg, activeColor, inactiveColor, buttonID=None):
        self.win = win
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.msg = msg
        self.activeColor = activeColor
        self.inactiveColor = inactiveColor
        self.state = 'inactive'
        self.button_id = buttonID

    def get_button_id(self):
        return self.button_id

    def draw(self):
        text = LARGEFONT.render(self.msg, True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        if self.state == 'inactive':
            self.win.fill(self.inactiveColor, [self.x, self.y, self.w, self.h])
        elif self.state == 'active':
            self.win.fill(self.activeColor, [self.x, self.y, self.w, self.h])
        self.win.blit(text, text_rect)

    def change_state(self, state):
        self.state = state

    def get_dimension(self):
        return [self.x, self.y, self.w, self.h]