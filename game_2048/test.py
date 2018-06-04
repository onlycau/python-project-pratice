#-*- coding:utf-8 -*-

'game 2048 by python'

__author__='onlycau'


from random import randrange, choice
import time, copy,os

help_string1=('  (W)Up (S)Down (A)Left (D)Right')
help_string2=('      (R)Restart (Q)Exit ')

class GameField(object):
    



    def __init__(self,height=4,width=4,win=2048):
        self.height=height
        self.width=width
        self.score=0
        self.highscore=0
        self.reset()

    def spawn(self):# add a new random element at the field
        new_element=4 if randrange(100)>80 else 2
        (i,j)=choice([(i,j)for i in range(self.width) for j in range(self.height) if self.field[i][j]==0])
        self.field[i][j]=new_element

    def reset(self): #resset field
        self.field=[[0 for i in range(self.width)]for j in range(self.height)]
        self.spawn()
        self.spawn()


    def draw_board(self): #draw field and fill in with data
        print('score:%d'%(self.score))
        line='+-------'*self.width+'+'
        row='|       '*self.width+'|'
        for i in range(self.height):
            print(line)
            print(row)
            for j in range(self.width):
                print('|'+('%s'%(self.field[i][j]or '')).center(7),end='')
            print('|\n'+row)
        print(line)
        print(help_string1)
        print(help_string2)

    def move_left(self):
        new_field=[]
        for old_row in self.field:
            row=[i for i in old_row if i!=0]
            for i in range(len(row)-1):
                if row[i]==row[i+1]:
                    self.score+=row[i]
                    row[i]=row[i]*2
                    row[i+1]=0
            row=[i for i in row if i!=0]
            for i in range(self.width-len(row)):
                row.append(0)
            new_field.append(row)
        self.field=new_field
    def move_right(self):
        self.field=[row[::-1]for row in self.field]
        self.move_left()
        self.field=[row[::-1]for row in self.field]            
    def move_up(self):
        self.field=[list(row) for row in zip(*self.field)]
        self.move_left()
        self.field=[list(row) for row in zip(*self.field)]
    def move_down(self):
        self.field=[list(row) for row in zip(*self.field)]
        self.move_right()
        self.field=[list(row) for row in zip(*self.field)]

    def move_is_possible(self):
        field_add=copy.deepcopy(self.field)
        field_add.append([1 for i in range(self.width)])
        for row in field_add:
            row.append(1)

        for i in range(self.width):
            for j in range(self.height):
                if not self.field[i][j]:
                    return True
                if field_add[i][j]==field_add[i+1][j] or field_add[i][j]==field_add[i][j+1]:
                    return True
        return False

    def get_action(self):
        action=input()
        while action not in 'wasdqr':
            action=input()  
        return action      


    def start(self):
        self.reset()
        self.draw_board()
        self.get_action()

    def game(self,direction):

        if not self.move_is_possible():
            return self.fail()            
        if direction=='a':
            self.move_left()
        elif direction=='d':
            self.move_right()
        elif direction=='w':
            self.move_up()
        elif direction=='s':
            self.move_down()
        self.spawn()
        self.draw_board()
        self.get_action()

    def win(self):
        print('win')

    def fail(self):
        print('     Game over     ')
        action=self.get_action()
        if action=='q':
            os._exit(0)       
        if action=='r':
            self.start()


    def play(self,action):
        if action=='q':
            self.exit()
        if action=='r':
            self.start()
        else:
            self.game(action)


    def exit(self):
        os._exit(0)

def main():
    game_2048=GameField()
    action=game_2048.start()
    while True:
        action=game_2048.play(action)


main()
