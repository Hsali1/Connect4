import numpy as np
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def create_board():
    # Creates a matrix of 6 rows, 7 columns with 0's
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    # need to make sure that the top row of col is zero
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    # need to check which row the piece falls on
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        

def print_board(board):
    # flip board over the x axis
    print(np.flip(board, 0))


def winning_move(board, piece):
    # check all horizontal locations for winner
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
            
    # check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
            
    # check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), height - int(r * SQUARESIZE  + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), height - int(r * SQUARESIZE  + SQUARESIZE/2)), RADIUS)

    pygame.display.update()

board = create_board()
print_board(board)
game_over = False
turn = 0

# initialize pygame
pygame.init()

# define screen size
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)
size = (width, height)

screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

# game loop
while not game_over:

    for event in pygame.event.get():
        # be able to quit out of game
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # Ask for player 1 input
            if turn == 0:
                posx = event.pos[0]
                column = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 1)

                    if winning_move(board, 1):
                        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        label = myfont.render("Player 1 wins!!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            # Ask for player 2 input
            else:
                posx = event.pos[0]
                column = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 2)

                    if winning_move(board, 2):
                        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        label = myfont.render("Player 2 wins!!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            # alternate between 0 and 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)