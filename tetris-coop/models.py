# models.py
import pygame
from config import CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT, BACKGROUND_COLOR, BORDER_COLOR, GRAY

class Tetromino:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, screen, offset_x, offset_y):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (
                            offset_x + (self.x + col_idx) * CELL_SIZE,
                            offset_y + (self.y + row_idx) * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE,
                        )
                    )

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.background_color = BACKGROUND_COLOR
        self.lines_cleared_count = 0

    def draw(self, screen, offset_x, offset_y):
        pygame.draw.rect(
            screen,
            self.background_color,
            (
                offset_x,
                offset_y,
                BOARD_WIDTH * CELL_SIZE,
                BOARD_HEIGHT * CELL_SIZE,
            )
        )
        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            (
                offset_x, offset_y,
                BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE
            ),
            3
        )
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.grid[row][col]:
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        (
                            offset_x + col * CELL_SIZE,
                            offset_y + row * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE,
                        )
                    )

    def check_collision(self, tetromino):
        # Método de colisión
        for row_idx, row in enumerate(tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = tetromino.x + col_idx
                    y = tetromino.y + row_idx
                    if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                        return True
                    if y >= 0 and self.grid[y][x] != 0:
                        return True
        return False

    def place_tetromino(self, tetromino):
        for row_idx, row in enumerate(tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = tetromino.x + col_idx
                    y = tetromino.y + row_idx
                    if y >= 0:
                        self.grid[y][x] = 1

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = BOARD_HEIGHT - len(new_grid)
        self.lines_cleared_count += lines_cleared
        self.grid = [[0] * BOARD_WIDTH for _ in range(lines_cleared)] + new_grid

    def is_game_over(self):
        return any(self.grid[1][col] for col in range(BOARD_WIDTH))
