"""
A complete Sudoku game implemented in Python.

This script allows a user to play Sudoku in the command line. It features puzzle
generation with adjustable difficulty, a backtracking solver, and a text-based
interface for gameplay.

To run the game, execute this file from your terminal:
    python3 sudoku/sudoku.py
"""
import random

class Sudoku:
    def __init__(self, size=9):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.solution = None
        self.original_puzzle = None

    def generate_board(self):
        """Generates a complete and valid Sudoku board using a backtracking algorithm."""
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self._fill_board(self.board)
        self.solution = [row[:] for row in self.board]
        return True

    def _fill_board(self, board):
        """Helper function to recursively fill the board."""
        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            return True

        row, col = empty_cell
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)

        for num in nums:
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self._fill_board(board):
                    return True
                board[row][col] = 0
        return False

    def find_empty_cell(self, board):
        """Finds the next empty cell (represented by 0)."""
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def generate_puzzle(self, difficulty='easy'):
        """Generates a puzzle by removing numbers from a full board."""
        self.generate_board()

        if difficulty == 'easy':
            squares_to_remove = 40
        elif difficulty == 'medium':
            squares_to_remove = 50
        elif difficulty == 'hard':
            squares_to_remove = 60
        else:
            squares_to_remove = 40

        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)

        removed_count = 0
        for r, c in cells:
            if removed_count >= squares_to_remove:
                break

            temp = self.board[r][c]
            self.board[r][c] = 0

            # Check if the puzzle still has a unique solution
            solutions = self._count_solutions()
            if solutions != 1:
                self.board[r][c] = temp
            else:
                removed_count += 1

        self.original_puzzle = [row[:] for row in self.board]
        return self.board

    def _count_solutions(self, board=None):
        """Counts the number of solutions for the current board."""
        if board is None:
            board = [row[:] for row in self.board]

        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            return 1

        row, col = empty_cell
        count = 0
        for num in range(1, self.size + 1):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                count += self._count_solutions(board)
                board[row][col] = 0
                if count > 1: # Optimization: if more than one solution, no need to continue
                    return count
        return count

    def solve(self, board=None):
        """Solves the Sudoku puzzle using a backtracking algorithm."""
        if board is None:
            board = self.board

        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            return True  # Puzzle is solved

        row, col = empty_cell

        for num in range(1, self.size + 1):
            if self.is_valid(board, row, col, num):
                board[row][col] = num

                if self.solve(board):
                    return True

                board[row][col] = 0  # Backtrack

        return False

    def is_valid(self, board, row, col, value):
        """Checks if placing a value in a cell is valid."""
        # Check row
        for c in range(self.size):
            if board[row][c] == value and c != col:
                return False

        # Check column
        for r in range(self.size):
            if board[r][col] == value and r != row:
                return False

        # Check 3x3 subgrid
        box_row_start = row - row % 3
        box_col_start = col - col % 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if board[r][c] == value and (r, c) != (row, col):
                    return False
        return True



    def print_board(self, board=None):
        """Prints the Sudoku board in a user-friendly format."""
        if board is None:
            board = self.board
        for i in range(self.size):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - -")
            for j in range(self.size):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                print(str(board[i][j]).replace('0', '.'), end=" ")
            print()

    def play(self):
        """Starts the text-based Sudoku game."""
        print("Welcome to Sudoku!")
        difficulty = input("Choose a difficulty (easy, medium, hard): ").lower()
        self.generate_puzzle(difficulty)

        while True:
            print("\nCurrent board:")
            self.print_board()

            action = input("\nChoose an action: (m)ake move, (c)heck, (n)ew game, (q)uit: ").lower()

            if action == 'q':
                print("Thanks for playing!")
                break
            elif action == 'n':
                difficulty = input("Choose a difficulty (easy, medium, hard): ").lower()
                self.generate_puzzle(difficulty)
            elif action == 'c':
                if self.board == self.solution:
                    print("Congratulations! You've solved the puzzle correctly.")
                else:
                    print("There are some errors on the board. Keep trying!")
            elif action == 'm':
                try:
                    row = int(input("Enter row (1-9): ")) - 1
                    col = int(input("Enter column (1-9): ")) - 1
                    val = int(input("Enter value (1-9): "))

                    if 0 <= row < self.size and 0 <= col < self.size and 1 <= val <= self.size:
                        if self.original_puzzle[row][col] != 0:
                            print("Cannot change the original puzzle numbers.")
                        elif self.is_valid(self.board, row, col, val):
                            self.board[row][col] = val
                        else:
                            print("Invalid move. Try again.")
                    else:
                        print("Invalid input. Please enter numbers between 1 and 9.")
                except ValueError:
                    print("Invalid input. Please enter numbers.")

            if self.find_empty_cell(self.board) is None:
                if self.board == self.solution:
                    print("\nCongratulations! You've solved the puzzle!")
                    self.print_board()
                    break

if __name__ == '__main__':
    game = Sudoku()
    game.play()
