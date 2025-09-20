import random
from tkinter import *
from tkinter import messagebox

class FifteenPuzzle:
    def __init__(self):
        self.board = []
        num = 1
        for i in range(4):
            row = []
            for j in range(4):
                if num <= 15:
                    row.append(num)
                    num += 1
                else:
                    row.append(0)
            self.board.append(row)
        self.scramble()
        
    def scramble(self):
        for _ in range(1000):
            empty_pos = self.find_empty_pos()
            if empty_pos is None:
                self.board[3][3] = 0
                empty_pos = (3,3)
            empty_row, empty_col = empty_pos
            directions = []
            if empty_col > 0:
                directions.append('left')
            if empty_col < 3:
                directions.append('right')
            if empty_row > 0:
                directions.append('up')
            if empty_row < 3:
                directions.append('down')
            directions = random.choice(directions)
            if directions == 'up':
                self.board[empty_row][empty_col] = self.board[empty_row-1][empty_col]
                self.board[empty_row-1][empty_col] = 0
            if directions == 'down':
                self.board[empty_row][empty_col] = self.board[empty_row+1][empty_col]
                self.board[empty_row+1][empty_col] = 0
            if directions == 'right':
                self.board[empty_row][empty_col] = self.board[empty_row][empty_col+1]
                self.board[empty_row][empty_col+1] = 0
            if directions == 'left':
                self.board[empty_row][empty_col] = self.board[empty_row][empty_col-1]
                self.board[empty_row][empty_col-1] = 0
                
    def find_empty_pos(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return i, j
                
    def move(self,row,col):
        
        row -= 1
        col -= 1
        
        if row<0 or row>3 or col<0 or col>3:
            return False
        
        if row>0 and self.board[row-1][col] == 0:
            self.board[row-1][col] = self.board[row][col]
            self.board[row][col] = 0
            return True
        elif row<3 and self.board[row+1][col] == 0:
            self.board[row+1][col] = self.board[row][col]
            self.board[row][col] = 0
            return True
        elif col>0 and self.board[row][col-1] == 0:
            self.board[row][col-1] = self.board[row][col]
            self.board[row][col] = 0
            return True
        elif col<3 and self.board[row][col+1] == 0:
            self.board[row][col+1] = self.board[row][col]
            self.board[row][col] = 0
            return True
        return False
    
    def is_solved(self):
        num = 1
        for i in range(4):
            for j in range(4):
                if i==3 and j==3:
                    if self.board[i][j] != 0:
                        return False
                else:
                    if self.board[i][j] != num:
                        return False
                    num += 1
        return True
    
    def get_item(self,index):
        i,j = index
        return self.board[i][j]
    
    def __str__(self):
        s = ''
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    s += '   '
                else:
                    s += f'{self.board[i][j]:2d} '
            s += '\n'
        return s

if __name__ == "__main__":
    game = FifteenPuzzle()
    print("Start position: ")
    print(game)
    
    while not game.is_solved():
        try:
            row = int(input("Enter row (1-4): "))
            col = int(input('Enter col (1-4): '))
            if game.move(row,col):
                print('Move complited: ')
                print(game)
            else:
                print('Not correct move, try again: ')
        except ValueError:
            print('Enter only numbers!')
        except KeyboardInterrupt:
            print('\nGame stoped!')
            break
            
    if game.is_solved():
        print("Congratulations, you complite the game!")