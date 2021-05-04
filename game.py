import pygame
import time
from solver import possible

# constants are in all caps
WIDTH, HEIGHT = 540, 540
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption("Sudoku")
pygame.font.init()
numFont = pygame.font.SysFont("tahoma", 32)
smallFont = pygame.font.SysFont("tahoma", 24)

FPS = 60
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
        
        # displays number of mistakes
        img = smallFont.render("X: " + str(self.mistakes), True, (0,0,0))
        img_rect = img.get_rect(center= (25, 570))
        win.blit(img, img_rect)

        # display solve msg
        solvemsg = smallFont.render("Press Space to solve", True, (0,0,0))
        solvemsg_rect = solvemsg.get_rect(center= (self.width / 2, 570))
        win.blit(solvemsg, solvemsg_rect)

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
                            pygame.time.delay(1)

                            # call solve again to fill next box 
                            if self.solve(WIN):
                                return True

                            self.board[row][col] = 0
                            self.cubes[row][col].n = 0
                            self.cubes[row][col].draw_change(win)
                            pygame.display.update()
                            pygame.time.delay(1)

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
        img = numFont.render(str(self.n), True, (0,0,0))
        img_rect = img.get_rect(center= (self.x_center, self.y_center))
        win.blit(img, img_rect)

# main game logic here
def main():
    grid = Grid(board, WIDTH, HEIGHT)

    #print(grid.board)  
    
    clock = pygame.time.Clock()
    run = True
    key = None

    while run:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                grid.on_click(mouse_pos)

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
                    grid.reset4solve()
                    grid.solve(WIN)
                    
            # guess number if key and cube is selected 
        if key != None and grid.selected_cube != None:
            grid.guess(key)
            key = None

        grid.render(WIN)
        pygame.display.update()

main()
pygame.quit()
