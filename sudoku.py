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

    # =========================
    # MRV heuristic
    # =========================
    def getUnassignedVariable(self):
        min_len = 10
        pos = (-1, -1)

        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == -1:
                    d = len(self.AvailableAssignments[i][j])
                    if d < min_len:
                        min_len = d
                        pos = (i, j)

        return pos

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

    # =========================
    # Correct Singleton Propagation
    # =========================
    def propagate_singletons(self):
        assigned = []
        removed_all = []

        progress = True
        while progress:
            progress = False
            for i in range(self.n):
                for j in range(self.n):
                    if self.board[i][j] == -1 and len(self.AvailableAssignments[i][j]) == 1:
                        value = self.AvailableAssignments[i][j][0]

                        self.board[i][j] = value
                        assigned.append((i, j))

                        ok, removed = self.forward_check(i, j, value)
                        removed_all.extend(removed)

                        if not ok:
                            return False, assigned, removed_all

                        progress = True

        return True, assigned, removed_all

    # =========================
    # Backtracking + FC + MRV + SP
    # =========================
    def csp_cells(self):
        if self.isGoal():
            return True

        ok, assigned, removed = self.propagate_singletons()
        if not ok:
            self.restore_domains(removed)
            for r, c in assigned:
                self.board[r][c] = -1
            return False

        row, col = self.getUnassignedVariable()
        if row == -1:
            return self.isGoal()

        domain_snapshot = copy.deepcopy(self.AvailableAssignments[row][col])

        while self.AvailableAssignments[row][col]:
            value = self.AvailableAssignments[row][col].pop()

            if self.isValidConstraints(row, col, value):
                self.board[row][col] = value

                ok, removed2 = self.forward_check(row, col, value)
                if ok and self.csp_cells():
                    return True

                self.restore_domains(removed2)
                self.board[row][col] = -1

        self.AvailableAssignments[row][col] = domain_snapshot

        # rollback singleton propagation
        for r, c in assigned:
            self.board[r][c] = -1
        self.restore_domains(removed)

        return False

    def solve(self):
        solvable = self.csp_cells()
        return solvable, self.board
