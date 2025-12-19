# sudoku.py

from collections import deque
import copy

class CSP_Sudoku:

    def __init__(self, board):
        self.n = 9
        self.board = copy.deepcopy(board)

        self.domain = [1,2,3,4,5,6,7,8,9]

        self.AvailableAssignments = []
        for i in range(self.n):
            self.AvailableAssignments.append([])
            for j in range(self.n):
                if self.board[i][j] == -1:
                    self.AvailableAssignments[i].append(deque(self.domain))
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
        for j in range(self.n):
            if self.board[row][j] == value:
                return False

        for i in range(self.n):
            if self.board[i][col] == value:
                return False

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == value:
                    return False

        return True

    # =========================
    # Forward Checking
    # =========================
    def forward_check(self, row, col, value):
        removed = []

        # Row & Column
        for k in range(self.n):
            if self.board[row][k] == -1 and value in self.AvailableAssignments[row][k]:
                self.AvailableAssignments[row][k].remove(value)
                removed.append((row, k, value))
                if not self.AvailableAssignments[row][k]:
                    return False, removed

            if self.board[k][col] == -1 and value in self.AvailableAssignments[k][col]:
                self.AvailableAssignments[k][col].remove(value)
                removed.append((k, col, value))
                if not self.AvailableAssignments[k][col]:
                    return False, removed

        # Box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == -1 and value in self.AvailableAssignments[i][j]:
                    self.AvailableAssignments[i][j].remove(value)
                    removed.append((i, j, value))
                    if not self.AvailableAssignments[i][j]:
                        return False, removed

        return True, removed

    def restore_domains(self, removed):
        for r, c, v in removed:
            self.AvailableAssignments[r][c].append(v)

    def csp_cells(self):
        if self.isGoal():
            return True

        row, col = self.getUnassignedVariable()

        domain_snapshot = copy.deepcopy(self.AvailableAssignments[row][col])

        while self.AvailableAssignments[row][col]:
            value = self.AvailableAssignments[row][col].pop()

            if self.isValidConstraints(row, col, value):
                self.board[row][col] = value

                ok, removed = self.forward_check(row, col, value)
                if ok:
                    if self.csp_cells():
                        return True

                self.restore_domains(removed)
                self.board[row][col] = -1

        self.AvailableAssignments[row][col] = domain_snapshot
        return False

    def solve(self):
        solvable = self.csp_cells()
        return solvable, self.board
