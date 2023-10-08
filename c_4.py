import pygame
import numpy
import math
import time

from pygame import font


class ConnectFour:
    '''
    Class representing the connect four game
    '''
    player_one_colour = (235, 0, 0)
    player_two_colour = (255, 255, 0)
    background_colour = (240, 240, 240)
    board_colour = (0, 0, 255)
    number_of_rows = 6
    number_of_columns = 7
    tile_frame_height = 100
    score_board_height = 50
    scoreboard_background_colour = (210, 210, 210)
    winning_player_number = 1
    final_score_message = ''
    board = numpy.zeros((number_of_rows, number_of_columns))
    current_player = 1
    game_won = False
    player_1_count = 0
    player_2_count = 0

    def __init__(self):
        '''
        The game is run when the constructor is called, thus everytime a new object of this class is created, the
        game is automatically played.
        '''
        pygame.init()  # Initialize pygame
        pygame.display.set_caption('Connect Four')
        self.window_width = self.number_of_columns * self.tile_frame_height
        self.window_height = (self.number_of_columns * self.tile_frame_height) + (self.score_board_height*2)

        self.screen_size = (self.window_width, self.window_height)

        self.circle_radius = int(
            self.tile_frame_height / 2) - 5  # Allow player circle tiles have a padding/spacing of 5

        self.screen = pygame.display.set_mode(self.screen_size)
        self.draw_board()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    # Draws the surface object to the screen.
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.window_width, self.tile_frame_height))
                    position_x = event.pos[0]
                    current_tile_colour = self.player_one_colour if self.current_player == 1 else self.player_two_colour
                    pygame.draw.circle(self.screen, current_tile_colour,
                                       (position_x, int(self.tile_frame_height / 2)),
                                       self.circle_radius)
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_x = event.pos[0]  # current x-location of the mouse click
                    tile_column = int(
                        math.floor(position_x / self.tile_frame_height))  # get column of the current click
                    self.play_turn(tile_column)
                    self.print_board()
                    pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.window_width, self.tile_frame_height))
                    pygame.display.update()

    def draw_board(self):
        column_count = self.number_of_columns
        row_count = self.number_of_rows
        board_colour = self.board_colour
        background_colour = self.background_colour
        tile_frame_height = self.tile_frame_height
        screen_width = self.window_width
        screen_height = self.window_height
        score_board_height = self.score_board_height
        self.final_score_message = ''

        for row in range(row_count):
            #  Draw each row with a blue colour
            pygame.draw.rect(self.screen, board_colour, (0, (row + 1) * tile_frame_height,
                                                         screen_width, tile_frame_height))
            # time.sleep(0.5)
            pygame.display.update()

            for column in range(column_count):
                #  Draw each circle in the current row
                pygame.draw.circle(self.screen, self.background_colour,
                                   (int(column * tile_frame_height + tile_frame_height / 2),
                                    int(row * tile_frame_height + tile_frame_height + tile_frame_height / 2)),
                                   self.circle_radius)
                # time.sleep(0.5)
                pygame.display.update()

        # Draw the score board at the bottom
        pygame.draw.rect(self.screen, background_colour, (0, screen_height - (score_board_height*2), screen_width,
                                                          score_board_height))
        font = pygame.font.SysFont("Times new Roman", 50)
        score_text = font.render(self.final_score_message, True, (158, 16, 16))
        self.screen.blit(score_text,
                         ((screen_width - score_text.get_width()) / 2, screen_height - (score_board_height*2)))

        # Draw score counter
        pygame.draw.rect(self.screen, (210, 210, 210), (0, screen_height - score_board_height, screen_width,
                                                        score_board_height))
        score_counter_font = pygame.font.SysFont("Times new Roman", 40)
        counter_text = f'Player 1   {self.player_1_count}   :   {self.player_2_count}   Player 2'
        score_counter_text = score_counter_font.render(counter_text, True, (158, 16, 16))
        self.screen.blit(score_counter_text,
                         ((screen_width - score_counter_text.get_width()) / 2, screen_height - score_board_height))

        pygame.display.update()


    def play_turn(self, column):
        board = self.board
        current_tile_colour = self.player_one_colour if self.current_player == 1 else self.player_two_colour
        is_column_open = board[0][column] == 0
        if is_column_open:
            for current_row in range(self.number_of_rows, 0, -1):
                if board[current_row - 1][column] == 0:
                    board[current_row - 1][column] = self.current_player
                    pygame.draw.circle(self.screen, current_tile_colour,
                                       (int(column * self.tile_frame_height + self.tile_frame_height / 2),
                                        int(current_row * self.tile_frame_height + self.tile_frame_height / 2)),
                                       self.circle_radius)
                    # time.sleep(0.5)
                    pygame.display.update()
                    if self.check_if_play_wins(board):
                        self.final_score_message = f'Player {self.current_player} Wins'
                        if self.current_player == 1:
                            self.player_1_count = self.player_1_count + 1
                        else:
                            self.player_2_count = self.player_2_count + 1
                        self.redraw_score_board()
                    else:
                        self.current_player = 1 if self.current_player == 2 else 2
                    break

    def print_board(self):
        print(self.board)

    def check_if_play_wins(self, board):
        player_number = self.current_player

        # Check if win is horizontal
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns-3):
                if board[i][j] == player_number == board[i][j+1] == board[i][j+2] == board[i][j+3]:
                    return True

        # Check if win is vertical
        for i in range(self.number_of_rows - 3):
            for j in range(self.number_of_columns):
                if board[i][j] == player_number == board[i + 1][j] == board[i + 2][j] == board[i + 3][j]:
                    return True

        # Check if win is negative slope
        for i in range(self.number_of_rows - 3):
            for j in range(self.number_of_columns - 3):
                if board[i][j] == player_number == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                    return True

        # Check if win is positive slope
        for i in range(self.number_of_rows - 3):
            for j in range(self.number_of_columns - 1, 0, -1):
                if board[i][j] == player_number == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3]:
                    return True

        return False

    def redraw_score_board(self):
        board_colour = self.board_colour
        background_colour = self.background_colour
        screen_width = self.window_width
        screen_height = self.window_height
        score_board_height = self.score_board_height
        # Redraw the score board at the bottom to show the player wins message
        pygame.draw.rect(self.screen, background_colour,
                         (0, screen_height - (score_board_height*2), screen_width,
                          score_board_height))
        font = pygame.font.SysFont("Times new Roman", 50)
        score_text = font.render(self.final_score_message, True, (158, 16, 16))
        self.screen.blit(score_text,
                         ((self.window_width - score_text.get_width()) / 2,
                          self.window_height - (score_board_height*2)))

        pygame.display.update()
        time.sleep(1.2)
        self.draw_board()
        # Redraw the score board at the bottom to remove the 'Player <> Wins' text'
        pygame.draw.rect(self.screen, background_colour,
                         (0, screen_height - score_board_height, screen_width,
                          score_board_height))
        font = pygame.font.SysFont("Times new Roman", 50)
        score_text = font.render('', True, (158, 16, 16))
        self.screen.blit(score_text,
                         ((self.window_width - score_text.get_width()) / 2,
                          self.window_height - (score_board_height*2)))

        # Update score counter with the new score
        pygame.draw.rect(self.screen, (210, 210, 210), (0, screen_height - score_board_height, screen_width,
                                                        score_board_height))
        score_counter_font = pygame.font.SysFont("Times new Roman", 40)
        counter_text = f'Player 1   {self.player_1_count}   :   {self.player_2_count}   Player 2'
        score_counter_text = score_counter_font.render(counter_text, True, (158, 16, 16))
        self.screen.blit(score_counter_text,
                         ((screen_width - score_counter_text.get_width()) / 2, screen_height - score_board_height))
        self.reset_board()

    def reset_board(self):
        self.current_player = 1
        self.board = numpy.zeros((self.number_of_rows, self.number_of_columns))
# jnvnv
