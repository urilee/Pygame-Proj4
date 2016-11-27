#pygame file

import random
import sys
import pygame

#dimensions for display screen
display_screen = 600, 600

#bricks
br_width = 50
br_height = 10

#paddle
p_width = 50
p_height = 15
p_y = display_screen[0] - p_width
max_paddle = display_screen[0] - p_width

#ball
b_diameter = 18
b_radius = int(b_diameter / 2)
max_ball_x = display_screen[0] - b_diameter
max_ball_y = display_screen[1] - b_diameter

#colors
background = (0, 0, 0)
ball_color = (255, 255, 255)
brick_color = (255, 0, 0)
paddle_color = (139, 137, 137)

#constants
ball_in_paddle = 0
playing = 1
won = 2
game_over = 3

class Bricks:
	def _init_(self):
		pygame.init()
		self.screen = pygame.display.set_mode(display_screen)
		self.clock = pygame.time.Clock()
		self.init_game()

	def init_game(self):
		self.lives = 5
		self.score = 0
		self.state = ball_in_paddle
#can draw text here later

		self.paddle = pygame.Rect(300, p_y, p_width, p_height)
		self.ball = pygame.Rect(300, p_y - b_diameter, b_diameter, b_radius)
		self.ball_v = [-5,5]

		self.now_bricks()

	def now_bricks(self):
		 y = 35
		 self.bricks = []
		 for x in range(7):
		 	z = 35
		 	for k in range(8):
		 		self.bricks.append(pygame.Rect(x,y,br_width, br_height))
		 		x += br_width + 10
	 		y += br_height + 5

	def check_input(self):
    	keys = pygame.key.get_pressed()
 
	    if keys[pygame.K_LEFT]:
	        self.paddle.left -= 5
	        if self.paddle.left < 0:
	            self.paddle.left = 0
	 
	    if keys[pygame.K_RIGHT]:
	        self.paddle.left += 5
	        if self.paddle.left > max_paddle:
	            self.paddle.left = max_paddle
	 
	    if keys[pygame.K_SPACE] and self.state == ball_in_paddle:
	        self.ball_v = [5,-5]
	        self.state = playing

	    elif keys[pygame.K_RETURN] and (self.state == game_over or self.state == won):
	        self.init_game()

    def draw_bricks(self):
    	for brick in self.bricks:
    		pygame.draw.rect(self.screen, brick_color, brick)
			

