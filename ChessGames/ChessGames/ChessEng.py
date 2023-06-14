# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 21:07:34 2021

@author: Aqsa

Chess Dictonary:
    https://en.wikipedia.org/wiki/Glossary_of_chess
Chess game AI info:
    https://medium.com/the-innovation/the-anatomy-of-a-chess-ai-2087d0d565
Chess moves algorithm:
    https://www.cs.cornell.edu/boom/2004sp/ProjectArch/Chess/algorithms.html
Knight Movement Error:
    https://tutorialspoint.dev/data-structure/matrix-archives/possible-moves-knight
Fixed Key Error 6 on line 70 Reference:
https://stackoverflow.com/questions/61179695/this-python-script-returns-keyerror-6-and-i-dont-know-why    

Thought processing notes:
    
both self and this are used for the same thing.
They are used to access the variable associated with the current instance.
Only difference is,have to include self explicitly as first parameter to
an instance method in Python, whereas this is not the case with Java

pawns need a bunch of if statements (also gotta work on pawn promotion)

algoirthm for rook bishop and Queen is same with different coordinates of the board
traversing the board using 2 loops for row and column
keeping check of opponents piece and capturing it.

Knight needs 1 loop since it will not be traversing the whole board its movements
king and knight will have similar codes and
are stricted to an L and sq shape like pawns are restricted to moving forward and capturing
diagonally

To save king from check gotta keep track of king's moves

Pawn Promoion: row 0 and row 7
changes need to be made in move class i guess to track and store info

"""


class GameFrameWork:
    #this class is responisble for storing all the data of the chess game
    #also responsible for checking whether the moves are valid or not of the chess game
    def __init__(self):
        #base of the chess board inside the constructor as a 2D list
        #a list of lists with list representing 1 on the 8 rows on a chess board
        #the names of the squares allow us to parse strings and check
        #against image name and show on screen
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],  #black side of the board
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["EE", "EE", "EE", "EE", "EE", "EE", "EE", "EE"],  #empty spaces
            ["EE", "EE", "EE", "EE", "EE", "EE", "EE", "EE"], #will help us in the backend manipulation of the code
            ["EE", "EE", "EE", "EE", "EE", "EE", "EE", "EE"],
            ["EE", "EE", "EE", "EE", "EE", "EE", "EE", "EE"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ] #white side of the board
        
        self.WM = True #helps keep track of turns of white
        self.CHECKM = False #checkmate
        self.STALEM = False #stalemate, no valid moves and king not in check
        self.SavingMoves = [] #helps keep track of moves made
        #helps keeping track of whethe the king under attack
        """
         made such a dumb mistakke accidentally put '.' instead of comma
         for the kings location and kept getting typeerror float not subscriptable 
        """
        self.BKLOC = (7,4)
        self.WKLOC = (0,4)

    #taking move as parameter and executes it 
    def MakingMoves(self, move):
        self.board[move.StartRow][move.StartColumn] = "EE"  #moving piece leaves a blank on the place it was before
        self.board[move.ER][move.EC] = move.Moved
        self.SavingMoves.append(move)  # log the move so we can undo it later
        self.WM = not self.WM  # switching players
        #need to keep track of kings location here as well
        if move.Moved == "wK":
            self.WKLOC = (move.ER,move.EC)
        elif move.Moved == "bK":
            self.BKLOC = (move.ER,move.EC)
        
        #pawn promo
        if move.Promo:
            self.board[move.ER][move.EC] = move.Moved[0] + 'Q' #parse string grab col
            
            
    """
        Need this for checkmate
    """
    def Undo(self):
        if len(self.SavingMoves) != 0: #to make sure that there is a move to undp
            move = self.SavingMoves.pop() #reutrns element and removes last element like stack
            #moving piece back to starting row and col
            self.board[move.StartRow][move.StartColumn] = move.Moved #piece moved
            #put back piece captured on board as well
            self.board[move.ER][move.EC] = move.Captured
            self.WM = not self.WM  # switching players
             #need to keep track of kings location here as well
        if move.Moved == "wK":
            self.WKLOC = (move.StartRow,move.StartColumn)
        if move.Moved == "bK":
            self.BKLOC = (move.StartRow,move.StartColumn)
        #everytime we undo a move we cannot be in check or stale therefore
        #needs to be reset
        self.CHECKM = False
        self.STALEM = False


    """
        check moves that are valid and occur before checkmate such as defending the King
        getting Valid Moves
        King is vvv important piece when in check limits piece movements
         algo:
             generate all possible moves whether check or not
             make a move once generated
             generate opposing moves
             check if opponent attacking king
                 if attack
                     not valid move
    
    if king in check after maing move then we need to remove that move
    since its not a valid move
    
    making sure number of times we swap players is even!!!
    """
    def CheckMoves(self):
        # generate
        M = self.PossibleMoves()
        #need to remove from list hence we loop backwards 
        #looping foward will mess if indexes didnt work 
        #make move
        for i in range(len(M)-1,-1,-1):
            self.MakingMoves(M[i])
            #opponents move
            O = self.PossibleMoves()
            #check if king under attack but switch turns before calling
            self.WM = not self.WM
            if self.Checkingforchecks(): # if attack not valid move 
                M.remove(M[i])
            #switch turns again to check if white was in check
            self.WM = not self.WM
            self.Undo()
        if len(M) == 0:
            #either checkmate or stalemate
            if self.Checkingforchecks():
                self.CHECKM = True
            else:
                self.STALEM = True
        else:
            self.CHECKM = False
            self.STALEM = False
            
        return M #debig latr
    
    """
        checking if opponent under attack
        decoupling the code to keep it neat
    """
    def Checkingforchecks(self): #for black and white
        if self.WM:
            #print("debug")
            return self.WhichSq(self.WKLOC[0], self.WKLOC[1])
        else:
            #print("debug")
            return self.WhichSq(self.BKLOC[0], self.BKLOC[1])
    
    """
        This code determines that which square the king is on by row and col
        switch to opp moves gen moves, switch turns back
        go through all moves 
        return false if under attack else true
    """
    def WhichSq(self,r,c):
        self.WM = not self.WM #opponents POV
        O = self.PossibleMoves()
        self.WM = not self.WM #switching turns back
        #print("debugging")
        for move in O:
            if move.ER == r and move.EC == c: #sq under attack
                #print("debugging")
                return True
        #sq undeer attack
        return False  
        
    """
     not check moves are all possible states that are valid in the game and do not require
     defending the King. Legal Moves in order to validate the moves we have to generate the
     other players moves. Gotta make sure that method can tell what type of piece it is and
     what colour it has
         Algo
         get all possible moves
             for each possible move
                 make move
                 gnerate all possible moves of opponent
                 look for checks 
                 if king safe
                     move is valid and move to list
        return list of check or valid moves
    """
    def PossibleMoves(self):
        #nested for loop to go through the board because at any given game state a piece will be anywhere
        PMoves = []
        for r in range(len(self.board)): #no of rows
            for c in range(len(self.board[r])): #no of rows in given row
                WhoseTurn = self.board[r][c][0]
                #we are parsing the strings on the board above to check whose turn
                if(WhoseTurn == 'w' and self.WM) or (WhoseTurn == 'b' and not self.WM):
                    WhatPiece = self.board[r][c][1]
                    #logic of each piece is called here
                    if WhatPiece == 'p':
                        self.Pawn(r,c,PMoves)
                    elif WhatPiece == 'R':
                        self.Rook(r,c,PMoves)
                    elif WhatPiece == 'B':
                        self.Bishop(r,c,PMoves)
                    elif WhatPiece == 'K':
                        self.King(r,c,PMoves)
                    elif WhatPiece == 'Q':
                        self.Queen(r,c,PMoves)
                    elif WhatPiece == 'N':
                        self.Knight(r,c,PMoves)
        #posible moves
        return PMoves 
                        
    #all methods below get all moves and locations and add possible moves to list   
    """
      black pawns move down, white move up, move twice on first move and capture diag
      rough algo: check if sq in front empty
          add as move
          check if on row 6 and sq 2 is empty
    """  
    def Pawn(self,r,c,PMoves):
    #if white turn to move we focus on white pawns
        if self.WM:
            #going up hence decreasing rows when sq empty
            if self.board[r-1][c] == "EE": #one sq move
                #adds as valid move
                PMoves.append(TrackingMoves((r,c),(r-1,c), self.board))
                #if sq in front block then cannot move 2 sq
                if r == 6 and self.board[r-2][c] == "EE":
                    PMoves.append(TrackingMoves((r,c),(r-2,c), self.board))
            #doesnt fall off board, capturing left
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #capturing black
                     PMoves.append(TrackingMoves((r,c),(r-1,c-1), self.board))
            if c+1 <= 7:
                #capture right
                if self.board[r-1][c+1][0] == 'b': #capturing black
                     PMoves.append(TrackingMoves((r,c),(r-1,c+1), self.board))
        else:
            #going down hence increasing rows when sq empty, blacks turn to move
            if self.board[r+1][c] == "EE": 
                #adds as valid move
                PMoves.append(TrackingMoves((r,c),(r+1,c), self.board))
                #if sq in front block then cannot move 2 sq
                if r == 1 and self.board[r+2][c] == "EE":
                    PMoves.append(TrackingMoves((r,c),(r+2,c), self.board))
            #doesnt fall off board, capturing left
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w': #capturing white
                     PMoves.append(TrackingMoves((r,c),(r+1,c-1), self.board))
            if c+1 <= 7:
                #capture right
                if self.board[r+1][c+1][0] == 'w': #capturing white
                     PMoves.append(TrackingMoves((r,c),(r+1,c+1), self.board))               
   
            
    """
        Rook moves N/S/E/W but does not jump over pieces
     """        
    def Rook(self,r,c,PMoves):
        #first row, second col in tuples
        NWSE = ((-1,0),(0,-1),(1,0),(0,1)) #movement in all four directions NWSE
        #checking enemy colour
        if self.WM:
            E = 'b'
        else:
            E = 'w'
        for i in NWSE:
            for x in range(1,8): #going through the board, row and col
                ER = r + i[0] * x
                EC = c + i[1] * x
                #this will check where the piece will land EC AND ER
                if 0 <= ER < 8 and 0 <= EC < 8: #so that piece doesnt fall off 
                    LP = self.board[ER][EC]
                    if LP == "EE": #can move unless there is a piece there
                        PMoves.append(TrackingMoves((r,c),(ER,EC), self.board))
                    elif LP[0] == E:
                        PMoves.append(TrackingMoves((r,c),(ER,EC), self.board))
                        break #to break the loop to check another direction
                    else:
                        break #same colour piece, preventing capture
                else:
                    break #off board
    
    """
    Bishop moves are exactly the same as rook, but moves diagonally
    so we gotta change the directions in the code most of it will be similar to Rook
    """
    def Bishop(self,r,c,PMoves):
         #first row, second col in tuples
        NWSE = ((-1,-1),(-1,1),(1,-1),(1,1)) #movement in all four directions NWSE but diagonally
        #we change the 0's here into ones so it moves slantly
        #checking enemy colour
        if self.WM:
            E = 'b'
        else:
            E = 'w'
        for i in NWSE:
            for x in range(1,8): #going through the board, row and col diagonally
                ER = r + i[0] * x
                EC = c + i[1] * x
                if 0 <= ER < 8 and 0 <= EC < 8: #so that piece doesnt fall off 
                    LP = self.board[ER][EC]
                    if LP == "EE": #can move unless there is a piece there
                        PMoves.append(TrackingMoves((r,c),(ER,EC), self.board))
                    elif LP[0] == E:
                        PMoves.append(TrackingMoves((r,c),(ER,EC), self.board))
                        break #to break the loop to check another direction
                    else:
                        break #same colour piece, preventing capture
                else:
                    break #off board 
    
    """
        The king moves all four directs 1 square around it
        need to work on checkmate, because kings cannot move on spaces
        that cause a check to occur
        basically 8 sq landings around it
    """
    def King(self,r,c,PMoves):
        M = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)) #to move in L
        #we change the 1's here into twos so it moves in L shape
        #checking same colour
        if self.WM:
            A = 'w'
        else:
            A = 'b'
            #need to work on checkmate and stalemate
        for i in range(8):
                ER = r + M[i][0]
                EC = c + M[i][1]
                if 0 <= ER < 8 and 0 <= EC < 8: #so that piece doesnt fall off 
                    LP = self.board[ER][EC]
                    if LP[0] != A:
                        PMoves.append(TrackingMoves((r,c),(ER,EC), self.board))
    
    """
     The knight can skip through other pieces unlike queen/rook bishop
     also it does not need to traverse row and col with two loops, just 
     need to add in coordinates for it to move properly
     only need to worry about landing sq
     rough algo:
         loop through the possible directions stored in list
         add the coordinates into row and column
    Note: need to check why not working with enemy piece??
    """
    def Knight(self,r,c,PMoves):
        MOVEL = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)) #to move in L
        #print("working fine") #debug
        #we change the 1's here into twos so it moves in L shape
        #checking same colour
        if self.WM:
            A = 'w'
        else:
            A = 'b'
        for i in MOVEL:
            ER = r + i[0]
            EC = c + i[1]
            #print("working") #debug
            if 0 <= ER < 8 and 0 <= EC < 8: #so that piece doesnt fall off 
                LP = self.board[ER][EC]
                #print("also working") #debug
                if LP[0] != A:
                    PMoves.append(TrackingMoves((r,c),(ER,EC), self.board))
        
              
    """
        The Queen is the mixture of Rook and Bishop because it can move both diagonally
        and sideways so the same algorithm will be similar except we will 
        merge cordinates of rook and bishop
    """
    def Queen(self,r,c,PMoves):
         #first row, second col in tuples
        NWSE = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)) #movement in all four directions NWSE
        #checking enemy colour
        if self.WM:
            E = 'b'
        else:
            E = 'w'
        for i in NWSE:
            for x in range(1,8): #going through the board, row and col
                ER = r + i[0] * x
                EC = c + i[1] * x
                if 0 <= ER < 8 and 0 <= EC < 8: #so that piece doesnt fall off 
                    LP = self.board[ER][EC]
                    if LP == "EE": #can move unless there is a piece there
                        PMoves.append(TrackingMoves((r,c),(ER,EC), self.board))
                    elif LP[0] == E:
                        PMoves.append(TrackingMoves((r,c),(ER,EC), self.board))
                        break #to break the loop to check another direction
                    else:
                        break #same colour piece, preventing capture
                else:
                    break #off board
        
#we create a move class that is tied to the game state 
#we can making chess notation function for the sake of debugging
class TrackingMoves():
    # key : value
    #chess has ranks for moving so we use dictionaries to map locations
    #ranks = rows, files = columns
    RanksRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    RowsToRanks = {v: k for k, v in RanksRows.items()}
    FilesColumns = {"a": 0, "b": 1, "c": 2, "d": 3,
                "e": 4, "f": 5, "g": 6, "h": 7}
    ColumnFiles = {v: k for k, v in FilesColumns.items()} #rlly cool way of going through the dictonary
    #basically map + reverse 
    #for each key/value make a val/key pair 

    def __init__(self, StartS, EndS, board):
         #a move in chess has start and end square, on the current board state
         #valid moves to keep check hence board is needed
         #storing log and current snapshot of the piece
         #helps us visualise the coordinates and moves
        self.StartRow = StartS[0]
        self.StartColumn = StartS[1]
        self.ER = EndS[0]
        self.EC = EndS[1]
        #keeping track of what piece was moved and what piece was captured
        self.Moved = board[self.StartRow][self.StartColumn]
        self.Captured = board[self.ER][self.EC]
         #pawn promo code
        self.Promo = False
        #self.PROMC = 'Q'
        if (self.Moved == 'wp' and self.ER == 0) or (self.Moved == 'bp' and self.ER == 7):
            self.Promo = True
        #unique ID between 0 to 7777 like a hash function from java DS
        self.moveID = self.StartRow * 1000 + self.StartColumn * 100 + self.ER * 10 + self.EC
        #print(self.moveID) #for debug purpose
         #all the code above is basically keep track of information 
         
        

    """
    Overriding equals method like in java so that one piece doesnt move on top of the
    other piece unless it is to capture it
    """
    def __eq__(self,other):
        #comparing one object with another object
        if isinstance(other, TrackingMoves): #checkin if obj belongs to class
            #comparing start col and row and end col and row
            return self.moveID == other.moveID
        return False
            
            
    def ChessNotations(self):
          #letter before number
        return self.RankFile(self.StartRow, self.StartColumn) + self.RankFile(self.ER, self.EC)



    def RankFile(self, r, c):
         #helper method like ones in OOP java
        return self.ColumnFiles[c] + self.RowsToRanks[r]       
         