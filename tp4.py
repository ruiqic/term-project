# Updated Animation Starter Code

import random
from tkinter import *
import tp2

class Board(object):
    def __init__(self,blocks):#create object board based on number of 3x3 block
        self.board = tp2.createBoard(blocks)
        
    def placeGoals(self, numBoxes):
        self.goals = []
        while numBoxes >0:
            randRow = random.randint(0,8)
            randCol = random.randint(0,8)
            if self.board[randRow][randCol] == "p" and \
            [randRow,randCol] not in self.goals:
                self.goals.append([randRow,randCol])
                numBoxes -= 1
    
    def setupStartingBoxes(self):
        for goal in self.goals:
             self.board[goal[0]][goal[1]] = "b"
        
        
        
        
        
def twoEmptySpace(board, row, col, direction):
    if direction == "up":
        if row > 1 and board[row-1][col] == board[row-2][col] == "p":
            return True
    elif direction == "down":
        if row < 7 and board[row+1][col] == board[row+2][col] == "p":
            return True
    elif direction == "left":
        if col > 1 and board[row][col-1] == board[row][col-2] == "p":
            return True
    elif direction == "right":
        if col < 7 and board[row][col+1] == board[row][col+2] == "p":
            return True
    return False
        
        
        
        
        
        
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.margin = 30
    data.gridSize = 40
    data.board = Board(9)
    data.board.placeGoals(3)

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    s = data.gridSize
    m = data.margin
    for row in range(len(data.board.board)):
        for col in range(len(data.board.board[0])):
            if data.board.board[row][col]== "p":
                color = "gray"
            elif data.board.board[row][col] == "w":
                color = "brown"
            canvas.create_rectangle(m+col*s, m+row*s,
            m+(col+1)*s, m+(row+1)*s, fill = color)
    for goal in data.board.goals:
        canvas.create_oval(m+goal[1]*s, m+goal[0]*s, m+(goal[1]+1)*s,
        m+(goal[0]+1)*s, fill = "green")


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(420, 420)