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

#ball
b_diameter = 15
b_radius = (b_diameter / 2)
max_ball_x = display_screen[0] - b_diameter
max_ball_y = display_screen[1] - b_diameter

#colors
background = (0, 0, 0)
ball_color = (255, 255, 255)
brick_color = (255, 0, 0)
paddle_color = (139, 137, 137)

class Bricks:
	def _init_(self):
		pygame.init()
		self.screen = pygame.display.set_mode(display_screen)
		self.clock = pygame.time.Clocl()
		self.init_game()

	def init_game(self):
		self.lives = 5
		self.score = 0
		self.state = ball_paddle

		self.paddle = pygame.Rect(300, p_y, p_width, p_height)
		self.ball = pygame.Rect(300, p_y - b_diameter, b_diameter, b_radius)
		self.ball_v = [-5,5]

		self.now_bricks()

	def now_bricks(self):
		

