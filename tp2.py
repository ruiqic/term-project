import random
import copy
    # "p" is pathway
    # "w" is wall
    #None is no restriction for the outside
    #to do
    # convert board to 2d list and make graphics

def templates():
    A = [[None,None,None,None,None],
         [None, "p", "p", "p",None],
         [None, "p", "p", "p",None],
         [None, "p", "p", "p",None],
         [None,None,None,None,None]]
         
    B = [[None,None,None,None,None],
         [None, "w", "w", "w",None],
         [None, "w", "p", "p",None],
         [None, "w", "p", "p",None],
         [None,None,None,None,None]]
        
    C = [[None,None, "p",None,None],
         [None, "w", "p", "w",None],
         [ "p", "p", "p", "p", "p"],
         [None, "w", "p", "w",None],
         [None,None, "p",None,None]]     
         
    D = [[None,None,None,None,None],
         [None, "w", "w", "w",None],
         [None, "w", "w", "w",None],
         [None, "w", "w", "w",None],
         [None,None,None,None,None]]
         
    E = [[None,None,None,None,None],
         [None, "w", "w", "w",None],
         [ "p", "p", "w", "p", "p"],
         [None, "p", "p", "p",None],
         [None, "p", "p",None,None]]
         
    F = [[None,None,None,None,None],
         [None, "w", "p", "p",None],
         [None, "p", "p", "p",None],
         [None, "p", "p", "p",None],
         [None,None,None,None,None]]
         
    G = [[None,None, "p",None,None],
         [None, "w", "p", "p",None],
         [ "p", "p", "p", "p",None],
         [None, "p", "p", "w",None],
         [None,None,None,None,None]]
         
    H = [[None,None, "p",None,None],
         [None, "w", "p", "w",None],
         [None, "w", "p", "p", "p"],
         [None, "w", "w", "w",None],
         [None,None,None,None,None]]
         
    I = [[None,None,None,None,None],
         [None, "w", "w", "w",None],
         [None, "w", "p", "p",None],
         [ "p", "p", "p", "p",None],
         [ "p", "p",None,None,None]]
         
    J = [[None,None,None, "p", "p"],
         [None, "w", "w", "p", "p"],
         [None, "p", "p", "p",None],
         [None, "p", "p", "p",None],
         [None,None,None,None,None]]
        
    K = [[None,None,None,None,None],
         [None, "w", "p", "p",None],
         [ "p", "p", "p", "p",None],
         [None, "w", "p", "p",None],
         [None,None,None,None,None]]
        
    L = [[None,None,None,None,None],
         [None, "w", "w", "w",None],
         [ "p", "p", "p", "p", "p"],
         [None, "w", "w", "w",None],
         [None,None,None,None,None]]    
    
    M = [[None, "p",None, "p",None],
         [None, "p", "p", "p",None],
         [None, "w", "p", "w",None],
         [None, "p", "p", "p",None],
         [None, "p",None, "p",None]]
    
    N = [[None,None,None,None,None],
         [None, "w", "w", "w",None],
         [None, "p", "p", "p",None],
         [None, "p", "p", "p",None],
         [None,None,None,None,None]]
         
    O = [[None,None, "p",None,None],
         [None, "w", "p", "p",None],
         [ "p", "p", "p", "p",None],
         [None, "w", "p", "w",None],
         [None,None, "p",None,None]]
    
    P = [[None,None,None,None,None],
         [None, "p", "p", "p", "p"],
         [None, "p", "w", "p", "p"],
         [None, "p", "p", "p",None],
         [None,None,None,None,None]]
    
    Q = [[None,None,None,None,None],
         [None, "w", "w", "w",None],
         [None, "w", "w", "w",None],
         [None, "p", "p", "p",None],
         [None, "p", "p", "p",None]]
    
    return [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q]

def createBoard(blocks = 9):
    board = [0]*9
    
    pieces = templates()
    if blocks == 2:
        for i in range(7):
            board[i] = pieces[3]
        
    elif blocks == 4:
        board[0]= pieces[3]
        board[1]= pieces[3]
        board[2]= pieces[3]
        board[3]= pieces[3]
        board[6]= pieces[3]
        
    elif blocks == 6:
        for i in range(3):
            board[i] = pieces[3]
    
    
    while nthPiece(board) != None:
        print(nthPiece(board))
        nextPiece = findNextPiece(board, pieces)
        board[nthPiece(board)] = nextPiece
    
    completeBoard = assembleBoard(board)
    if not isConnected(completeBoard):
        return createBoard(blocks)
        
    if hasFourByThree(completeBoard):
        return createBoard(blocks)
        
    return completeBoard
            
        
def hasFourByThree(board): #check if there is 4 by 3 empty space
    #horizontal
    for row in range(7):
        for col in range(6):
            total = 0
            for drow in range(3):
                for dcol in range(4):
                    if board[drow+row][dcol+col] == "p":
                        total += 1
            if total == 12:
                return True
    #vertical
    for row in range(6):
        for col in range(7):
            total = 0
            for drow in range(4):
                for dcol in range(3):
                    if board[drow+row][dcol+col] == "p":
                        total += 1
            if total == 12:
                return True
    return False

def isConnected(board):
    b = copy.deepcopy(board)    
    filled = False    
    for row in range(9):
        for col in range(9):
            if b[row][col] == "p" and not filled: #only fill once
                filled = True
                floodFill(b,row,col)
    if not filled:
        return False # full board of walls to begin with, remake board
        
    for row in range(9): #check for path after floodfill once
        for col in range(9):
            if b[row][col] == "p":
                return False
    return True
    
def floodFill(board, row, col): #got general framework from 112 website
    if row <0 or row > 8 or col<0 or col >8:
        return #off board
    if board[row][col] in ["w","b","f"]:
        return
    board[row][col] = "f" 
    floodFill(board, row+1,col)
    floodFill(board, row-1, col)
    floodFill(board, row, col+1)
    floodFill(board, row, col-1)
    

def assembleBoard(board): #make from linear (with None) list to 2d grid
    newBoard =[]
    for row in range(9):
        newBoard.append([0]*9)
    for i in range(len(board)):
        dc = int(i%3)
        dr = int(i//3)
        for row in range(1,4):
            for col in range(1,4):
                newBoard[row-1+3*dr][col-1+3*dc] = board[i][row][col]
    return newBoard
                
                
                
def findNextPiece(board, pieces): #find next valid piece for the board
    random.shuffle(pieces)
    nextPiece = None
    while nextPiece == None:
        for piece in pieces:
            #print(board,nthPiece(board),"next piece")
            randomRotatedPieces = rotate(piece)
            random.shuffle(randomRotatedPieces)
            for randomRotatedPiece in randomRotatedPieces:
                
                if isValidPlacement(board, randomRotatedPiece):
                    nextPiece = randomRotatedPiece
                    break
            if nextPiece != None:
                break
                
    return nextPiece
        
def rotate(template): #returns all 4 rotated versions of template piece
    result = []
    for j in range(4):
        rotated = []
        for i in range(5):
            rotated.append([None]*5)
        for row in range(5):
            for col in range(5):
                rotated[4- col][row] = template[row][col]
        result.append(rotated)
        template = copy.deepcopy(rotated)
    return result
    
def nthPiece(board):
    for i in range(9):
        if board[i] == 0:
            return i
    print("complete board")
    return None
    
    
#check border and diagonal

def isValidPlacement(board, template):
    n = nthPiece(board) #which section of the board is being added
    if not isCompatibleBorder(board,template, n):
        return  False
    if n in [3,4,6,7]:
        topRight = board[n-2]
        if not isCompatibleTopRight(topRight, template):
            return False
    if n in [4,5,7,8]:
        diagTemplate = board[n-4]
        if not isCompatibleDiag(diagTemplate,template):
            return False
    if n in [1,2,4,5,7,8]: #check if adding to the right is compatible
        prevTemplate = board[n-1]
        if not isCompatibleRight(prevTemplate, template):
            return False
    if n in [3,4,5,6,7,8]: #check if adding to the bottom is compatible
        upTemplate = board[n-3]
        if not isCompatibleDown(upTemplate, template):
            return False
    return True
    
def isCompatibleRight(prevTemplate, template):
    #print("checking right")
    for row in range(1,4):
        if template[row][0] == None:
            continue
        else:
            if template[row][0] != prevTemplate[row][3]:
                return False
    for row in range(1,4):
        if prevTemplate[row][4] == None:
            continue
        else:
            if prevTemplate[row][4] != template[row][1]:
                return False
    return True
    
def isCompatibleDown(upTemplate, template):
    for col in range(1,4):
        if template[0][col] == None:
            continue
        else:
            if template[0][col] != upTemplate[3][col]:
                return False
    for col in range(1,4):
        if upTemplate[4][col] == None:
            continue
        else:
            if upTemplate[4][col] != template[1][col]:
                return False
    return True

def isCompatibleDiag(diagTemplate, template):
    return (template[0][0] == None or diagTemplate[3][3] == template[0][0])\
    and (diagTemplate[4][4] == None or diagTemplate[4][4] == template[1][1])
            
            
def isCompatibleTopRight(topRight, template):
    return (template[0][4] == None or topRight[3][1] == template[0][4])\
    and (topRight[4][0] == None or topRight[4][0] == template[1][3])
    
def isCompatibleBorder(board,template, n): #border should be walls
    if n in [0,1,2]:
        for col in range(5):
            if template[0][col] == "p":
                return False
    if n in [6,7,8]:
        for col in range(5):
            if template[4][col] == "p":
                return False
    if n in [0,3,6]:
        for row in range(5):
            if template[row][0] == "p":
                return False
    if n in [2,5,8]:
        for row in range(5):
            if template[row][4] == "p":
                return False
    return True

























