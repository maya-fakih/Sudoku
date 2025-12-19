#install numpy using: pip install numpy

from collections import deque
import copy
import numpy as np
import itertools
import time

class CSP_NQueens:
    """ attributes
    num_rows=8
    num_cols=8
    n=8
    board[n][n] initialized to -1 : those are the variables
    domain=[1,0] :domain values
    DomainStack deque(0,1) :domain values as a stack
    AvailableAssignments[8][8] initialized to DomainStack: available domain values per variable
    """
    
    def __init__(self,n=8):
    
        self.n=n
        self.num_rows=n
        self.num_cols=n
        self.domain=[1,0]
  
        #self.board=[[0]*self.num_cols for i in range(self.num_rows)]
        self.board=[]
        self.AvailableAssignments=[]
        self.DomainStack=deque()
        self.DomainStack.append(0)
        self.DomainStack.append(1)
        for row in range(self.num_rows):
            # Add an empty array that will hold each cell
            # in this row
            self.board.append([])
            self.AvailableAssignments.append([])
            for column in range(self.num_cols):
                self.board[row].append(-1)  # Append a cell with value -1 (unassigned)                
                self.AvailableAssignments[row].append(copy.copy(self.DomainStack))  #set availble assignments per cell
        
    def isValidConstraintsRooks(self,row,col):        
        for j in range(len(self.board)):
            if self.board[row][j]==1: return False
        
        for i in range(len(self.board[0])):
            if self.board[i][col]==1: return False      
        
        return True
    
    def getUnassignedVariable(self,assignment):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if assignment[i][j]==-1:
                    return (i,j)
        return (-1,-1)
    
    def removeAssignedVariables(self,row,col,assignment):
        assignment[row][col]=-1
        if col<(self.num_cols-1):
            col=col+1
        else:
            row=row+1
            col=0
        for i in range(row,self.num_rows):
            for j in range(col,self.num_cols):
                assignment[i][j]=-1
                self.AvailableAssignments[i][j]=copy.copy(self.DomainStack)
            col=0
        #print(self.AvailableAssignments)
        return assignment
   
    def isGoal(self,assignment):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if assignment[i][j]==-1:
                    return False
        
        nb_assigned_queens=0
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if assignment[i][j]==1:
                    nb_assigned_queens=nb_assigned_queens+1
        
        if nb_assigned_queens==self.n:
            return True
        else:
            return False    
    
       
    def isValidConstraints(self,assignment,row,col,domain_value=1,color=2):
        if domain_value==0:
            return True
        for j in range(len(self.board)):
            
            if assignment[row][j]==1: 
                #print("conflict on row",row)
                return False
            #self.board[row][j]=color
        for i in range(len(self.board[0])):
            
            if assignment[i][col]==1: 
                #print("conflict on col",col)
                return False
            #self.board[i][col]=color
        
        #left up
        for i, j in zip(range(row,-1,-1),range(col,-1,-1)):            
            if assignment[i][j]==1: 
                #print("conflict on diag 1st, cell:",i,j)
                return False
            #self.board[i][j]=color
        #right down
        for i, j in zip(range(row+1,self.num_rows),range(col+1,self.num_cols)):            
            if assignment[i][j]==1: 
                #print("conflict on diag 3rd, cell:",i,j)
                return False
            #self.board[i][j]=color
        #left down   
        for i, j in zip(range(row,self.num_rows),range(col,-1,-1)):            
            if assignment[i][j]==1: 
                #print("conflict on diag 4th, cell:",i,j)
                return False
            #self.board[i][j]=color
        #right up   
        for i, j in zip(range(row-1,-1,-1),range(col+1,self.num_cols)):            
            if assignment[i][j]==1: 
                #print("conflict on diag 2nd, cell:",i,j)
                return False
            #self.board[i][j]=color
        
        #print ("No Conflicts")
        return True
    
    def csp_cells(self,assignment,step=0):
        #print("\niteration nb:",step)
        #print("goal:",self.isGoal())
        
        #print(np.matrix(assignment))
        #print()
        if (self.isGoal(assignment)==True):
            return True
        i,j=self.getUnassignedVariable(assignment)
        while self.AvailableAssignments[i][j]:
        #for value in self.domain:
            value=self.AvailableAssignments[i][j].pop()            
            if self.isValidConstraints(assignment,i,j,value):
                assignment[i][j]=value
                res=self.csp_cells(assignment,step+1)
                
                if res==True:
                    return True
                if assignment[i][j]==1:
                    self.removeAssignedVariables(i,j,assignment)
                
            #print("T[",i,"][",j,"]: ",self.board[i][j])
        return False
      
    
    

#initialize a 2d array of zero values
nqueens=CSP_NQueens(10)
#print((nqueens.AvailableAssignments))
#nqueens.board[2][0]=1

color=2
#nqueens.isValidConstraints(4,4)
t1=time.time()
print(nqueens.csp_cells(nqueens.board))
print(np.array(nqueens.board))
#print((nqueens.AvailableAssignments))
exec_time=time.time()-t1
print(exec_time)





