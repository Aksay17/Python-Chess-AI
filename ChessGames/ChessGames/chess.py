# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 15:24:04 2021

@author: Aqsa
Since we are building this in python we are prefering simplicity over efficency
so the Chess game wouldnt be as fast as it would be in another language.
most of my work is based on 2D arrays which is a tad bit slower theres something called
bitboards which is a super advanced way of implmeneting chess for AI 

I added links throughout the code whereever I took help from
also sorry for the messy code I tend to put a lot of comments since the whole
project was made in a span of 1 month and 11 days the comments made it easier to
debug the code

Chess Pieces Image Link:
    https://www.dreamstime.com/high-quality-illustration-set-chess-pieces-isolated-transparent-background-graphic-element-your-design-project-high-image105511167
Pygame terminal and Chess Board help:
    https://openbookproject.net/thinkcs/python/english3e/pygame.html
For More pygame functions and methods:
    https://www.pygame.org/docs/ 
Pygame Text:
    https://pygame.readthedocs.io/en/latest/4_text/text.html
handling key errors:
    https://realpython.com/python-keyerror/
remove and pop method:
    https://www.w3schools.com/python/python_lists_remove.asp
RGB Color Codes:
    https://www.w3schools.com/colors/colors_picker.asp
subscripttable error:
    https://careerkarma.com/blog/python-typeerror-float-object-is-not-subscriptable/
"""

import pygame as p
from ChessGames import ChessEng
from ChessGames import AiPart
#from multiprocessing import Process, Queue


HEIGHT = 400 #Height of the pygame board
WIDTH = HEIGHT
NotationPanelWidth = 200
NotationPanelHeight = HEIGHT
DIME = 8 #dimension of the board
SQSIZE = HEIGHT // DIME #double divides is for integers
MAXFPS = 15 #for animation
IMAGES = {} #dictonary of images

"""
Loading images once in the memory to save up space rather than doing it over 
and over again and the game does lag. Hence we initialise dictonary of imagees

StartRow = x StartCol = y

When game is over make sure we pretend user from clicking the pieces
"""

#debug subscript error here
#handling user interface with these functions
def DrawBoard(screen,gs, Vmove, SquareSel, Font):
    #helper methods called here
    #method to display graphics
    ChessBoard(screen) #draws squares on the board
    HiLights(screen, gs, Vmove, SquareSel)
    Pieces(screen,gs.board)
    ChessMoves(screen,gs,Font)
    
    #order important! board first then pieces

"""
    Shows what square a piece was moved on the chess board
"""
def ChessMoves(screen,gs,font):
    #drawing rectangle at side of chess board
    #width x coord 
    WhereNotationsShouldBe = p.Rect(WIDTH, 0, NotationPanelWidth, NotationPanelHeight)
    p.draw.rect(screen, p.Color(133, 173, 173), WhereNotationsShouldBe)
    #moves made
    MoveLog = gs.SavingMoves
    #move texts
    MT = []
    #to prevent text overwriting
    Y = 5
    MovePerRow = 3
    #go through our move log two at a time
    for i in range(0, len(MoveLog), 2):
        #turn that we arw on
        #going to give us the number of move per pair 
        MoveStr = str(i//2+1) + "- " + MoveLog[i].ChessNotations() + " "
        #checking if black made a move (error fix)
        if i+1 < len(MoveLog):
            MoveStr += MoveLog[i+1].ChessNotations()
        MT.append(MoveStr)
    for x in range(0, len(MT), MovePerRow):
        txt = ""
        for j in range(MovePerRow):
            if x+j < len(MT):
                txt += MT[x+j] + " "
        txtObj = font.render(txt,True,p.Color("white"))
        #5 to left and 5 down
        txtloc = WhereNotationsShouldBe.move(5,Y)
        screen.blit(txtObj,txtloc)
        Y += txtObj.get_height()
    

def Text(screen, txt):
    #pygame text font setting italics to false
    font = p.font.SysFont("Times New Roman",60,True,False)
    txtObj = font.render(txt,0,p.Color(191, 191, 191))
    #to centre the text in middle and give shadow effect
    txtloc = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - txtObj.get_width()/2,HEIGHT/2 - txtObj.get_height()/2)
    screen.blit(txtObj,txtloc)
    #shadow effect
    txtObj = font.render(txt,0,p.Color(128, 0, 128))
    screen.blit(txtObj,txtloc.move(2,2))
    
"""
    This code will add glidng like movement to the pieces
    using pygame methods to complish this
    a copy of board will be made every time animation is done
"""
def Anime(move,screen,board,clock):
    #calling colours from board method
   #global colors
   colors = [p.Color(240, 245, 245), p.Color(133, 173, 173)]
   coordinate = [] #list of cordi animation will move through
   R = move.ER - move.StartRow
   C = move.EC - move.StartColumn
   #handles gliding speed, frame per square
   FPSQ = 5 #frames taken to move 1 square
   #total frames needed, frame count
   FC = (abs(R)+abs(C))*FPSQ
   #gen all coordinates based on frame count
   for F in range(FC+1): #doing plus 1 to bring us at end
       #change by R, also keep track of ratio of how far through gliding weve reached
       #frame/frame count = how far (to manipulate the frame)
       #doesnt need second for loop 2 loops are useless remove loop later
       #coordinate.append((move.StartRow+R*F/FC , move.StartColumn+C*F/FC))
       r,c = ((move.StartRow+R*F/FC , move.StartColumn+C*F/FC))
       ChessBoard(screen) #draws squares on the board
       Pieces(screen,board)
       #erases piece moved to end square warna itll show the piece already on the b
       color = colors[(move.ER+move.EC) % 2]
       Esq = p.Rect(move.EC*SQSIZE,move.ER*SQSIZE,SQSIZE,SQSIZE)
       p.draw.rect(screen,color,Esq)
       #captured puece on rectangle because it was vanishing bug fix
       if move.Captured != "EE":
           screen.blit(IMAGES[move.Captured],Esq)
       #moving piece on board show
       screen.blit(IMAGES[move.Moved],p.Rect(c*SQSIZE,r*SQSIZE,SQSIZE,SQSIZE))
       p.display.flip()
       #frames per second
       clock.tick(60)
          
"""
    Will highlight squares thhat are clicked by user
    and so we need to pass parameters of sq selected and valid moves
"""
def HiLights(screen, gs, Vmove, SquareSel):
    if SquareSel != ():
        #row col reference that user selects
        r,c = SquareSel
        #hightlight happens only at turn 
        #using if statement within if statement to compress code
        if gs.board[r][c][0] == ('w' if gs.WM else 'b'): #compring w or b to r,c,0
           #hightlight selected sq using pygame transparency feature
           #surface takes x,y in constructor
           surface = p.Surface((SQSIZE,SQSIZE))
           surface.set_alpha(180) #selects transparency value 0 is trans 255 opaque
           surface.fill(p.Color(119, 51, 255))
           screen.blit(surface, (c * SQSIZE, r * SQSIZE))
           #highlight the move that the selected piece can make
           surface.fill(p.Color(255, 128, 255))
           #go to all valid moves game generated
           #checking starting r,c to see if equal to sq selected
           #if yes then end r,c should be highlights
           for move in Vmove:
               if move.StartRow == r and  move.StartColumn == c:
                   screen.blit(surface, (move.EC * SQSIZE, move.ER * SQSIZE))
           
            
def Pieces(screen,board):
    for r in range(DIME):
            for c in range(DIME): #nested loop to go through the rows and columns
                piece = board[r][c]
                if piece != "EE": #to check for an empty sq
                #make a fast copy of an image or pixels from a sub-rectangle of one image or surface to another surface or image.
                   screen.blit(IMAGES[piece], p.Rect(c * SQSIZE, r * SQSIZE, SQSIZE, SQSIZE))
                #col by row squares                          
       
def ChessBoard(screen):
        colors = [p.Color(240, 245, 245), p.Color(133, 173, 173)] #two chess square colours
        for r in range(DIME):
            for c in range(DIME): #nested loop to go through the rows and columns
            #like we do for matrices 8 row/col here
                color = colors[((r+c)) % 2] #for light squares to be even and pick colours
#and dark squares to be odd and top left of chess board is always light and alternating on each sq
                p.draw.rect(screen, color, p.Rect(c*SQSIZE, r*SQSIZE, SQSIZE, SQSIZE))

def Images():
    pieces = ['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQSIZE,SQSIZE)) 
        #to load images and use proper scaling for it and make them sit in squares nicely
        #we can access by index the images


#This part of the code is responsible for dealing with the input and 
#showing what the game's current status (GAMESTATE OBJECT) graphics and everything
#of the game, usually written in most pygame games
def main():
    p.init()
    Time = p.time.Clock()
    screen = p.display.set_mode((WIDTH + NotationPanelWidth, HEIGHT))
    screen.fill(p.Color("white"))
    Game = ChessEng.GameFrameWork() #calling constructor from other class like we did in java
    ValidationofMoves = Game.CheckMoves()
    #pygame text font setting italics to false, bol to true as well
    NotationFont = p.font.SysFont("Times New Roman",12,True,False)
    
    #flag variable when move is made, function regeration after every valid move
    MOVEFLAG = False
    ANIMEFLAG = False #when we should glide
    OVERFLAG = False 
    #when both false then two Ais against each other
    WHITEPLAYER = True #human playing white, true. AI playing white then false
    BLACKPLAYER = False
    #THINKING = False
    #Process = None
    #it creates the variables defined in the constructor
    Images() #only once
    #print(Game.board) #testing to see if the board prints
    running = True
    #loop is used for showing and exiting the pygame terminal
    #that opens to show the chess board
    SquareSelected = () #tuple to keep track of last click of user in row,col
    PlayerClicks = [] #keep track of clicks made by player in 2 tuples that hold x,y coord pairs
    
    """
        main loop for the window to open
    """
    while running: # Main event loop
    #checking whose turn it is
        HUMAN = (Game.WM and WHITEPLAYER) or (not Game.WM and BLACKPLAYER)
        for e in p.event.get():  # Finds the events that are currently queued up
            if e.type == p.QUIT: # If the window close button is pressed
                running = False # The game stops running
                
                 #mouse event handles
            elif e.type == p.MOUSEBUTTONDOWN:
                if not OVERFLAG and HUMAN: #able to make mve when turn and when not game over
                    loc = p.mouse.get_pos() #location in x,y coordinates
                    col = loc[0]//SQSIZE #taking x coordinate / by sq size
                    row = loc[1]//SQSIZE
                    #print(col) debug statement
                    #to avoid double click issues, when user click twice or o notation section
                    if  SquareSelected == (row,col) or col >= 8:
                        SquareSelected = () #deselect when clicked again
                        PlayerClicks = [] #clear player clicks
                    else:
                         SquareSelected = (row,col)
                         PlayerClicks.append(SquareSelected) #fisrt click will append to second click of sq
                   #was that the users second click?
                    if len(PlayerClicks) == 2: #after sec click
                   #callin move function 
                        Moove = ChessEng.TrackingMoves(PlayerClicks[0],PlayerClicks[1],Game.board)
                        #print(Moove.ChessNotations()) #debug print statement
                        #Game.MakingMoves(Moove)                    
                        #if a move is made will generate a new set of valid moves
                        #based on id we have given
                        for x in range(len(ValidationofMoves)):
                            if Moove == ValidationofMoves[x]:
                                #move gen by engine
                                Game.MakingMoves(ValidationofMoves[x])
                                MOVEFLAG = True
                                ANIMEFLAG = True
                                SquareSelected = () #reset user clicks
                                PlayerClicks = [] #so that length doesnt create issues
                        if not MOVEFLAG:
                            PlayerClicks = [SquareSelected]
            
        """
            AI MOVES CODE
        """           
        #AI stuff here 
        #above is human player 
        #just as we dont want human make move when game over same for AI
        if not OVERFLAG and not HUMAN:
            #Game.CheckMoves() passing doing work twice
            AI = AiPart.findAlphabeta(Game, ValidationofMoves)
            if AI is None: #just in case our AI runs out of moves
                AI = AiPart.RandomAI(ValidationofMoves)
            #AI makes move
            Game.MakingMoves(AI)
            #move has been made
            MOVEFLAG = True
            #gliding happens
            ANIMEFLAG = True
        
        """
            Animation and drawing the game on the windows 
        """
        if MOVEFLAG:
            if ANIMEFLAG: #if true then glding motion
                #glding last move at move log onto scren with the board
                Anime(Game.SavingMoves[-1],screen, Game.board,Time)
            #generating valid move when valid move is actually made
            ValidationofMoves = Game.CheckMoves()
            MOVEFLAG = False  
            ANIMEFLAG = False
        DrawBoard(screen,Game,ValidationofMoves,SquareSelected, NotationFont)
        
        """
            END GAME STATE CHECK
        """
        if Game.CHECKM:
            OVERFLAG = True
            if Game.WM:
                Text(screen, "Black Wins!")
            else:
                Text(screen, "White Wins!")
        elif Game.STALEM:
            OVERFLAG = True
            Text(screen, "StaleMate :(")
        Time.tick(MAXFPS)
        p.display.flip()
    p.quit()
    

"""
to run the main code 
"""
main()