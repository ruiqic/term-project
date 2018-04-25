# Updated Animation Starter Code #from 112 website

import random
from tkinter import *
import tp2
import copy

#self.targetBoxPositions are the positions of the boxes to be moved by player

class Board(object):
    def __init__(self,blocks, numGoals, level):
        #create object board based on number of 3x3 block
        self.blocksParameter = blocks
        self.numGoalsParameter = numGoals
        self.levelParameter = level
        self.boxesMoved = [False]*numGoals #keeps the status of moved boxes
        
        self.difficulty = level*10 + 11 #determine difficulty based on level
        self.board = tp2.createBoard(blocks)
        self.cleanBoard = copy.deepcopy(self.board)
        
        self.placeBoxes(numGoals)
        self.setupStartingGoals()
        self.setupBoard(0)
        self.placePlayer() #place player on the board
        self.saveCleanBoard()
        
    def loadCleanBoard(self):
        self.boxes = self.cleanBoxes
        self.playerPosition = self.cleanPlayerPosition
        self.saveCleanBoard()
        
        
    def saveCleanBoard(self):
        self.cleanBoxes = copy.deepcopy(self.boxes)
        self.cleanPlayerPosition = copy.copy(self.playerPosition)
    
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
    
    def setupBoard(self, tryNewGoalsCount):
        helperBoard = copy.deepcopy(self.board)
        for row in range(9):
            for col in range(9):
                if helperBoard[row][col] == "g":
                    helperBoard[row][col] = "b"
        helperBoxes = copy.deepcopy(self.boxes)
        root = Root()
        self.moveSet = set()
        self.tree = {} #box positions mapping to difficulty
        self.nodeDict = {} #box positions mapping to easiest move node
        
        self.tree[root] = 0
        self.getPossibleBoards(helperBoard,root,helperBoxes)
        print(self.tree)
        self.targetBoxPositions = None
        for boxPositions in self.tree:
            if self.tree[boxPositions] <= self.difficulty and (
            self.tree[boxPositions] > (self.difficulty - 10)):
                print(self.boxes, boxPositions, self.tree[boxPositions])
                
                self.solutionNode = self.nodeDict[makeTuple(boxPositions)]
                
                self.targetBoxPositions = self.removeUnmovedBoxes(boxPositions)                    
                
                self.goals = self.boxes #save the locations of goals
                
                self.boxes = self.targetBoxPositions
                
                print(self.solutionNode)#######
                print(self.targetBoxPositions)#########
                print(self.goals)
                break
                
        if self.targetBoxPositions == None:
            blocks = self.blocksParameter
            numGoals = self.numGoalsParameter 
            level = self.levelParameter 
            if tryNewGoalsCount < 10:
                print("trying new goal positions") ##########
                self.board = copy.deepcopy(self.cleanBoard)
                self.placeBoxes(numGoals)
                self.setupStartingGoals()
                self.setupBoard(tryNewGoalsCount+1)
            else:
                print("remaking board") ##############
                self.__init__(blocks, numGoals,level)
            #remake
        
    def removeUnmovedBoxes(self, boxPositions):
        boxPositions = makeList(boxPositions)
        removeList = copy.deepcopy(boxPositions)
        indexSet = set(str(self.solutionNode))
        for i in range(len(self.boxes)):
            if str(i) not in indexSet:
                removeList[i] = None####maybe self.boxes?
                self.board[self.boxes[i][0]][self.boxes[i][1]] = "w"
        return removeList
    
    # def removeSameBoxes(self, boxPositions):
    #     boxPositions = makeList(boxPositions)
    #     removeList = copy.deepcopy(boxPositions)
    #     for i in range(len(self.boxes)):
    #         if self.boxes[i] == boxPositions[i]:
    #             removeList.remove(self.boxes[i])
    #             self.board[self.boxes[i][0]][self.boxes[i][1]] = "w"
    #     return removeList

    def getPossibleBoards(self,board,currentNode, boxes):
        for direction in ["up","down","left","right"]:
            for i in range(len(boxes)):
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
                        
                        
                        if (tupleBoxes in self.tree and (self.tree[tupleBoxes] >
                        newNode.difficulty)):
                            self.tree[tupleBoxes] = newNode.difficulty
                            self.nodeDict[tupleBoxes] = newNode
                        elif tupleBoxes not in self.tree:
                            self.tree[tupleBoxes] = newNode.difficulty
                            self.nodeDict[tupleBoxes] = newNode
                            self.getPossibleBoards(currentBoard,newNode,currentBoxes)
                  
    def isWon(self):
        for box in self.boxes:
            if box != None and self.board[box[0]][box[1]] != "g":
                return False
        return True
            
    def placePlayer(self):
        self.playerPosition = None
        move = self.solutionNode.move #[boxNumber, direction]
        boxes = self.targetBoxPositions
        helperBoard = copy.deepcopy(self.board)
        for box in boxes:
            if box == None:
                continue
            helperBoard[box[0]][box[1]] = "w"
        trow = boxes[move[0]][0] #temporary
        tcol = boxes[move[0]][1]
        direction = move[1]
        (row,col) = connectedHelper(trow, tcol, direction)
        tp2.floodFill(helperBoard, row, col)
        while self.playerPosition == None:
            randRow = random.randint(0,8)
            randCol = random.randint(0,8)
            if helperBoard[randRow][randCol] == "f" and [randRow,randCol] not in boxes:
                self.playerPosition = [randRow,randCol]
        
    def movePlayer(self,direction): #passing in event.keysym
        currentLocation = copy.copy(self.playerPosition)
        self.movePlayerHelper(direction)
        if not self.isValidMove(direction):
            self.playerPosition = currentLocation
        
    def isValidMove(self,direction):
        (row,col) = (self.playerPosition[0],self.playerPosition[1])
        if row <0 or row > 8 or col<0 or col >8:
            return False
        if self.board[row][col] == "w":
            return False
        if [row,col] in self.boxes:
            boxNumber = self.boxes.index([row,col])
            if not self.moveBox(boxNumber, direction):
                return False
        return True
    
    def movePlayerHelper(self,direction): #passing in event.keysym
        if direction == "Up":
            self.playerPosition[0] -=1
        elif direction == "Down":
            self.playerPosition[0] +=1
        elif direction == "Left":
            self.playerPosition[1] -= 1
        elif direction == "Right":
            self.playerPosition[1] += 1
        
    def moveBox(self,boxNumber, direction):
        
        currentLocations = copy.deepcopy(self.boxes)
        self.moveBoxHelper(boxNumber, direction)
        if not self.isValidBoxMove(boxNumber, currentLocations):
            self.boxes = currentLocations
            return False
        return True
    
    def isValidBoxMove(self,boxNumber, currentLocations):
        (row,col) = (self.boxes[boxNumber][0],self.boxes[boxNumber][1])
        if row <0 or row > 8 or col<0 or col >8:
            return False
        if self.board[row][col] == "w":
            return False
        if [row,col] in currentLocations:
            return False
        return True
        
    def moveBoxHelper(self, boxNumber, direction):
        if direction == "Up":
            self.boxes[boxNumber][0] -=1
        elif direction == "Down":
            self.boxes[boxNumber][0] +=1
        elif direction == "Left":
            self.boxes[boxNumber][1] -= 1
        elif direction == "Right":
            self.boxes[boxNumber][1] += 1
        
def twoPointsConnected(currentNode, newNode, boxes, board ):
    if currentNode.move == "root":
        return True #root always true
    currentDir = currentNode.move[1]
    newDir = newNode.move[1]
    (currentRow, currentCol) = tuple(boxes[currentNode.move[0]])
    (newRow, newCol) = tuple(boxes[newNode.move[0]])
    (currentRow, currentCol) = connectedHelper(currentRow,currentCol,currentDir)
    (newRow, newCol) = connectedHelper(newRow, newCol, newDir)
    if (currentRow,currentCol) == (newRow,newCol): #connected if same block
        return True
    return arePointsConnected(currentRow, currentCol, newRow, newCol, board)
    
def arePointsConnected(currentRow, currentCol, newRow, newCol, board):
    b = copy.deepcopy(board)
    tp2.floodFill(b,currentRow,currentCol)
    if b[newRow][newCol] == "f":
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
        self.difficulty = 0
        if self.parent.move == "root":
            self.difficulty = self.parent.difficulty + 1
        else:
            if self.parent.move[0] != self.move[0]:
                self.difficulty = self.parent.difficulty + 3
            elif self.parent.move[1] != self.move[1]:
                self.difficulty = self.parent.difficulty + 2
            else:
                self.difficulty = self.parent.difficulty
                
        # if self.level > 1:
        #     if (self.move == self.parent.move):
        #         self.difficulty -= 1
        
        # if self.level > 3:
        #     if self.parent.parent.parent.move[0]
        # 
        if self.level > 1 and self.move[0] == self.parent.move[0]:
            if (sorted(self.parent.move[1] + self.move[1]) == 
            ['d', 'n', 'o', 'p', 'u', 'w']) or (sorted(self.parent.move[1] + 
            self.move[1]) == ['e', 'f', 'g', 'h', 'i', 'l', 'r', 't', 't']):
                self.difficulty -= 2
    
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
    
    data.levelcount = 0
    data.level = data.levelcount//3
    data.stage = data.level % 3
    
    data.board = Board(9,2+int(data.level+0.5),data.level+1)
    data.mode = "play"


def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.mode == "play":
        if event.keysym == "r":
            data.board.loadCleanBoard()
        else:
            data.board.movePlayer(event.keysym)
            if data.board.isWon():
                data.mode = "between levels"
    
    if data.mode == "between levels":
        if event.keysym == "c":
            data.levelcount += 1
            data.level = data.levelcount//3
            data.stage = data.level % 3
            data.board = Board(9,2+int(data.level*0.67),data.level+1)
            data.mode = "play"
        
def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    s = data.gridSize
    m = data.margin
    if data.mode == "play":
        canvas.create_text(0,0,text = "level : %d" % (data.level+1), anchor = NW)
        canvas.create_text(420,0,text = "stage : %d" % (data.stage+1), anchor = NE)
        
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
        for box in data.board.boxes:
            if box == None:
                continue
            canvas.create_oval(m+box[1]*s, m+box[0]*s, m+(box[1]+1)*s,
            m+(box[0]+1)*s, fill = "green")
            
        canvas.create_oval(m+data.board.playerPosition[1]*s, m+data.board.playerPosition[0]*s,
        m+(data.board.playerPosition[1]+1)*s,m+(data.board.playerPosition[0]+1)*s, fill = "yellow")
    
    elif data.mode == "between levels":
        canvas.create_text(210,210, text = "Press 'c' to continue", font = "Arial 15 bold")
        
    # elif data.mode == "loading":
    #     canvas.create_text(210,210, text = "Loading...", font = "Arial 15 bold")
             
                
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