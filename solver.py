import numpy as np

# check if n can be placed at a specific box on the grid, returns true if can be placed 
# row is y, col is x
def possible(grid, row, col, n):

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

# places numbers in boxes
def solve(grid):
    # go through every box 
    for row in range(9):
        for col in range(9):

            # if box is blank
            if grid[row][col] == 0:

                # generate numbers to place in box
                for n in range(1,10):

                    # chcek if number is valid
                    if possible(grid, row, col, n):
                        grid[row][col] = n

                        # call solve again to fill next box 
                        solve(grid)
                        grid[row][col] = 0
                
                # if all numbers not valid
                return 
    #print(np.matrix(grid))
    
  
