#pygame file

import random
import sys
import pygame

pygame.init()
#dimensions for display screen
display_screen = 600, 600

#bricks
br_width = 50
br_height = 25

#paddle
p_width = 100
p_height = 10
p_y = display_screen[0] - 50 #sets how high the paddle is
max_paddle = display_screen[0] - p_width

#ball
b_diameter = 18
b_radius = int(b_diameter / 2)
max_ball_x = display_screen[0] - b_diameter
max_ball_y = display_screen[1] - b_diameter

#colors
background = (0, 0, 0) #black
ball_color = (255, 255, 255) #white
brick_color = (255, 0, 0)
paddle_color = (139, 137, 137)

#constants
ball_in_paddle = 0
playing = 1
won = 2
game_over = 3

class Bricks:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode(display_screen)
		self.clock = pygame.time.Clock()
		self.init_game()


	def init_game(self):
		self.lives = 5
		self.score = 0
		self.state = ball_in_paddle

		self.paddle = pygame.Rect(200, p_y, p_width, p_height)
		self.ball = pygame.Rect(200, p_y - b_diameter, b_diameter, b_radius)
		self.ball_v = [-4,4] #velocity of the ball

		self.now_bricks()

	def now_bricks(self):
		 y = 35
		 self.bricks = []
		 for x in range(7):
		 	z = 35
		 	for k in range(8):
		 		self.bricks.append(pygame.Rect(x,y,br_width, br_height))
		 		x += br_width + 25
	 		y += br_height + 5

	def draw_things(self):
		for brick in self.bricks:
			pygame.draw.rect(self.screen, brick_color, brick)
		pygame.draw.rect(self.screen, paddle_color, self.paddle)
		pygame.draw.circle(self.screen, ball_color, (self.ball.left + b_radius, self.ball.top + b_radius), b_radius)

	def play_game(self):
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
			self.ball_v = [4,-4]
			self.state = playing
		elif keys[pygame.K_RETURN] and (self.state == game_over or self.state == won):
			self.init_game()
	
	def move_ball(self):
		self.ball.left += self.ball_v[0]
		self.ball.top  += self.ball_v[1]

		if self.ball.left <= 0:
			self.ball.left = 0
			self.ball_v[0] = -self.ball_v[0]
		elif self.ball.left >= max_ball_x:
			self.ball.left = max_ball_x
			self.ball_v[0] = -self.ball_v[0]

		if self.ball.top < 0:
			self.ball.top = 0
			self.ball_v[1] = -self.ball_v[1]
		elif self.ball.top >= max_ball_y:
			self.ball.top = max_ball_y
			self.ball_v[1] = -self.ball_v[1]

	def handle_collisions(self):
		#removes bricks
		for brick in self.bricks:
			if self.ball.colliderect(brick):
				self.score += 10
				#reverses direction of the ball
				self.ball_v[1] = -self.ball_v[1]
				self.bricks.remove(brick)
				break

		if len(self.bricks) == 0:
			self.state = won

		#when ball hits the paddle
		if self.ball.colliderect(self.paddle):
			self.ball.top = p_y - b_diameter
			#reverses direction of the ball
			self.ball_v[1] = -self.ball_v[1]

		#status of the game
		elif self.ball.top > self.paddle.top:
			self.lives -= 1
			if self.lives > 0:
				self.state = ball_in_paddle
			else:
				self.state = game_over


	def show_message(self,message):
		if self.font:
			size = self.font.size(message)
			font_surface = self.font.render(message,False, ball_color)
			x = (display_screen[0] - size[0]) / 2
			y = (display_screen[1] - size[1]) / 2
			self.screen.blit(font_surface, (x,y))

	def run(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit

			#self.clock.tick(50)
			self.screen.fill(background)
			self.play_game()

			if self.state == playing:
				self.move_ball()
				self.handle_collisions()

			elif self.state == ball_in_paddle:
				self.ball.left = self.paddle.left + self.paddle.width / 2
				self.ball.top  = self.paddle.top - self.ball.height
				pygame.display.set_caption("PRESS SPACE TO LAUNCH THE BALL")

			elif self.state == game_over:
				pygame.display.set_caption("game over... press ENTER to play again")
			elif self.state == won:
				pygame.display.set_caption("Congrats!!! press Enter to play again")

			self.draw_things()
			
			pygame.display.set_caption("SCORE: " + str(self.score) + " LIVES: " + str(self.lives))


			pygame.display.flip()

if __name__ == "__main__":
    Bricks().run()


