#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

import g2d
from boardgame import BoardGame
from time import time

W, H = 40, 40
LONG_PRESS = 0.5

class BoardGameGui:
    def __init__(self, g: BoardGame):
        self._game = g
        self._downtime = 0
        self._action = 0
        self.update_buttons()
        

    def tick(self):
        if g2d.key_pressed("LeftButton"):
            self._downtime = time()
        elif g2d.key_released("LeftButton"): #cerchia un numero o lo nasconde
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            if time() - self._downtime > LONG_PRESS:
                self._game.flag_at(x, y)
            else:
                self._game.play_at(x, y)
            self.update_buttons()
        elif g2d.key_released("Spacebar"): #check: controlla se il puzzle e' risolto
                res = self._game.finished()
                if res !=None:
                    g2d.alert(self._game.message(int(res)))
                else:
                    g2d.alert(self._game.message(0))
    def update_buttons(self):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        cols, rows = self._game.cols(), self._game.rows()
        for y in range(1, rows):
            g2d.draw_line((0, y * H), (cols * W, y * H))
        for x in range(1, cols):
            g2d.draw_line((x * W, 0), (x * W, rows * H))
        for y in range(rows):
            for x in range(cols):
                value = self._game.value_at(x, y) #cerchia, nasconde o mostra numero in base al valore nel vettore
                if self._game.status(x,y) == "CLEAR":
                    self._action = 0
                elif self._game.status(x,y) == "BLACK":
                    self._action = 1
                elif self._game.status(x,y) == "CIRCLE":
                    self._action = 2
                #print(self._action)
                center = x * W + W//2, y * H + H//2
                if self._action == 2: #cerchia
                    g2d.set_color((255, 0, 0))
                    g2d.fill_circle((center), H//2)
                    g2d.set_color((255, 255, 255))
                    g2d.fill_circle((center), H//2-3)
                    self._action = 0
                if self._action == 1: #nasconde
                    g2d.set_color((0, 0, 0))
                    g2d.fill_rect((x * W + W//2-W/2, y * H + H//2-H/2, W, H))
                    self._action = 0
                g2d.set_color((0, 0, 0))
                g2d.draw_text_centered(value, center, H//2)
                g2d.set_color((0, 0, 0)) #instruzioni comandi
                g2d.draw_text_centered("HITORI",(self._game.cols() * W/2,self._game.rows() * H+20),20)
                g2d.set_color((50, 50, 50))
                g2d.draw_text_centered("click: hide/show",(self._game.cols() * W/2,self._game.rows() * H+40),15)
                g2d.set_color((50, 50, 50))
                g2d.draw_text_centered("hold: circle",(self._game.cols() * W/2,self._game.rows() * H+55),15)
                g2d.set_color((50, 50, 50))
                g2d.draw_text_centered("spacebar: check",(self._game.cols() * W/2,self._game.rows() * H+70),15)
        g2d.update_canvas()
        
           

def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W, game.rows() * H+80))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)
