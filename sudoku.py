# sudoku.py

from collections import deque
import copy
import numpy as np

class CSP_Sudoku:
    """
    9x9 Sudoku CSP
    - Variables: each cell (row, col)
    - Domain: {1..9}
    - -1 means unassigned
    """

    def __init__(self, board):
        self.n = 9
        self.board = copy.deepcopy(board)

        self.domain = [1,2,3,4,5,6,7,8,9]

        self.AvailableAssignments = []
        self.DomainStack = deque(self.domain)

        for i in range(self.n):
            self.AvailableAssignments.append([])
            for j in range(self.n):
                if self.board[i][j] == -1:
                    self.AvailableAssignments[i].append(copy.copy(self.DomainStack))
                else:
                    self.AvailableAssignments[i].append(deque())

    def getUnassignedVariable(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == -1:
                    return i, j
        return -1, -1

    def isGoal(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == -1:
                    return False
        return True

    def isValidConstraints(self, row, col, value):
        # Row
        for j in range(self.n):
            if self.board[row][j] == value:
                return False

        # Column
        for i in range(self.n):
            if self.board[i][col] == value:
                return False

        # 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3

        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == value:
                    return False

        return True

    def removeAssignedVariables(self, row, col):
        self.board[row][col] = -1
        self.AvailableAssignments[row][col] = copy.copy(self.DomainStack)

    def csp_cells(self):
        if self.isGoal():
            return True

        row, col = self.getUnassignedVariable()
        if row == -1:
            return False

        while self.AvailableAssignments[row][col]:
            value = self.AvailableAssignments[row][col].pop()

            if self.isValidConstraints(row, col, value):
                self.board[row][col] = value

                if self.csp_cells():
                    return True

                self.removeAssignedVariables(row, col)

        return False

    def solve(self):
        solvable = self.csp_cells()
        return solvable, self.board
