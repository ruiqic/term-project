# Updated Animation Starter Code #from 112 website

import random
from tkinter import *
import tp2
import copy

class Board(object):
    def __init__(self,blocks, numGoals, level):
        #create object board based on number of 3x3 block
        self.blocksParameter = blocks
        self.numGoalsParameter = numGoals
        self.levelParameter = level
        
        self.difficulty = level*10 + 20 #determine difficulty based on level
        self.board = tp2.createBoard(blocks)
        self.placeBoxes(numGoals)
        self.setupStartingGoals()
        self.setupBoard()
        
    def placeBoxes(self, numBoxes):
        self.boxes = []
        while numBoxes >0:
            randRow = random.randint(0,8)
            randCol = random.randint(0,8)
            if self.board[randRow][randCol] == "p" and \
            [randRow,randCol] not in self.boxes:
                self.boxes.append([randRow,randCol]) #list [row,col]
                numBoxes -= 1
    
    def setupStartingGoals(self):
        for goal in self.boxes:
             self.board[goal[0]][goal[1]] = "g"
        
    def moveBox(self, boxNumber, direction):
        if direction == "up":
            self.boxes[boxNumber][0] -=1
        elif direction == "down":
            self.boxes[boxNumber][0] +=1
        elif direction == "left":
            self.boxes[boxNumber][1] -= 1
        elif direction == "right":
            self.boxes[boxNumber][1] += 1
    
    def setupBoard(self):
        helperBoard = copy.deepcopy(self.board)
        for row in range(9):
            for col in range(9):
                if helperBoard[row][col] == "g":
                    helperBoard[row][col] = "b"
        helperBoxes = copy.deepcopy(self.boxes)
        root = Root()
        self.moveSet = set()
        self.tree = {}
        self.tree[root] = 0
        self.getPossibleBoards(helperBoard,root,helperBoxes)
        print(self.tree)
        self.targetBoxPositions = None
        for boxPositions in self.tree:
            if self.tree[boxPositions] <= self.difficulty and (
            self.tree[boxPositions] > (self.difficulty - 10)):
                print(self.boxes, boxPositions, self.tree[boxPositions])
                if self.areSameBoxes(boxPositions):
                    continue
                        
                self.targetBoxPositions = makeList(boxPositions)
                print(self.targetBoxPositions, "set to", boxPositions)
                break
                
        if self.targetBoxPositions == None:
            print("remaking board")
            blocks = self.blocksParameter
            numGoals = self.numGoalsParameter 
            level = self.levelParameter 
            self.__init__(blocks, numGoals,level)
            #remake
        
    def areSameBoxes(self, boxPositions):
        boxPositions = makeList(boxPositions)
        for i in range(len(self.boxes)):
            if self.boxes[i] in boxPositions:
                return True
        return False

    def getPossibleBoards(self,board,currentNode, boxes):
        for i in range(len(boxes)):
            for direction in ["up","down","left","right"]:
                row = boxes[i][0]
                col = boxes[i][1]
                newNode = Node([i,direction],currentNode)
                
                if (twoEmptySpace(board, row, col, direction, boxes) and
                twoPointsConnected(currentNode, newNode, boxes, board)):
                #and path connected
                    move = (i,row,col,direction)
                    if move not in self.moveSet:
                        self.moveSet.add(move)
                        
                        currentBoard = moveHelperBoard(board,row,col,direction)
                        
                        currentBoxes = moveHelperBox(boxes, i, direction)
                        
                        tupleBoxes = makeTuple(currentBoxes)
                        
                        if tupleBoxes not in self.tree or (tupleBoxes in 
                        self.tree and (self.tree[tupleBoxes] >
                        newNode.difficulty)):
                            self.tree[tupleBoxes] = newNode.difficulty
                        
                        self.getPossibleBoards(currentBoard,newNode,currentBoxes)
        
def twoPointsConnected(currentNode, newNode, boxes, board ):
    if currentNode.move == "root":
        return True #root always true
    currentDir = currentNode.move[1]
    newDir = newNode.move[1]
    (currentRow, currentCol) = tuple(boxes[currentNode.move[0]])
    (newRow, newCol) = tuple(boxes[newNode.move[0]])
    (currentRow, currentCol) = connectedHelper(currentRow,currentCol,currentDir)
    (newRow, newCol) = connectedHelper(newRow, newCol, newDir)
    return arePointsConnected(currentRow, currentCol, newRow, newCol, board)
    
def arePointsConnected(currentRow, currentCol, newRow, newCol, board):
    b = copy.deepcopy(board)
    tp2.floodFill(b,currentRow,currentCol)
    if b[newRow][newCol] == "w":
        return True
    return False


    
    
def connectedHelper(row, col, direction):
    if direction == "up":
        return (row-1,col)
    elif direction == "down":
        return (row+1,col)
    elif direction == "left":
        return (row,col-1)
    else:
        return (row, col+1)


def makeTuple(list2d):
    l = []
    for element in list2d:
        l.append(tuple(element))
    return tuple(l)

def makeList(tuple2d):
    l = []
    for element in tuple2d:
        l.append(list(element))
    return l

def moveHelperBoard(board, row, col, direction):
    newBoard = copy.deepcopy(board)
    newBoard[row][col] = "p"
    if direction == "up":
        newBoard[row-1][col] = "b"
    elif direction == "down":
        newBoard[row+1][col] = "b"
    elif direction == "left":
        newBoard[row][col-1] = "b"
    elif direction == "right":
        newBoard[row][col+1] = "b"
    return newBoard

def moveHelperBox(boxes, boxNumber, direction):
    newBoxes = copy.deepcopy(boxes)
    if direction == "up":
        newBoxes[boxNumber][0] -=1
    elif direction == "down":
        newBoxes[boxNumber][0] +=1
    elif direction == "left":
        newBoxes[boxNumber][1] -= 1
    elif direction == "right":
        newBoxes[boxNumber][1] += 1
    return newBoxes
    
    
    
class Node(object):
    def __init__(self, move, parent):
        #move = [boxNumber, direction]
        self.parent = parent
        self.move = move
        self.level = self.parent.level + 1
        if self.parent.move == "root":
            self.difficulty = 1
        else:
            if self.parent.move[0] != self.move[0]:
                self.difficulty = self.parent.difficulty + 3
            elif self.parent.move[1] != self.move[1]:
                self.difficulty = self.parent.difficulty + 2
            else:
                self.difficulty = self.parent.difficulty + 1
                
        if self.level > 2:
            if (self.parent.parent.move == self.move == self.parent.move):
                self.difficulty -= 1
        
        # if self.level > 3:
        #     if self.parent.parent.parent.move[0]
        # 
        # if self.level > 1 and self.move[0] == self.parent.move[0]:
        #     if sorted(self.parent.move[1] + self.move[1]) == 
        #     ['d', 'n', 'o', 'p', 'u', 'w']) or (sorted(self.parent.move[1] + 
        #     self.move[1]) == ['e', 'f', 'g', 'h', 'i', 'l', 'r', 't', 't']):
        #         self.difficulty -= 2
    
    def __repr__(self):
        if self.move == "root":
            return self.move
            
        else:
            result = str(self.move[0]) + "," + str(self.move[1])
            return str(self.parent) + "/" + result
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return str(self) == str(other)
    
class Root(Node):
    def __init__(self):
        self.parent = "None"
        self.level = 0
        self.difficulty = 0
        self.move = "root"
        
        
        
def twoEmptySpace(board, row, col, direction, boxes):
    if direction == "up":#check if there is path of goal space and no box in way
        if row > 1 and (board[row-1][col] in ["p","g"] and board[row-2][col]  
        in ["p","g"]) and ([row-1,col] 
        not in boxes and [row-2,col] not in boxes):
            return True
    elif direction == "down":
        if row < 7 and (board[row+1][col] in ["p","g"] and board[row+2][col]
        in ["g","p"]) and ([row-1,col] 
        not in boxes and [row-2,col] not in boxes):
            return True
    elif direction == "left":
        if col > 1 and (board[row][col-1] in ["p","g"] and board[row][col-2]  
        in ["p","g"]) and ([row,col-1] 
        not in boxes and [row,col-2] not in boxes):
            return True
    elif direction == "right":
        if col < 7 and (board[row][col+1] in ["p","g"] and board[row][col+2] 
        in ["p","g"]) and ([row,col+1]
        not in boxes and [row,col+2] not in boxes):
            return True
    return False
        
        
        
        
        
        
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.margin = 30
    data.gridSize = 40
    data.board = Board(9,3,2)
    data.level = 1


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
            elif data.board.board[row][col] == "g":
                color = "blue"
            canvas.create_rectangle(m+col*s, m+row*s,
            m+(col+1)*s, m+(row+1)*s, fill = color)
    for box in data.board.targetBoxPositions:
        canvas.create_oval(m+box[1]*s, m+box[0]*s, m+(box[1]+1)*s,
        m+(box[0]+1)*s, fill = "green")
        
                
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