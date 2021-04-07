# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 13:30:32 2020

@author: iainr
"""

import numpy as np
import math


class Sudoku:
    def __init__(self, startPuzzle = np.zeros((9,9))):
        
        # EASY PUZZLE
        # self.startPuzzle = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
        #                         [6, 0, 0, 1, 9, 5, 0, 0, 0],
        #                         [0, 9, 8, 0, 0, 0, 0, 6, 0],
        #                         [8, 0, 0, 0, 6, 0, 0, 0, 3],
        #                         [4, 0, 0, 8, 0, 3, 0, 0, 1],
        #                         [7, 0, 0, 0, 2, 0, 0, 0, 6],
        #                         [0, 6, 0, 0, 0, 0, 2, 8, 0],
        #                         [0, 0, 0, 4, 1, 9, 0, 0, 5],
        #                         [0, 0, 0, 0, 8, 0, 0, 7, 9]])
        # 
        # HARD PUZZLE
        # self.startPuzzle = np.array([[0, 0, 0, 0, 0, 0, 0, 9, 0],
        #                               [0, 9, 0, 7, 0, 0, 2, 1, 0],
        #                               [0, 0, 4, 0, 9, 0, 0, 0, 0],
        #                               [0, 1, 0, 0, 0, 8, 0, 0, 0],
        #                               [7, 0, 0, 4, 2, 0, 0, 0, 5],
        #                               [0, 0, 8, 0, 0, 0, 0, 7, 4],
        #                               [8, 0, 1, 0, 0, 0, 0, 4, 0],
        #                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                               [0, 0, 9, 6, 1, 3, 0, 0, 0]])
        
        #use input argument to create a copy of the start puzzle
        self.startPuzzle = startPuzzle.copy()
        
        #initialise puzzle with copy of start puzzle
        self.puzzle = startPuzzle.copy()
        
        self.orange = (255,165,0)
        self.yellow = (255,255,0)
        self.white = (255, 255, 255)
        
        
    def reset(self):
        """
        Resets the puzzle back to its original state
        """
        
        self.puzzle = self.startPuzzle.copy()
        
    
    def numZeros(self):
        """
        Counts the number of unsolved spaces in the puzzle
        """
        
        nonZeros = np.count_nonzero(self.puzzle)
        return self.puzzle.size - nonZeros
        
        
    def checkAll(self, r, c):
        """
        Checks which numbers are plausible at a specific index
        """
        
        if self.puzzle[r,c] != 0:
            print("error, solution already exists at this location")
            return
        
        #check row
        row = self.puzzle[r]
        #check column
        col = self.puzzle[:,c]
        #check box
        box = (self.puzzle[3*math.floor(r/3):3+3*math.floor(r/3):1,
                           3*math.floor(c/3):3+3*math.floor(c/3):1])
        
        #initialise list of potential solutions
        sol = []
        
        #check for plausible solutions
        for num in range(1,10):
            # check if number is not in row or column or box
            if num not in row and num not in col and num not in box:
                sol.append(num)
        
        return sol
    
    def checkNum(self, num, r, c):
        """
        Checks if a number is plausible at a specific index
        """
        
        #check row
        row = self.puzzle[r]
        #check column
        col = self.puzzle[:,c]
        #check box
        box = (self.puzzle[3*math.floor(r/3):3+3*math.floor(r/3):1,
                           3*math.floor(c/3):3+3*math.floor(c/3):1])
        

        return num not in row and num not in col and num not in box
    
                
    def solve(self):
        """
        Solves by iteratively checking each box to see if there is only 1
        possible solution. Keeps updating until puzzle is complete, or no more
        solutions can be found
        """
        
        #keep solving while there are empty numberes
        while self.numZeros() > 0:
            #store puzzle in temporary array for later
            temp = self.puzzle.copy() #.copy since np arrays are passed by reference
            #loop through each row
            for row in range(9):
                #loop through number in each row
                for col in range(9):
                    #check if number is 0
                    num = self.puzzle[row,col]
                    if num == 0:
                        #check which numbers are plausable in this location
                        sol = self.checkAll(row,col)
                        #if no solutions then puzzle is flawed
                        if len(sol)==0:
                            return
                        #if only 1 plausible solution add it to the puzzle
                        if len(sol) == 1:
                            self.puzzle[row,col] = sol[0] 
                            yield (row,col), sol[0], self.yellow

                            
            #check if no new solutions were found
            if (temp == self.puzzle).all() and self.numZeros() != 0:                
                yield from self.solveBackTrack()       
                return
                
            
    def nextZero(self):
        """
        Finds the index of the "first" zero
        """
        for i in range(9):
            for j in range(9):
                if self.puzzle[i,j] == 0:
                    return i, j
                
                
    def solveBackTrack(self):
        """
        Solves iteratively using backtracking if no values are found from solve()
        """
        
        #return if puzzle is already solved
        if self.numZeros() == 0:
            return
        
        #find the index of the next empty cell
        row, col = self.nextZero()

        #loop through all potential solutions
        for num in range(1,10):
            
            if self.checkNum(num, row, col):
                           
                #copy puzzle to revert back to incase of error
                orig = self.puzzle.copy()
                
                #add potential solution into the puzzle
                self.puzzle[row,col] = num
                
                #x = self.puzzle.copy()
                yield (row, col), num, self.orange
                
                yield from self.solve()
                
                #return if puzzle is solved
                if self.numZeros()==0:
                    return
                
                #revert back to previous solution               
                yield from self.prevState(orig, self.puzzle)
                
                            
    def backTrack(self):
        """
        Solves iteratively using purely backtracking
        """
        #return true if puzzle is solved
        if self.numZeros() == 0:
            return True
        
        #find the index of the next empty cell
        row, col = self.nextZero()
        
        #find all solutions at this index
        sols = self.checkAll(row,col)
        
        #return false if no solutions available
        if sols == []:
            return False
        
        #loop through all potential solutions
        for num in sols:
                       
            #add potential solution into the puzzle
            self.puzzle[row,col] = num
            
            #if puzzle can be completed, return true
            if self.backTrack():
                return True
            
            #reset to 0 of no potential solutions exist
            else:
                self.puzzle[row,col] = 0
                
    
    def prevState(self, prevPuzzle, currPuzzle):
        """
        Reverts the puzzle back to previous state if an error is found
        """
        
        for i in range(8,-1,-1): # loop backwards for better visuals
            for j in range(8,-1,-1):
                if prevPuzzle[i,j] != currPuzzle[i,j]:
                    yield (i,j), 0, self.white
                    
        self.puzzle = prevPuzzle.copy()
        
    
    def showSolutions(self, delay=0):    
        """
        Shows what is produced by the solving generator function
        """
        for solution in self.solve(): 
            print(solution)  

            
    def showBoard(self, delay=0):
        """
        Prints the board iteratively as it is solved
        """
        
        puzzle = self.startPuzzle.copy()
        
        for solution in self.solve():
            i, j = solution[0]
            num = solution[1]
            puzzle[i,j] = num
            print(puzzle)



