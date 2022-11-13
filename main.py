import time
import copy
import pygame
from pygame.locals import *

"""
Instruction:
1) Press K_RIGHT to see the result py steps
2) Press K_LEFT to activate auto mode
2) Press K_SPACE to interrupt the programm
"""


class GameOfLife:
    def __init__(self, width, height, cell_size, speed):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.speed = speed
        self.screen_size = width, height
        # Create outputting window
        self.screen = pygame.display.set_mode(self.screen_size)
        # Reckon the count of cells
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Create the array of cells
        self.list_cell = [[0] * self.cell_width for _ in range(self.cell_height)]

    def draw_lines(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def draw_cell(self):
        for y in range(0, self.height, self.cell_size):
            for x in range(0, self.width, self.cell_size):
                if self.list_cell[y//self.cell_size][x//self.cell_size] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(x, y, x+self.cell_size, y+self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(x, y, x+self.cell_size, y+self.cell_size))

    def start_play(self):
        """Rules of Game"""
        new_list = copy.deepcopy(self.list_cell)
        for y in range(1, self.cell_height-1):
            for x in range(1, self.cell_width-1):
                who_alive = self.list_cell[y-1][x-1] + self.list_cell[y-1][x] + self.list_cell[y-1][x+1] \
                            + self.list_cell[y][x-1] + self.list_cell[y][x+1] \
                            + self.list_cell[y+1][x-1] + self.list_cell[y+1][x] + self.list_cell[y+1][x+1]
                if self.list_cell[y][x] == 1:
                    if who_alive < 2 or who_alive > 3:
                        new_list[y][x] = 0
                else:
                    if who_alive == 3:
                        new_list[y][x] = 1
        self.list_cell = new_list

    def run(self):
        pygame.init()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    x_mouse, y_mouse = pygame.mouse.get_pos()
                    row = y_mouse // self.cell_size
                    column = x_mouse//self.cell_size
                    if self.list_cell[row][column] == 0:
                        self.list_cell[row][column] = 1
                    else:
                        self.list_cell[row][column] = 0

                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.start_play()
                    elif event.key == K_LEFT:
                        while running:
                            self.start_play()
                            self.draw_cell()
                            self.draw_lines()
                            pygame.display.update()
                            time.sleep(self.speed)
                            for ev in pygame.event.get():
                                if ev.type == KEYDOWN and ev.key == K_SPACE:
                                    running = False

            self.draw_cell()
            self.draw_lines()
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    """Width Height Cell_size Output_speed"""
    game = GameOfLife(400, 200, 20, 0.2)
    game.run()
