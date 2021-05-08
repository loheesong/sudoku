import pygame, time, datetime
from solver import possible

# constants are in all caps
WIDTH, HEIGHT = 540, 540
FPS = 60
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption("Sudoku")
pygame.font.init()
numFont = pygame.font.SysFont("tahoma", 32)
smallFont = pygame.font.SysFont("tahoma", 24)
bigFont = pygame.font.SysFont("tahoma", 56)



board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]

class Grid:
    def __init__(self, board, width, height):
        self.board = board
        self.row = len(self.board)
        self.col = len(self.board)
        self.width = width
        self.height = height

        self.cubes = [[Cubes(row, col) for col in range(9)] for row in range(9)]
        for row in range(9):
            for col in range(9):
                self.cubes[row][col].n = self.board[row][col]

                if self.cubes[row][col].n != 0:
                    # set puzzle numbers guess to -1 to prevent overriding
                    self.cubes[row][col].guess = -1
                #print(self.cubes[row][col].n)

        self.selected_cube = None

        self.mistakes = 0

    # draws current state to screen
    def render(self, win):
        win.fill((255,255,255))

        gap = self.width / 9
        for i in range(self.col + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            # vertical lines
            pygame.draw.line(win, (0,0,0), (i * gap, 0), (i * gap, self.height), thick)
            # horizontal lines
            pygame.draw.line(win, (0,0,0), (0, i * gap), (self.width, i * gap), thick)
        
        for row in range(9):
            for col in range(9):
                self.cubes[row][col].n = self.board[row][col]
                self.cubes[row][col].render(win)

    # checks if board is completed
    def is_finished(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return False

        # if none of the numbers are 0, the board is finished 
        return True

    def on_click(self, mouse_pos):
        if mouse_pos[1] < HEIGHT:
            # calculate which box is clicked
            row = int(mouse_pos[1] // (HEIGHT / 9))
            col = int(mouse_pos[0] // (WIDTH / 9))

            # if another cube is selected
            if self.selected_cube != None:
                self.selected_cube.selected = False
                
            self.cubes[row][col].selected = True
            self.selected_cube = self.cubes[row][col]
        
    def guess(self, key):
        # prvents overriding puzzle numbers
        if self.selected_cube.n == 0:
            self.selected_cube.guess = key

    # update when number is confirmed 
    def update(self):
        # cannot update puzzle squares
        if self.selected_cube.guess not in [0,-1]: 
            if possible(self.board, self.selected_cube.row, self.selected_cube.col, self.selected_cube.guess):
                self.selected_cube.n = self.selected_cube.guess
                self.selected_cube.guess = 0
                self.board[self.selected_cube.row][self.selected_cube.col] = self.selected_cube.n
            else:
                self.mistakes +=1
                self.selected_cube.guess = 0

    def clear(self):
        # cannot clear puzzle squares
        if self.selected_cube.guess != -1:
            self.selected_cube.n = 0
            self.selected_cube.guess = 0
            self.board[self.selected_cube.row][self.selected_cube.col] = 0

    def solve(self, win):
        # once board is solved return true to resolve stack
        if self.is_finished():
            return True

        # go through every box 
        for row in range(9):
            for col in range(9):

                # if box is blank
                if self.board[row][col] == 0:
                    # generate numbers to place in box
                    for n in range(1,10):

                        # chcek if number is valid
                        if possible(self.board, row, col, n):
                            self.board[row][col] = n
                            self.cubes[row][col].n = n
                            self.cubes[row][col].draw_change(win)
                            pygame.display.update()
                            #pygame.time.delay(1)

                            # call solve again to fill next box 
                            if self.solve(WIN):
                                return True

                            self.board[row][col] = 0
                            self.cubes[row][col].n = 0
                            self.cubes[row][col].draw_change(win)
                            pygame.display.update()
                            #pygame.time.delay(1)

                    # if all numbers not valid
                    return False
        print(self.board)

    def reset4solve(self):
        for row in self.cubes:
            for col in row:
                # if not puzzle square
                if col.guess != -1:
                    col.n = 0
                    col.guess = 0
                    self.board[col.row][col.col] = 0
    
    def reset4new(self):
        pass

class Cubes:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.n = 0
        # user input guess
        self.guess = 0

        self.x = WIDTH / 9 * self.col
        self.y = HEIGHT / 9 * self.row
        self.width = WIDTH / 9
        self.height = HEIGHT / 9
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.x_center = self.x + WIDTH / 9 / 2
        self.y_center = self.y + HEIGHT / 9 / 2
        
        self.selected = False

    def render(self, win):
        if self.selected: 
            pygame.draw.rect(win, (255,0,0), self.rect, width=2)
        
        if self.n != 0:
            img = numFont.render(str(self.n), True, (0,0,0))
            img_rect = img.get_rect(center= (self.x_center, self.y_center))
            win.blit(img, img_rect)

        if self.guess not in [0,-1]:
            img = numFont.render(str(self.guess), True, (150,150,150))
            img_rect = img.get_rect(center= (self.x_center, self.y_center))
            win.blit(img, img_rect)

    def draw_change(self, win):
        pygame.draw.rect(win, (255, 255, 255), pygame.Rect(self.x+10, self.y+10, self.width-20, self.height-20))
        if self.n != 0:
            img = numFont.render(str(self.n), True, (0,0,0))
            img_rect = img.get_rect(center= (self.x_center, self.y_center))
            win.blit(img, img_rect)

def update_stats(win, grid, time_passed, gameState):
    if gameState == "run":
        # displays number of mistakes
        img = smallFont.render("X: " + str(grid.mistakes), True, (0,0,0))
        img_rect = img.get_rect(center= (25, 570))
        win.blit(img, img_rect)

        # display solve msg
        solvemsg = smallFont.render("Press Space to solve", True, (0,0,0))
        solvemsg_rect = solvemsg.get_rect(center= (grid.width / 2, 570))
        win.blit(solvemsg, solvemsg_rect)

        # timer 
        timer = smallFont.render(str(datetime.timedelta(seconds=time_passed)), True, (0,0,0))
        timer_rect = timer.get_rect(center= (490, 570))
        win.blit(timer, timer_rect)
    elif gameState == "ans":
        # display next msg
        solvemsg = smallFont.render("Press Space to end", True, (0,0,0))
        solvemsg_rect = solvemsg.get_rect(center= (grid.width / 2, 570))
        win.blit(solvemsg, solvemsg_rect)
    
def game_finished(win, solved, player_time, com_time=0):
    win.fill((255,255,255))

    # if player manually solves 
    if solved:
        vic = bigFont.render("Victory!", True, (0,0,0))
        vic_rect = vic.get_rect(center= (WIDTH / 2, HEIGHT / 4))
        win.blit(vic, vic_rect)
    # if computer solves
    else:
        lose = bigFont.render("Game Over", True, (0,0,0))
        lose_rect = lose.get_rect(center= (WIDTH / 2, HEIGHT / 4))
        win.blit(lose, lose_rect)

    # display time taken 
    p_time = numFont.render("You took: " + str(datetime.timedelta(seconds=player_time)), True, (0,0,0))
    p_time_rect = p_time.get_rect(center= (WIDTH / 2, HEIGHT / 2 - 15))
    win.blit(p_time, p_time_rect)

    if com_time != 0:
        c_time = numFont.render("Computer took: " + str(datetime.timedelta(seconds=com_time)), True, (0,0,0))
        c_time_rect = c_time.get_rect(center= (WIDTH / 2, HEIGHT / 2 + 15))
        win.blit(c_time, c_time_rect)

    # display play again msg
    play_again = numFont.render("Press ENTER to play again", True, (0,0,0))
    play_again_rect = play_again.get_rect(center= (WIDTH / 2, HEIGHT / 4*3))
    win.blit(play_again, play_again_rect)

def resetAll(grid):
    # reset mistakes and time
    grid.mistakes = 0
    start_time = time.time()

    #grid.board = newboard

# main game logic here
def main():
    grid = Grid(board, WIDTH, HEIGHT)    
    clock = pygame.time.Clock()
    run = True
    key = None
    solved = True
    start_time = time.time()
    
    # gameStates: run, ans, end
    gameState = "run"

    while run:
        clock.tick(FPS)

        if gameState == "run":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONUP:
                    grid.on_click(pygame.mouse.get_pos())

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        key = 1
                    if event.key == pygame.K_2:
                        key = 2
                    if event.key == pygame.K_3:
                        key = 3
                    if event.key == pygame.K_4:
                        key = 4
                    if event.key == pygame.K_5:
                        key = 5
                    if event.key == pygame.K_6:
                        key = 6
                    if event.key == pygame.K_7:
                        key = 7
                    if event.key == pygame.K_8:
                        key = 8
                    if event.key == pygame.K_9:
                        key = 9
                    if event.key == pygame.K_BACKSPACE:
                        grid.clear()
                        key = None
                    if event.key == pygame.K_RETURN:
                        grid.update()
                    if event.key == pygame.K_SPACE:
                        player_time = round(time.time() - start_time)
                        grid.reset4solve()
                        grid.solve(WIN)
                        com_time = round(time.time() - start_time - player_time)
                        solved = False
                        gameState = "ans"

            # guess number if key and cube is selected 
            if key != None and grid.selected_cube != None:
                grid.guess(key)
                key = None

            grid.render(WIN)
            
            time_passed = round(time.time() - start_time)
            update_stats(WIN, grid, time_passed, gameState)
        
        # display the solved sudoku
        elif gameState == "ans":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and gameState == "ans": 
                            gameState = "end"
                
            grid.render(WIN)
            update_stats(WIN, grid, time_passed, gameState)

        # ending screen
        elif gameState == "end":
            # if player solved
            if solved:
                game_finished(WIN, solved, time_passed)
            # if com solved
            else: 
                game_finished(WIN, solved, player_time, com_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        resetAll(grid)
                        start_time = time.time()
                        gameState = "run"


        
        
        pygame.display.update()

main()
pygame.quit()
