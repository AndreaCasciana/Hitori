#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''
import numpy
from boardgame import BoardGame, console_play
from boardgamegui import gui_play
import random
class Fifteen(BoardGame):

    def __init__(self, w: int, h: int, type: int):
        self._w, self._h = w, h
        self._x0, self._y0 = w - 1, h - 1
        self._board = []
        if type == 0:
            for x in range (w*h): #valori casuali
                self._board.append(str(random.randint(1, w)))
        else:
            self.readfile() #prende valori da file
        self._utente = self._board.copy()
        

    def cols(self) -> int:
        return self._w

    def rows(self) -> int:
        return self._h

    def message(self,x: int) -> str:
        if x == 0:
            return "Puzzle Risolto!"
        if x == 1:
            return "Alcuni numeri si ripetono, controlla meglio!"
        if x == 2:
            return "Ci sono celle nere che si toccano!"
        if x == 3:
            return "Celle bianche non contigue"
    
    
    
    def readfile(self): #prende valori da file csv e li copia nell'array
        cols,rows,count,count2 = 0,0,0,0
        text=""
        with open("hitori.csv", "r") as f3:
            for line in f3:
                cols = line.count(",")+1
                rows +=1
                text = text+str(line.strip()+",")
        array=[]
        self._h, self._w = rows,cols
        self._x0, self._y0 = self._w - 1, self._h - 1
        text = text.split(",")
        count = cols*rows
        for i in range(count):
            array.append(text[count2])
            count2+=1
        self._board = array.copy()
        
        
    def status (self,x: int, y: int) -> str: #in base allo stato nasconde, mostra o cerchia sul canvas
        b, w, h = self._board, self._w, self._h
        if b[y * w + x] == "nero":
            return "BLACK"
        if b[y * w + x] == "c":
            return "CIRCLE"
        if 0 <= int(y) < int(h) and 0 <= int(x) < int(w) and int(b[y * w + x]) > 0:
            return "CLEAR"
        return ""
    
    def value_at(self, x: int, y: int) -> str: #prende valore
        a, b, w, h = self._utente, self._board, self._w, self._h
        if b[y * w + x] == "nero":
            return str("nero")
        if b[y * w + x] == "c":
            return str(a[y * w + x])
        if 0 <= int(y) < int(h) and 0 <= int(x) < int(w) and int(b[y * w + x]) > 0:
            return str(b[y * w + x])
        return ""

    def play_at(self, x: int, y: int): #nasconde
        x0, y0, w, h = self._x0, self._y0, self._w, self._h
        if 0 <= y < h and 0 <= x < w:
            a, b, i0, i1 = self._utente, self._board, y0 * w + x0, y * w + x
            if b[i1] != "nero":
                b[i0], b[i1] = b[i0], "nero" 
            else:
                b[i0], b[i1] = b[i0], a[i1] 
            self._x0, self._y0 = x, y

    def flag_at(self, x: int, y: int): #cerchia
        x0, y0, w, h = self._x0, self._y0, self._w, self._h
        b, i0, i1 = self._board, y0 * w + x0, y * w + x
        b[i0], b[i1] = b[i0], "c"
        self._x0, self._y0 = x, y

    def finished(self) -> int: #controlla che non ci siano valori ripetuti o celle nere affiancate
        w, h, b_cells = self._w, self._h,0
        try:
            matrix = numpy.zeros((w,h),str)
            matrix2 = numpy.zeros((w,h),str)
            count2=0
            for q in range(h):
                for e in range (w):
                    matrix[q][e]=self._board[count2]
                    matrix2[q][e]=self._utente[count2]
                    count2+=1
            for z in range(w):
                for j in range(h):
                    n=matrix[z][j] #prende valore da controllare (se e' ripetuto, in caso sia un numero, se ci sono celle nere vicine in caso sia una cella annerita)
                    if matrix[z][j]=="n": #serve per controllare successivamente la contiguita' delle celle bianche
                        b_cells+=1
                    if matrix[z][j]=="c": #se il numero e' cerchiato, va a prendere il valore dall'altra matrice
                        n=matrix2[z][j]
                    for x in range(1+z,w):
                        if matrix[x][j]=="n": #controlla che non ci siano celle nere vicine verticalmente
                            if  matrix[z+1][j] =="n" and n=="n":
                                return 2
                        elif matrix[x][j]=="c": #controlla che non ci siano numeri ripetuti verticalmente (anche se il numero e' cerchiato)
                            if n == matrix2[x][j] and n!="n":
                                return 1
                        else:
                            if n == matrix[x][j] and n!="n": #controlla che non ci siano numeri ripetuti verticalmente
                                return 1
                    for y in range(1+j,w): #stessi controlli di prima ma in orizzontale
                        if matrix[z][y]=="n":
                            if  matrix[z][j+1] =="n" and n=="n":
                                return 2
                        elif matrix[z][y]=="c":
                            if n == matrix2[z][y] and n!="n":
                                return 1
                        else:
                            if n == matrix[z][y] and n!="n":
                                return 1 
            if b_cells>w*h/3: #minimo controllo, anche se non efficace al 100% sulla contiguita' delle celle bianche
                return 3               
        except:
            pass
               
def main():
    game = Fifteen(8, 8, 1) #il terzo valore puo' essere 0 o 1:
    gui_play(game)          #0 = genera automaticamente, 1 = prendi valori da file
    ##console_play(game)    #in caso sia 0, la matrice si adatta in base alla grandezza fornita
                            #in caso sia 1, assume la stessa grandezza della matrice sul file csv
main()
