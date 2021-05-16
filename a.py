counter = 0

def solve_puzzle( grid):
    """solve the sudoku puzzle with backtracking"""
    for i in range(0,81):
        row=i//9
        col=i%9
        #find next empty cell
        if grid[row][col]==0:
            for number in range(1,10):
                #check that the number hasn't been used in the row/col/subgrid
                if valid_location(grid,row,col,number):
                    grid[row][col]=number
                    if not find_empty_square(grid):
                        counter+=1
                        break
                    else:
                        if solve_puzzle(grid):
                            return True
            break
    grid[row][col]=0
    #print(grid)  
    return False

def find_empty_square(grid):
    """return the next empty square coordinates in the grid"""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i,j)
    return

def valid_location(grid,row,col,number):
    """return False if the number has been used in the row, column or subgrid"""
    if num_used_in_row(grid, row,number):
        return False
    elif num_used_in_column(grid,col,number):
        return False
    elif num_used_in_subgrid(grid,row,col,number):
        return False
    return True

def num_used_in_row(grid,row,number):
    """returns True if the number has been used in that row"""
    if number in grid[row]:
        return True
    return False

def num_used_in_column(grid,col,number):
    """returns True if the number has been used in that column"""
    for i in range(9):
        if grid[i][col] == number:
            return True
    return False

def num_used_in_subgrid(grid,row,col,number):
    """returns True if the number has been used in that subgrid/box"""
    sub_row = (row // 3) * 3
    sub_col = (col // 3)  * 3
    for i in range(sub_row, (sub_row + 3)): 
        for j in range(sub_col, (sub_col + 3)): 
            if grid[i][j] == number: 
                return True
    return False


s = "534070000600195000098000060800060003400803001700020006060000280000419005000080200"

puzzle = [s[i:i+9] for i in range(0, len(s), 9)]
board = [[int(i[j])  for j in range(9)] for i in puzzle]

print(solve_puzzle(board))
print(board)
print(counter)