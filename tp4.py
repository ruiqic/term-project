# Updated Animation Starter Code #from 112 website

import string
import time
import random
from tkinter import *
import tp2
import copy

#self.targetBoxPositions are the positions of the boxes to be moved by player

class Board(object):
    def __init__(self,blocks, numGoals, level):
        #create object board based on number of 3x3 block
        self.playerMoves = []
        self.playerMoveCount = 0
        self.displaySolutionIndex = None
        
        
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
        self.playerMoves = []
        
        
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
        if not self.isValidMove(direction,currentLocation):
            self.playerPosition = currentLocation
        
    def isValidMove(self,direction, currentLocation):
        (row,col) = (self.playerPosition[0],self.playerPosition[1])
        if row <0 or row > 8 or col<0 or col >8:
            return False
        if self.board[row][col] == "w":
            return False
        if [row,col] in self.boxes:
            boxNumber = self.boxes.index([row,col])
            if not self.moveBox(boxNumber, direction,currentLocation):
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
        
    def moveBox(self,boxNumber, direction, currentLocation):
        currentLocations = copy.deepcopy(self.boxes)
        self.moveBoxHelper(boxNumber, direction)
        if not self.isValidBoxMove(boxNumber, currentLocations):
            self.boxes = currentLocations
            return False
        else:
            self.playerMoveCount += 1
            self.playerMoves.append([boxNumber,direction,currentLocation[0],currentLocation[1]])
            print(self.playerMoves) #############3            
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
            
    def undoMove(self):
        if self.playerMoves == []:
            return
        self.playerMoveCount -= 1
        boxNumber = self.playerMoves[-1][0]
        direction = reverseDirection(self.playerMoves[-1][1])
        pos = self.playerMoves[-1][2:4]
        self.moveBoxHelper(boxNumber,direction)
        self.playerPosition = pos
        self.playerMoves.pop()
        
    def displaySolution(self):
        self.loadCleanBoard()
        node = self.solutionNode
        self.solution = convertNodeToReverseList(node)
        self.displaySolutionIndex = 0
        self.solutionMoves = []
        
    def displaySolutionNextMove(self):
        index = self.displaySolutionIndex
        move = self.solution[index]
        boxNumber = move[0]
        direction = move[1]
        currentPlayerPos = copy.copy(self.playerPosition)
        playerPos = copy.copy(self.boxes[boxNumber])
        self.moveBoxHelper(boxNumber,direction)
        self.playerPosition = playerPos
        self.displaySolutionIndex += 1
        self.solutionMoves.append([boxNumber,direction,currentPlayerPos[0],currentPlayerPos[1]])
        
    def displaySolutionPrevMove(self):
        if self.solutionMoves == []:
            return
        boxNumber = self.solutionMoves[-1][0]
        direction = reverseDirection(self.solutionMoves[-1][1])
        pos = self.solutionMoves[-1][2:4]
        self.moveBoxHelper(boxNumber,direction)
        self.playerPosition = pos
        self.solutionMoves.pop()
        self.displaySolutionIndex -= 1
    
    
        
def convertNodeToReverseList(node):
    if node.move == "root":
        return []
    else:
        direction = reverseDirection(node.move[1])
        return [[node.move[0],direction]] + convertNodeToReverseList(node.parent)
        
def reverseDirection(direction):
    if direction in ["Up","up"]:
        return "Down"
    elif direction in ["Down","down"]:
        return "Up"
    elif direction in ["Left","left"]:
        return "Right"
    elif direction in ["Right","right"]:
        return "Left"
        
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
        
        
        
#read and write file from 112 nots
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    importImages(data)
    data.margin = 80
    data.gridSize = 40
    data.scores = readHighscores("highscores.txt")
    data.playerName = ""
    data.mode = "startScreen"

def readHighscores(path):
    raw = readFile(path)
    highscoreList = raw.split()
    for i in range(len(highscoreList)):
        try:
            highscoreList[i] = int(highscoreList[i])
        except:
            continue
    return highscoreList

def writeHighscores(path,data):
    score = data.levelcount
    for i in range(len(data.scores)):
        try:
            if score >= data.scores[i]:
                data.scores.insert(i-1,score)
                data.scores.insert(i-1,data.playerName)
                writeHighscoresHelper(path,data)
                print(data.scores)
                return
        except:
            continue
    data.scores.extend([data.playerName,score])
    writeHighscoresHelper(path,data)
    print(data.scores)
    
def writeHighscoresHelper(path,data):
    text = ""
    for i in range(0,len(data.scores),2):
        text += data.scores[i]
        text += " " + str(data.scores[i+1]) + "\n"
    writeFile(path, text)

def importImages(data):
    data.playerImage = PhotoImage(file="player.gif")
    data.wallImage = PhotoImage(file="brick.gif")
    data.pathImage = PhotoImage(file="floor.gif")
    data.boxImage = PhotoImage(file = "box.gif")
    data.goalImage = PhotoImage(file = "goal.gif")
    data.arrowKeysImage = PhotoImage(file = "arrowKeys.gif")

def mousePressed(event, data):
    # use event.x and event.y
    if data.mode == "startScreen":
        if event.x>=data.width/2-180 and event.x<=data.width/2+180 and event.y>=data.height/3-40-10 and event.y <= data.height/3+40-10:
            data.mode = "prePlay"
        elif event.x>= data.width/2-180 and event.x <= data.width/2+180 and event.y >=3.5*data.height/6-40-10 and event.y<=3.5*data.height/6+40-10:
            data.mode = "selectLevel"
        elif event.x>= data.width/2-180 and event.x <= data.width/2+180 and event.y>=5*data.height/6-40-10 and event.y<=5*data.height/6+40-10:
            data.mode = "howToPlay"
    elif data.mode == "howToPlay":
        if event.x>=data.width/8-80 and event.x <=data.width/8+80 and event.y >= 7*data.height/8-60 and event.y <= 7*data.height/8+60:
            data.mode = "highscores"
        elif event.x >= 7*data.width/8-80 and event.x <= 7*data.width/8+80 and event.y >= 7*data.height/8-60 and event.y <= 7*data.height/8+60:
            data.mode = "tutorial"
            data.board = Board(4,1,0)
            data.levelcount =0
            data.level = data.levelcount//3
            data.stage = data.level % 3
            
        elif event.x >= 7*data.width/8-80 and event.x <= 7*data.width/8+80 and event.y >= data.height/8-60 and event.y <= data.height/8+60:
            data.mode = "startScreen"

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Escape":
        data.mode = "startScreen"
    if data.mode == "startScreen":
        if event.keysym == "1":
            data.mode = "prePlay"
            
        elif event.keysym == "2":
            data.mode = "selectLevel"
        elif event.keysym == "3":
            data.mode = "howToPlay"
            
    elif data.mode == "endGame":
        if event.keysym in string.printable:
            data.playerName += event.keysym
        elif event.keysym == "BackSpace":
            data.playerName = data.playerName[:-1]
        elif event.keysym == "Return":
            writeHighscores("highscores.txt", data)
            data.mode = "startScreen"
        
    elif data.mode == "prePlay":
        if event.keysym == "Return":
            data.levelcount = 0
            data.level = data.levelcount//3
            data.stage = data.levelcount % 3 
            data.board = Board(9,2+int(data.level*0.7),data.level+1)
            data.timeRemaining = 60
            data.mode = "play"
    
    elif data.mode == "howToPlay":
        if event.keysym == "1":
            data.mode = "highscores"
        elif event.keysym == "2":
            data.mode = "tutorial"
            data.board = Board(4,1,0)
            data.levelcount = 0
            data.level = data.levelcount//3
            data.stage = data.level % 3
    
    elif data.mode == "play":
        if event.keysym == "r":
            data.board.loadCleanBoard()
        elif event.keysym == "u":
            data.board.undoMove()
        elif event.keysym == "s":
            data.board.displaySolution()
            data.mode = "displaySolution"
        else:
            data.board.movePlayer(event.keysym)
            if data.board.isWon():
                data.mode = "between levels"
    
    elif data.mode == "tutorial":
        if event.keysym == "r":
            data.board.loadCleanBoard()
        elif event.keysym == "u":
            data.board.undoMove()
        elif event.keysym == "s":
            data.board.displaySolution()
            data.mode = "displaySolutionTutorial"
        else:
            data.board.movePlayer(event.keysym)
            if data.board.isWon():
                data.mode = "tutorialComplete"
    
    elif data.mode in ["displaySolution","displaySolutionTutorial"]:
        if event.keysym == "n":
            try:
                data.board.displaySolutionNextMove()
            except:
                if data.mode == "displaySolutionTutorial":
                    data.mode = "tutorialComplete"
                else:
                    data.mode = "endGame"
                    data.levelcount -= 1
                    data.level = data.levelcount//3
                    data.stage = data.levelcount % 3
                    
        elif event.keysym == "p":
            data.board.displaySolutionPrevMove()
                
    elif data.mode == "between levels":
        if event.keysym == "c":
            data.levelcount += 1
            data.level = data.levelcount//3
            data.stage = data.levelcount % 3
            data.board = Board(9,2+int(data.level*0.67),data.level+1)
            data.timeRemaining = 60 + data.timeRemaining//2
            data.mode = "play"
        
def timerFired(data):
    if data.mode == "play":
        data.timeRemaining-=1
        if data.timeRemaining == "0":
            data.mode = "endGame"
            data.levelcount -= 1
            data.level = data.levelcount//3
            data.stage = data.levelcount % 3
        
def redrawAll(canvas, data):
    # draw in canvas
    s = data.gridSize
    m = data.margin
    canvas.create_rectangle(0,0,data.width+10,data.height+10,fill="yellow2")
    #background +10 to overcome tkinter framing issue
    if data.mode == "startScreen":
        canvas.create_text(data.width/2,data.height/8,text = "Sokoban Puzzle", font = "fixedsys 40")
        canvas.create_rectangle(data.width/2-180,data.height/3-40-10, data.width/2+180,data.height/3+40-10, fill = "orange",width = 0)
        canvas.create_rectangle(data.width/2-180,3.5*data.height/6-40-10, data.width/2+180,3.5*data.height/6+40-10, fill = "orange",width = 0)
        canvas.create_rectangle(data.width/2-180,5*data.height/6-40-10, data.width/2+180,5*data.height/6+40-10, fill = "orange",width = 0)
        
        canvas.create_text(data.width/2+20,data.height/3-10,text = "Timed Challenge", font = "fixedsys 30")
        canvas.create_text(data.width/2+20,3.5*data.height/6-10,text = "Select Level", font = "fixedsys 30")
        canvas.create_text(data.width/2+20,5*data.height/6-10,text = "  How To Play\nand Highscores", font = "fixedsys 25")
        
        canvas.create_text(data.width/2-145,data.height/3-10,text = "(1)", font = "fixedsys 30")
        canvas.create_text(data.width/2-145,3.5*data.height/6-10,text = "(2)", font = "fixedsys 30")
        canvas.create_text(data.width/2-145,5*data.height/6-10,text = "(3)", font = "fixedsys 30")
        
        
        
        createMarginBoxesStart(canvas,data)
    
    elif data.mode == "endGame":
        if data.levelcount == -1:
            canvas.create_text(data.width/2,2*data.height/7, text = "You completed nothing!", font = "fixedsys 30")
        else:
            canvas.create_text(data.width/2,2*data.height/7, text = "You completed level %d stage %d"%(data.level+1,data.stage+1), font = "fixedsys 30")
            canvas.create_text(data.width/2,0.7*data.height/2, text = "Enter your name to record score", font = "fixedsys 30")
            canvas.create_text(data.width/2,data.height/2, text = data.playerName, font = "fixedsys 30")
            canvas.create_text(data.width/2,1.5*data.height/2, text = "Press 'Enter' to confirm name", font = "fixedsys 30")
            
        canvas.create_text(data.width/2,data.height/7, text = "Challenge Over", font = "fixedsys 40")
        canvas.create_text(data.width/2,1.3*data.height/2, text = "Press 'Esc' to return to main menu", font = "fixedsys 30")
    
    elif data.mode == "prePlay":
        canvas.create_text(data.width/2,data.height/8,text = "Timed Challenge", font = "fixedsys 40")
        t="""
        In this challenge you have 60 seconds to complete each 
        puzzle. Half of the time left over from the last
        puzzle will get added to the next level.
        
        The puzzles will get harder as you advance through the levels.
        Each level has 3 stages of similar difficulties. After 
        completing the 3 stages, you advance to the next level, 
        which will be more difficult.
        
        Get as far as you can before to timer runs to record your score!
        Using 's' to show solution will end the run, using 'r' and 'u'
        have no penalties.
        
        Press 'Enter' to begin the challenge
        """
        canvas.create_text(data.width/2,data.height/2, text = t, font = "fixedsys 21")
    
    elif data.mode == "howToPlay":
        canvas.create_rectangle(data.width/8-80,7*data.height/8-60,data.width/8+80,7*data.height/8+60, fill = "orange",width=0)
        canvas.create_rectangle(7*data.width/8-80,7*data.height/8-60,7*data.width/8+80,7*data.height/8+60, fill = "orange",width=0)
        canvas.create_text(data.width/8,7*data.height/8+20, text = "Highscores", font = "fixedsys 25")
        canvas.create_text(7*data.width/8,7*data.height/8+20, text = "Tutorial", font = "fixedsys 25")
        canvas.create_text(data.width/8,7*data.height/8-20, text = "(1)", font = "fixedsys 25")
        canvas.create_text(7*data.width/8,7*data.height/8-20, text = "(2)", font = "fixedsys 25")
        canvas.create_rectangle(7*data.width/8-80,data.height/8-60,7*data.width/8+80,data.height/8+60, fill = "orange",width=0)
        canvas.create_text(7*data.width/8,data.height/8+20, text = "Main Menu", font = "fixedsys 25")
        canvas.create_text(7*data.width/8,data.height/8-20, text = "(Esc)", font = "fixedsys 25")
        
        canvas.create_image(data.width/2,7*data.height/8-50, image = data.arrowKeysImage)
        canvas.create_text(data.width/2,7.5*data.height/8, text="Use arrow keys to move", font = "fixedsys 21")
        
        canvas.create_rectangle(data.width/4-25-20,data.height/7-25,data.width/4+25-20, data.height/7+25,fill="black")
        canvas.create_text(data.width/4-20,data.height/7, text = "S", fill = "yellow2", font = "fixedsys 40")
        canvas.create_text(data.width/4-10,2*data.height/7, text = "Press 's' to view the solution\nto the puzzle, in the Timed\nChallenge this ends the run", font = "fixedsys 21")
        
        canvas.create_rectangle(data.width/8-25,data.height/2-25-30,data.width/8+25,data.height/2+25-30, fill = "black")
        canvas.create_text(data.width/8, data.height/2-30, text = "P", font = "fixedsys 40", fill = "yellow2")
        canvas.create_rectangle(2*data.width/8-25,data.height/2-25-30,2*data.width/8+25,data.height/2+25-30, fill = "black")
        canvas.create_text(2*data.width/8, data.height/2-30, text = "N", font = "fixedsys 40", fill = "yellow2")
        canvas.create_text(data.width/4-20,4.3*data.height/7, text = "When viewing the solution\nuse the 'p' and 'n' keys\nto view the previous and\nnext steps of the puzzle", font = "fixedsys 21")
        
        canvas.create_rectangle(2.5*data.width/4-25-20,data.height/7-25,2.5*data.width/4+25-20, data.height/7+25,fill="black")
        canvas.create_text(2.5*data.width/4-20,data.height/7, text = "U", fill = "yellow2", font = "fixedsys 40")
        canvas.create_text(2.5*data.width/4-10,2*data.height/7, text = "Press 'u' to undo the last\nbox pushing move", font = "fixedsys 21")
    
        canvas.create_rectangle(7*data.width/8-35-30,data.height/2-25-30,7*data.width/8+35-30,data.height/2+25-30, fill = "black")
        canvas.create_text(7*data.width/8-30, data.height/2-30, text = "Esc", font = "fixedsys 30", fill = "yellow2")
        canvas.create_text(7*data.width/8-30, 1.3*data.height/2-30, text = "Press 'Esc' anytime to\nreturn to main menu", font = "fixedsys 21")
        
        canvas.create_rectangle(5*data.width/8-25-55,data.height/2-25-30,5*data.width/8+25-55,data.height/2+25-30, fill = "black")
        canvas.create_text(5*data.width/8-55, data.height/2-30, text = "R", font = "fixedsys 40", fill = "yellow2")
        canvas.create_text(5*data.width/8-55, 1.3*data.height/2-30, text = "Press 'r' to reset the\npuzzle to starting state", font = "fixedsys 21")
    
    elif data.mode in ["play","displaySolution","tutorial","tutorialComplete","displaySolutionTutorial"]:
        createMarginBoxes(canvas,data,s,m)
        
        if data.mode in ["play","displaySolution"]:
            canvas.create_text(6*data.width/8,data.height/8,text = "Level : %d" % (data.level+1), anchor = NW, font = "fixedsys 25")
            canvas.create_text(6*data.width/8,2*data.height/8,text = "Stage : %d" % (data.stage+1), anchor = NW, font = "fixedsys 25")
            canvas.create_text(6*data.width/8,3*data.height/8,text = "Moves : %d" % (len(data.board.playerMoves)), anchor = NW, font = "fixedsys 25")
            if data.mode == "play":
                canvas.create_text(6*data.width/8,4*data.height/8,text = "Time : %d" % (data.timeRemaining), anchor = NW, font = "fixedsys 25")
            else:
                t = """
                Showing the solution
                to the puzzle.
                
                Use 'p' and 'n'
                to move through
                the steps
                """
                numSteps = len(data.board.solution)
                index = data.board.displaySolutionIndex
                canvas.create_text(6.7*data.width/9, 5*data.height/8, text = t, font = "fixedsys 20")
                canvas.create_text(7.5*data.width/9, 7*data.height/8-30, text = "%d steps in total"%numSteps, font = "fixedsys 20")
                canvas.create_text(7.5*data.width/9, 7*data.height/8, text = "showing step %d"%index, font = "fixedsys 20")
        
        elif data.mode in ["tutorial","tutorialComplete","displaySolutionTutorial"]:
            canvas.create_image(7*data.width/9,data.height/8, image = data.wallImage)
            canvas.create_image(8*data.width/9,data.height/8, image = data.pathImage)
            canvas.create_text(7*data.width/9,data.height/8+30, text = "wall", font = "fixedsys 15")
            canvas.create_text(8*data.width/9,data.height/8+30, text = "pathway", font = "fixedsys 15")
            canvas.create_image(7*data.width/9,2*data.height/8, image = data.boxImage)
            canvas.create_image(8*data.width/9,2*data.height/8, image = data.goalImage)
            canvas.create_text(7*data.width/9,2*data.height/8+30, text = "box", font = "fixedsys 15")
            canvas.create_text(8*data.width/9,2*data.height/8+30, text = "goal", font = "fixedsys 15")
            if data.mode == "displaySolutionTutorial":
                t = """
                Showing the solution
                to the puzzle.
                
                Use 'p' and 'n'
                to move through
                the steps
                """
                numSteps = len(data.board.solution)
                index = data.board.displaySolutionIndex
                canvas.create_text(6.7*data.width/9, 4*data.height/8, text = t, font = "fixedsys 20")
                canvas.create_text(7.5*data.width/9, 6*data.height/8, text = "%d steps in total"%numSteps, font = "fixedsys 20")
                canvas.create_text(7.5*data.width/9, 6*data.height/8+30, text = "showing step %d"%index, font = "fixedsys 20")
                
            else:
                t = """
                The player and the box
                can only be on pathways
                or goals.
                
                The goal of the puzzle
                is to push all the boxes
                onto the goals.
                
                A box can only be pushed
                if there is a pathway or
                goal block behind it.
                
                Boxes can not be pushed
                if a wall or another box
                is blocking the way.
                """
                canvas.create_text(6.7*data.width/9, 5*data.height/8, text = t, font = "fixedsys 15")
        
        
        for row in range(len(data.board.board)):
            for col in range(len(data.board.board[0])):
                if data.board.board[row][col]== "p":
                    canvas.create_image(m+col*s,m+row*s, image=data.pathImage,
                    anchor = NW)
                elif data.board.board[row][col] == "w":
                    canvas.create_image(m+col*s,m+row*s, image=data.wallImage,
                    anchor = NW)
                elif data.board.board[row][col] == "g":
                    canvas.create_image(m+col*s,m+row*s, image=data.goalImage,
                    anchor = NW)
        for box in data.board.boxes:
            if box == None:
                continue
            canvas.create_image(m+box[1]*s, m+box[0]*s, image=data.boxImage,
            anchor = NW)
            
        canvas.create_image(m+data.board.playerPosition[1]*s, m+data.board.playerPosition[0]*s,
        image=data.playerImage, anchor=NW)
        
        if data.mode == "tutorialComplete":
            canvas.create_rectangle(data.width/2-150,data.height/2-75,data.width/2+150,data.height/2+75, fill = "black")
            canvas.create_text(data.width/2,data.height/2, text = "You completed the tutorial puzzle!\nPress 'Esc' to return to main menu", font = "fixedsys 10", fill = "yellow2")
    
    elif data.mode == "between levels":
        canvas.create_text(data.width/2,data.height/7, text = "Level %d Stage %d complete"%(data.level+1,data.stage+1), font = "fixedsys 40")
        canvas.create_text(data.width/2,0.7*data.height/2, text = "Press 'c' to continue", font = "fixedsys 40")
        canvas.create_text(data.width/2,1.3*data.height/2, text = "      %d seconds remained\nadding %d seconds to next level"%(data.timeRemaining,data.timeRemaining//2), font = "fixedsys 30")
        
        
    # elif data.mode == "loading":
    #     canvas.create_text(210,210, text = "Loading...", font = "Arial 15 bold")

def createMarginBoxes(canvas,data,s,m):
    m = m - 40 # one block less
    for row in range(11):
        for col in range(11):
            if row==0 or col == 0 or row == 10 or col == 10:
                    canvas.create_image(m+col*s,m+row*s, image=data.wallImage,
                    anchor = NW)

def createMarginBoxesStart(canvas,data):
    s=40
    for row in range(14):
        for col in range(19):
            if row in [0,12,13] or col in [0,1,2,15,16,17,18]:
                    canvas.create_image(col*s,row*s, image=data.wallImage,
                    anchor = NW)



                
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
    data.timerDelay = 1000 # milliseconds
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

run(720, 520)