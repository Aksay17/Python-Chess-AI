# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 13:17:14 2021

@author: Aks

here ill probably add the Ai stuff will create a bunch of methods with 
different AI algorithms abd compare them

References:

Alpha-Beta Prunning;
    https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
Random Methods:
    https://www.w3schools.com/python/ref_random_random.asp
MinMax algo for chess:
    https://www.chessprogramming.org/Minimax
Zero-Sum games:
    https://en.wikipedia.org/wiki/Elo_rating_system#:~:text=The%20Elo%20rating%20system%20is,sum%20games%20such%20as%20chess.&text=After%20every%20game%2C%20the%20winning,or%20lost%20after%20a%20game.
"""

"""
    not gonna be very efficent but keeping this as comparaion and AI testing
"""
import random

def RandomAI(valdMves):
    return valdMves[random.randint(0,len(valdMves)-1)] #will pick a random move
    #this is inclusive of the last length will give out of bound error hence -1
 
"""
need to check for all possible responses in order to make a move
evaluate the board and take pick best postion in consideration

bishops and knights are equally powerful in chess queen is stronger than rook
pawns have least value
kings have no value because they cannot be captured
evaluate by seeing who has higher score therefore need to keep check
"""
#assigning point value to each piece, a dctonary 
#values are true to a real comuter chess
#value/key
piecepoints = {'K':0,'Q':10,'R':5,'B':3,'N':3,'p':1}
#if we can get checkmate 
CHECKPOINTS = 1000
#stalemate better than losing position
STALEPOINTS = 0
DEPTH = 2
#treatng as zero-sum game
#when white is winning score is +ve and -ve when black
#black has to try to make the board score neg as possible and vise versa

"""
    Making AI efficent by giving it positional scores
    for example
    knights position on middle of board is better than on rim 
    creating postional scores so its more effiecent AI will consider postion
    that holds a greater value
"""
NPOINTS = [[1,1,1,1,1,1,1,1],
           [1,2,2,2,2,2,2,1],
           [1,2,3,3,3,3,2,1],
           [1,2,3,4,4,3,2,1],
           [1,2,3,4,4,3,2,1],
           [1,2,3,3,3,3,2,1],
           [1,2,2,2,2,2,2,1],
           [1,1,1,1,1,1,1,1]]

BPOINTS = [[4,3,2,1,1,2,3,4],
           [3,4,3,2,2,3,4,3],
           [2,3,4,3,3,4,3,2],
           [1,2,3,4,4,3,2,1],
           [1,2,3,4,4,3,2,1],
           [2,3,4,3,3,4,3,2],
           [3,4,3,2,2,3,4,3],
           [4,3,2,1,1,2,3,4]]

#rooks are better at open columns or when they able to support the Queen
RPOINTS = [[4,3,4,4,4,4,3,4],
           [4,4,4,4,4,4,4,4],
           [1,1,2,3,3,2,1,1],
           [1,2,3,4,4,3,2,1],
           [1,2,3,4,4,3,2,1],
           [1,1,2,3,3,2,1,1],
           [4,4,4,4,4,4,4,4],
           [4,3,4,4,4,4,3,4]]

QPOINTS = [[4,1,1,1,1,1,1,4],
           [1,4,2,3,3,2,4,1],
           [1,2,4,3,3,4,2,1],
           [1,3,3,4,4,3,3,1],
           [1,3,3,4,4,3,3,1],
           [1,2,4,3,3,4,2,1],
           [1,4,2,3,3,2,4,1],
           [4,1,1,1,1,1,1,4]]

#white pawns positional movements
WPPOINTS = [[9,9,9,9,9,9,9,9],
           [9,9,9,9,9,9,9,9],
           [5,6,6,7,7,6,6,5],
           [2,3,3,5,5,3,3,2],
           [1,2,3,4,4,3,2,1],
           [1,1,2,3,3,2,1,1],
           [1,1,1,0,0,1,1,1],
           [0,0,0,0,0,0,0,0]]

#white pawns positional movements
BPPOINTS = [[0,0,0,0,0,0,0,0],
           [1,1,1,0,0,1,1,1],
           [1,1,2,3,3,2,1,1],
           [1,2,3,4,4,3,2,1],
           [2,3,3,5,5,3,3,2],
           [5,6,6,7,7,6,6,5],
           [9,9,9,9,9,9,9,9],
           [9,9,9,9,9,9,9,9]]

#key value pair for position and score we create dictonary
#N then look up col/row in the Npoints 2D array
#king is not necessary as it only needs to be protected 
PositionScore = {"N":NPOINTS,"B":BPOINTS,"Q":QPOINTS,"R":RPOINTS,
                 "bp":BPPOINTS,"wp":WPPOINTS}

"""
    give points based on pieces on board 
    dont need to give points when checkmate happens
    perfectly equal game will have board score 0
"""
def Points(board):
    #for loop goes through the board to sum up the score
    points = 0
    for rows in board:
        for square in rows: #check for pieces
        #[0] letter of colour
            if square[0] == 'w':
                points+= piecepoints[square[1]] #type of piece
            elif square[0] == 'b':
                points-= piecepoints[square[1]]
    return points

"""
    helpful to check for defense and attacks
    positive score means whte is winning black othewise
    (sees all other moves as equal need to fix that)
    so far only cares about points not position and in chess position is imp!
    
    not every capture is a good capture but lets consider 
"""
def BoardPoints(game): #takes whole game state as input
    #minmax m check nahe krna hoga phr
    if game.CHECKM:
        if game.WM:
            return -CHECKPOINTS #black wins
        else:
            return CHECKPOINTS #white
    elif game.STALEM:
        return STALEPOINTS #draw
        #for loop goes through the board to sum up the score
    points = 0
    #range val between 0 and 7 and eval squares
    for row in range(len(game.board)):
        for column in range(len(game.board[row])): #check for pieces
        #[0] letter of colour
            #square is the piece 
            square = game.board[row][column]
            if square != "EE":
                #score positionally
                PS = 0
                if square[1] != "K": #since i have no position score table for king
                    if square[1] == "p": #for pawns
                        PS = PositionScore[square][row][column]
                    else: #for other pieces
                        #positional scoring using dictonary lookup
                        PS = PositionScore[square[1]][row][column]
                if square[0] == 'w':
                    points+= piecepoints[square[1]] + PS * .1 #type of piece
                elif square[0] == 'b':
                    points-= piecepoints[square[1]] + PS * .1
    return points 
"""
    greedy fashion first 
    has to work for both black and white depending on whose turn it is
    should make best move based on maxisiming score based on pieces on board
"""   
def GreedyBestMove(game, valdMves):
    #since there is a neg/pos difference, need variable to toggle
    #similar to jave ? notation
    TurnToggle = 1 if game.WM else -1
    #black AI prespective
    #best possible max score will be the worst for black
    #max algo - starting with worst possible score and try to bring it down
    maxScore = -CHECKPOINTS
    bestMove = None
    for PlayerMoves in valdMves: #goes through board for whoever trn it is
        #tell game to make that move
        game.MakingMoves(PlayerMoves)
        if game.CHECKM:
            points = CHECKPOINTS
        elif game.STALEM:
            points = STALEPOINTS
        #score the board based on pieces of board
        #neg/pos score will depend on whose turn it is black or white
        else:
            points = TurnToggle*Points(game.board)
        #greedy algorithm presepctive
        if(points > maxScore):
            maxScore = points 
            #find current top score keep track of the moves 
            #if we find a score that is our best score
            bestMove = PlayerMoves
        #prevents bug 
        game.Undo()
    return bestMove
        
        
"""
   idea: need to maximise our score while minimising our oppoonents points
    we need to find min of our opp max points
    even/odd par changes here we negate the score
    need to look 2 moves in 
    algo:
        outer loop same as greedy algo 
        looking at my moves
        whats the max opponent response to that?
        if oppo max score is less than previous best score
        that ecomes my new best moove
        
        inner loop 
            get opp moves
            set their max score to low val
            try to fnd their best move
            checking for score
                is it larger than my max so far?
                if yes than it becomes my max
        (this is a redundant minmax code i tired doing with for loops 
         didnt delete it just to give an idea of my thought process)
"""   
def MinMax(game, valdMves):
    #since there is a neg/pos difference, need variable to toggle
    #similar to jave ? notation
    TurnToggle = 1 if game.WM else -1
    #black AI prespective
    #this is gonna be our opponents min/max score
    #want smallest val
    OppMinMaxScore = CHECKPOINTS
    PlayBestMove = None
    random.shuffle(valdMves)
    for PlayerMoves in valdMves: #goes through board for whoever trn it is
        #tell game to make that move
        game.MakingMoves(PlayerMoves)
        oppoMoves = game.CheckMoves() #grabbing oppo moves
        if game.STALEM:
            OppMaxScore = STALEPOINTS
        elif game.CHECKM:
            #need to find opp score neg
            #best move of oppo in the state space that i give them
            OppMaxScore = -CHECKPOINTS
        else:
            #for each of moves we make a move
            for OppoMove in oppoMoves:
                game.MakingMoves(OppoMove)
                #for every move opponent makes genes all possible moves
                #but need to check for checkmate so it is required
                game.CheckMoves()
                if game.CHECKM:
                   points = CHECKPOINTS
                elif game.STALEM:
                    points = STALEPOINTS
                #score the board based on pieces of board
                #neg/pos score will depend on whose turn it is black or white
                else:
                    points = -TurnToggle*Points(game.board) #negate
                #greedy algorithm presepctive
                if points > OppMaxScore:
                    OppMaxScore = points
                 #make sure undo that as well
                game.Undo()
        #mini part of the algo
        if OppMaxScore < OppMinMaxScore:
            OppMinMaxScore = OppMaxScore
            PlayBestMove = PlayerMoves
        #prevents bug 
        game.Undo()
    return PlayBestMove    
    
"""
depth in recursion: how deep you want to check before halting
boolean variable for players turn
needing helper methods to implement, to make first recursive call
each player gets 1 if statement
one we try to maximise (white) other minimise (black)
"""
def findMinMax(game, validMove):
    #initial recursive call to this value
    #returns result
    #white = T, black = F
    global NextMove, counter
    print(counter)
    #if method not set
    NextMove = None
    random.shuffle(validMove)
    MoveMinMax(game, validMove, DEPTH, game.WM)
    return NextMove

def findAlphabeta(game, validMove):
    global nextMove, counter
    #if method not set
    #counter = 0
    #print(counter)
    NextMove = None
    random.shuffle(validMove)
    #alpha = current max = lowest possible score
    #beta = current min = highest possible score
    #bringing them slowly towards each other when they cross
    #we know weve found out cuttofff point
    AlphaBeta(game, validMove, DEPTH, 1 if game.WM else -1, -CHECKPOINTS, CHECKPOINTS)
    return nextMove
    

def MoveMinMax(game, validMoves, depth, WM):
    #recursive code needs a global var defined
    global nextMove
    #check and stale are base cases, we turn score
    if depth == 0: #lower this by 1 until i get 0, lowest depth
        return Points(game.board)
    
    if game.WM:
        #if white turn - max
        maxScore = -CHECKPOINTS #worse score possible
        #then we go through our moves
        for move in validMoves:
            game.MakingMoves(move)
            #grabbing next valid moves
            nextMoves = game.CheckMoves()
            #recursivecall
            score = MoveMinMax(game, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                #if im at top of tree
                if depth == DEPTH:
                    NextMove = move #search all possibilities of that certain branch
                    #best score at that point in time
            game.Undo() 
        return maxScore               
            
    else: #now mini score
        minScore = CHECKPOINTS #start from highest thrn bring down
        #then we go through our moves
        for move in validMoves:
            game.MakingMoves(move)
            #grabbing next valid moves
            nextMoves = game.CheckMoves()
            #recursivecall
            score = MoveMinMax(game, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                #if im at top of tree
                if depth == DEPTH:
                    NextMove = move #search all possibilities of that certain branch
                    #best score at that point in time
            game.Undo() 
        return minScore
    
    
        
"""
    MinMax checks for every position regardless of the score except when in check
    because then valid moves get narrowed down to ones that exist to protect the king
    
    what alpha beta will allow is to do is cut off branches that arent going to yeild
    an optimal result
    
    relatively faster than MinMax
    assuming that your opponent makes the best move then we wouldnt have to check
    all states in that branch because the opponent already will benefit from it
    
    alpha = upper bound, beta = lower bound
    values for maximum possible and minimum possible scores overall
    
    if max score > alpha then maxscore = alpha
    if alpha >= beta then we prune off the branch
"""   
    
    
def AlphaBeta(game, validMoves, depth, whoseTurn, alpha, beta):
    global nextMove, counter
    #counter = counter + 1
    #print(counter)
    #checking for turns, no two for loops algo work for both cases
    if depth == 0:
        return whoseTurn * BoardPoints(game) 
    maxScore = -CHECKPOINTS
    for move in validMoves:
        game.MakingMoves(move)
        #grabbing next valid moves
        nextMoves = game.CheckMoves()
            #recursivecall
            #beta becomes negative alpha and alpha becomes negative beta
            #because for our opp everything is reversed
        score = -AlphaBeta(game, nextMoves, depth-1, -whoseTurn, -beta, -alpha)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                #print(move, score) #debug
        game.Undo()
        #cutting branch here
        if maxScore > alpha:
            alpha = maxScore
        #break case
        if alpha >= beta:
            #we stop looking, no need to evalute rest of the tree
            break
    return maxScore
        
