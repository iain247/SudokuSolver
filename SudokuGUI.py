# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 20:51:43 2020

@author: iainr
"""

import pygame, sys, math, time
from SudokuSolver import Sudoku


####################################################
## BUG LIST
## make mouse click exit user input (although this is not necessary)
## also have to restart kernel everytime for some reason
## USER INPUTTED VALUES ARE NOT SHOWING UP AFTER UPDATEBOARD IS CALLED

#########################################################
## MAKE INSTRUCTION MENU AT THE START
## give user option to go back to instructions at anytime
#########################################################
        
#########################################################
## PROBLEMS WITH PUZZLE AND STARTPUZZLE
## ADDING TO STARTPUZZLE ALSO ADDS TO PUZZLE
## FIX IT DUDE

#initialise
pygame.init()

#create sudoku class
sk = Sudoku()

#some rgb tuples
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200,200,200)

#define window length
length = 500
screen = pygame.display.set_mode([length, length])

#define some useful geometric features for later use
thick = 5
thin = 2    
halfThick = thick/2
halfThin = thin/2
newLength = length - thick
boxSize = (length - 4*thick - 6*thin)/9
    
    
def helpScreen():
    """
    Help screen which contains instructions on how to use the solver
    """
    screen.fill(white)
    pygame.display.update()
    insertText(80, "Welcome to Iain's Sudoku Solver", 38)
    insertText(175, "Controls" ,24)
    insertText(210, "Click a square to edit its number. The selected box will turn gray.", 15)
    insertText(225, "You can then enter a number and confirm it by pressing enter.", 15)
    insertText(250, "Press the spacebar to start solving the puzzle. Once started, you ", 15)
    insertText(265, "can press the up and down arrow keys to control the solving speed. ", 15)
    insertText(280, "You can also press space again to solve at full speed or backspace ", 15)
    insertText(295, "to pause and reset", 15)
    insertText(360, "Press 'h' at any time to return to this menu", 15)
    insertText(410, "Press any key to continue", 18)
 
    while True:
        
        for event in pygame.event.get():
            
            #quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
            #handle key presses
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:   
                drawPuzzle()
                return
                    
                
def insertText(top, message, fontSize):
    """
    Inserts centre aligned text. Requires 'top' coordinate,

    """
    
    textFont = pygame.font.SysFont('Arial',fontSize)
    text = textFont.render(message, True, black)
    size = textFont.size(message)
    
    left = length/2 - size[0]/2
    #top = length/2 - size[1]
    
    screen.blit(text, (left,top))
    
    pygame.display.update()   

    
def updateBoard():
    """
    Updates board so it matches sudoku object
    """
    for row in range(9):
        for col in range(9):
            num = sk.puzzle[row,col]
            index = (row,col)
            insertNumber(index,int(num))
            

def drawPuzzle():
    """
    Draws a blank sudoku puzzle
    """   
    screen.fill(black)   
    for row in range(9):
        for col in range(9):
            drawRect(row,col,white)
            
  
def getCoord(row, col):
    """
    Returns the left and top coordinate of a specific sudoku cell
    """
    
    topLines = 0
    
    for i in range(9):
        
        leftLines = 0
        
        if i % 3 == 0:
            topLines += thick
        else:
            topLines += thin
            
        top = i*boxSize + topLines
            
        for j in range(9):
            
            if j % 3 == 0:
                leftLines += thick           
            else:
                leftLines += thin
                       
            left = j*boxSize + leftLines
            
            if i == row and j == col:
                
                return left, top
            

def drawRect(row, col, colour):
    """
    Draws a rectangle of a specific colour at a specified location
    """
    
    left, top = getCoord(row, col)
    
    rect = pygame.Rect(left,top,boxSize,boxSize)
    pygame.draw.rect(screen, colour, rect)
    
    pygame.display.update()


def insertNumber(index, num, colour=white, user = False):
    """
    Inserts a number into a specific sudoku cell.
    Colour defines the cell background colour
    If user = true, the sudoku object is updated and the number is permanently
    inserted
    """
    #delete current number
    row, col = index
    drawRect(row,col,colour)
       
    if num == 0:
        if user:
            sk.puzzle[row,col] = num
            sk.startPuzzle[row,col] = num
        return
      
    #insert text   
    font = pygame.font.SysFont('Arial', 38)
    txt = font.render(str(num), True, black)
    size = font.size(str(num))
    
    left, top = getCoord(row, col)    
    
    drawX = left + boxSize/2 - size[0]/2
    drawY = top + boxSize/2 - size[1]/2
    
    screen.blit(txt, (drawX,drawY))
    
    pygame.display.update()
    
    if user: # if this is true, amend the puzzle
        sk.puzzle[row,col] = num
        sk.startPuzzle[row,col] = num
        

def getCell(pos):
    """
    Returns the cell row and column of a mouseclick position
    """
    
    #unpack coordinates
    xPos, yPos = pos
    
    x = math.floor(xPos/length * 9)
    y = math.floor(yPos/length * 9)
    
    return y,x

def getText(event, pos):
    """
    Takes input from the user in the form of a number between 0 and 9.
    Returns false once the user has finished their input and pressed enter
    """
    
    row,col = getCell(pos) 
   
    if event.key == pygame.K_RETURN:
        global inputValue # create global value for input
        
        try: # if a number has been entered, put it in the board
            insertNumber((row,col), inputValue, white, True)
        except: # if not, make it blank
            drawRect(row, col, white)
            
        inputValue = 0 # reset back to 0
        return False # return false to stop text input
        
    elif event.key == pygame.K_BACKSPACE:
        inputValue = 0
        insertNumber((row,col),inputValue,gray)
        
    else:
        num = event.unicode
        if num.isnumeric():
            num = int(num)
            if num in range(10) and sk.checkNum(num, row, col):
                inputValue = num 
                insertNumber((row,col),inputValue,gray)
                
    return True
    
    
def showSolve(event):
    """
    Uses Sudoku object's solve generator to find a number, its index, and its
    colour whilst solving
    """
    
    delay = 0.4
    
    for solution in sk.solve():
        
        pygame.event.pump() # to stop from crashing
        time.sleep(delay)
                          
        insertNumber(solution[0], solution[1], solution[2])
        
        for event in pygame.event.get():
        
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP:
                    delay *= 0.5
                if event.key == pygame.K_DOWN:
                    delay *= 2
                if event.key == pygame.K_SPACE:
                    delay = 0
                if event.key == pygame.K_BACKSPACE:
                    sk.reset()
                    return
                if event.key == pygame.K_h:
                    helpScreen()
                    return
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    updateBoard() # to make all squares white again

##################################################
# MAIN LOOP
##################################################

def main():
    
    helpScreen()

    userInput = False
      
    while True:
            
        for event in pygame.event.get():
            
            #quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
            #handle mouse clicks
            if event.type == pygame.MOUSEBUTTONUP:
                
                if not userInput:
                
                    pos = pygame.mouse.get_pos()               
                    row, col = getCell(pos) # change this to use rect overlap function
                    drawRect(row,col,gray)
                    userInput = True # take input from user               
                             
            #handle key presses
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_h:
                    helpScreen()                
                
                elif userInput:
                    userInput = getText(event, pos)                   
                
                elif event.key == pygame.K_SPACE:              
                    showSolve(event)
                        
                elif event.key == pygame.K_BACKSPACE:
                    sk.reset()
                    updateBoard()
                    
                
if __name__ == "__main__":
    main()         
                
                