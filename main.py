# main.py

import numpy as np
import time
from sudoku import CSP_Sudoku

# =======================
# Global Sudoku Templates
# =======================

EASY = [
    [5,3,-1,-1,7,-1,-1,-1,-1],
    [6,-1,-1,1,9,5,-1,-1,-1],
    [-1,9,8,-1,-1,-1,-1,6,-1],
    [8,-1,-1,-1,6,-1,-1,-1,3],
    [4,-1,-1,8,-1,3,-1,-1,1],
    [7,-1,-1,-1,2,-1,-1,-1,6],
    [-1,6,-1,-1,-1,-1,2,8,-1],
    [-1,-1,-1,4,1,9,-1,-1,5],
    [-1,-1,-1,-1,8,-1,-1,7,9]
]

MEDIUM = [
    [-1,-1,-1,6,-1,-1,4,-1,-1],
    [7,-1,-1,-1,-1,3,6,-1,-1],
    [-1,-1,-1,-1,9,1,-1,8,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,5,-1,1,8,-1,-1,-1,3],
    [-1,-1,-1,3,-1,6,-1,4,5],
    [-1,4,-1,2,-1,-1,-1,6,-1],
    [9,-1,3,-1,-1,-1,-1,-1,-1],
    [-1,2,-1,-1,-1,-1,1,-1,-1]
]

HARD = [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,3,-1,8,5],
    [-1,-1,1,-1,2,-1,-1,-1,-1],
    [-1,-1,-1,5,-1,7,-1,-1,-1],
    [-1,-1,4,-1,-1,-1,1,-1,-1],
    [-1,9,-1,-1,-1,-1,-1,-1,-1],
    [5,-1,-1,-1,-1,-1,-1,7,3],
    [-1,-1,2,-1,1,-1,-1,-1,-1],
    [-1,-1,-1,-1,4,-1,-1,-1,9]
]

EXTREME = [
    [-1,-1,-1,-1,-1,-1, 2,-1,-1],
    [-1, 8,-1,-1,-1, 7,-1, 9,-1],
    [ 6,-1, 2,-1,-1,-1, 5,-1,-1],

    [-1, 7,-1,-1, 6,-1,-1,-1,-1],
    [-1,-1,-1, 9,-1, 1,-1,-1,-1],
    [-1,-1,-1,-1, 2,-1,-1, 4,-1],

    [-1,-1, 5,-1,-1,-1, 6,-1, 3],
    [-1, 9,-1, 4,-1,-1,-1, 7,-1],
    [-1,-1, 6,-1,-1,-1,-1,-1,-1]
]


# =======================
# Main Function
# =======================

def main():
    print("Choose Sudoku Level:")
    print("1 - Easy")
    print("2 - Medium")
    print("3 - Hard")
    print("4 - Extreme")

    choice = input("Enter choice: ")

    if choice == "1":
        board = EASY
    elif choice == "2":
        board = MEDIUM
    elif choice == "3":
        board = HARD
    elif choice == "4":
        board = EXTREME
    else:
        print("Invalid choice")
        return

    print("\nInitial Board:")
    print(np.array(board))

    agent = CSP_Sudoku(board)

    start_time = time.time()
    solvable, solution = agent.solve()
    end_time = time.time()

    print("\nSolvable:", solvable)

    if solvable:
        print("Solved Board:")
        print(np.array(solution))

    print(f"\nExecution Time: {end_time - start_time:.4f} seconds")

# =======================
# Run Program
# =======================

if __name__ == "__main__":
    main()
