import tkinter as tk
from tkinter import messagebox

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, column=4, columnspan=2)

    def create_grid(self):
        validate_cmd = (self.root.register(self.validate_input), '%P') # validate the input enetered and root.register() makes validate_input() into a tool to pass to tkinter functions
        for row in range(9):
            for col in range(9):
                self.cells[row][col] = tk.Entry(self.root, width=2, font=("Arial", 18), justify="center", validate="key", validatecommand=validate_cmd)
                self.cells[row][col].grid(row=row, column=col, padx=5, pady=5)

    def validate_input(self, P):
        if P == "" or (P.isdigit() and 1 <= int(P) <= 9):
            return True
        else:
            messagebox.showerror("Invalid input", "Please enter a number between 1 and 9.")
            return False

    def get_board(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.cells[row][col].get()
                if val.isdigit():
                    current_row.append(int(val))
                else:
                    current_row.append(0)
            board.append(current_row)
        return board

    def set_board(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    self.cells[row][col].delete(0, tk.END)
                    self.cells[row][col].insert(0, str(board[row][col]))

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def is_valid(self, board, num, pos):
        for i in range(len(board[0])):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(len(board)):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self, board):
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(board, i, (row, col)):
                board[row][col] = i

                if self.solve(board):
                    return True

                board[row][col] = 0

        return False

    def solve_sudoku(self):
        board = self.get_board()
        if self.solve(board):
            self.set_board(board)
        else:
            messagebox.showerror("Error", "No solution exists")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
