import random, copy, numpy

class SudokuGenerator:
    """Class that generates a puzzle with solution"""

    def __init__(self):
        self.grid = [[0 for i in range(9)] for j in range(9)]


    def possible(self, grid, row, col, n):
        """Check if possible to place a number at a particular square, returns True if so"""
        # check row y for repeats
        for i in range(9):
            if grid[row][i] == n:
                return False
        
        # check column x for repeats
        for i in range(9):
            if grid[i][col] == n:
                return False

        # check box for repeats
        y = row // 3
        x = col // 3
        for i in range(3):
            for j in range(3):
                if grid[y * 3 + i][x * 3 + j] == n:
                    return False

        return True
    # checks if board is completed
    def is_finished(self, grid):
        """Checks if board is completed, returns True if so"""
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return False

        # if none of the numbers are 0, the board is finished 
        return True

    def solve(self, grid):
        """Solves sudoku"""
        # go through every box 
        for row in range(9):
            for col in range(9):

                # if box is blank
                if grid[row][col] == 0:
                    # generate numbers to place in box
                    for n in range(1,10):
                        # chcek if number is valid
                        if self.possible(grid, row, col, n):
                            grid[row][col] = n

                            if self.is_finished(grid):
                                self.counter += 1
                                break
                            else:
                                # call solve again to fill next box 
                                if self.solve(grid):
                                    return True
                    break
        grid[row][col] = 0
        # if all numbers not valid
        return False

    def solution_gen(self):
        """Generate fully filled sudoku using backtracking"""
        if self.is_finished(self.grid):
            return True

        num_list = [i for i in range(1,10)]
        for row in range(9):
            for col in range(9):
                # find empty square 
                if self.grid[row][col] == 0:
                    random.shuffle(num_list)
                    for n in num_list:
                        if self.possible(self.grid, row, col, n):
                            self.grid[row][col] = n

                            if self.solution_gen():
                                return True

                            self.grid[row][col] = 0
                    return False

    def remove_num(self):
        """Remove numbers from grid to create puzzle"""
        pass

def main():
    
    gen = SudokuGenerator()
    #gen.solution_gen()
    #print(numpy.matrix(gen.grid))
    s = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

    puzzle = [s[i:i+9] for i in range(0, len(s), 9)]
    board = [[int(i[j])  for j in range(9)] for i in puzzle]
    print(board)
    print(gen.solve(board))
    print(board)






main()

#at least 17 clues in order to have a puzzle with one unique solution.
#s = "000700000100000000000430200000000006000509000000000418000081000002000050040000300"

'''
s = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

puzzle = [s[i:i+9] for i in range(0, len(s), 9)]
board = [[int(i[j])  for j in range(9)] for i in puzzle]
'''