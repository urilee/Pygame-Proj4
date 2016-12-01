#pygame file

import random
import sys
import pygame
import os

#pygame.init()
#dimensions for display screen
display_screen = screen_w, screen_h = 600, 600
screen = pygame.display.set_mode(display_screen)

#paddle
p_width = 100
p_height = 10
p_y = display_screen[0] - 50 #sets how high the paddle is
max_paddle = display_screen[0] - p_width

#ball
b_diameter = 20
b_radius = int(b_diameter / 2)
max_ball_x = display_screen[0] - b_diameter
max_ball_y = display_screen[1] - b_diameter

#colors
ball_color = (255, 255, 255) #white
paddle_color = (139, 137, 137) 

#constants
intro = 0
ball_in_paddle = 1
playing = 2
won = 3
game_over = 4

bg_image = (pygame.image.load(os.path.join('images','start.png')), pygame.image.load(os.path.join('images','game.png')),pygame.image.load(os.path.join('images','game2.png')), pygame.image.load(os.path.join('images','won.png')), pygame.image.load(os.path.join('images','lose.png')))

class Bricks(pygame.sprite.Sprite):

	def __init__(self):
		pygame.init()
		self.init_game()

	def init_game(self):
		self.lives = 3
		self.score = 0
		self.state = intro
		self.sound = pygame.mixer.Sound('power.wav')
		self.sound_lose = pygame.mixer.Sound('sad.wav')
		self.sound_win = pygame.mixer.Sound('yay.wav')

		self.paddle = pygame.Rect(200, p_y, p_width, p_height)
		self.ball = pygame.Rect(200, p_y - b_diameter, b_diameter, b_radius)
		self.ball_v = [4,-4]

		self.img = pygame.image.load(os.path.join('images','brick.png'))
		bricks = self.img.get_rect()
		self.brick_l = bricks.right - bricks.left
		self.brick_h = bricks.bottom - bricks.top	

		self.now_bricks()
		
	def now_bricks(self):
		y = 25
		self.bricks = []
		for i in range(4):
			x = 25
			for k in range(5):
				self.bricks.append(pygame.Rect(x,y,self.brick_l, self.brick_h))
				x += self.brick_l + 14
			y += self.brick_h + 5

	def draw_things(self):
		for brick in self.bricks:
			screen.blit(self.img, brick)
			
		pygame.draw.rect(screen, paddle_color, self.paddle)
		pygame.draw.circle(screen, ball_color, (self.ball.left + b_radius, self.ball.top + b_radius), b_radius)

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
	
		#when the ball is in the paddle - hit SPACE to start
		if keys[pygame.K_SPACE] and self.state == intro:
			self.state = playing
			self.ball.left = self.paddle.left + self.paddle.width / 2
			self.ball.top  = self.paddle.top - self.ball.height

		elif keys[pygame.K_SPACE] and self.state == ball_in_paddle:
			self.ball_v = [4,-4]
			self.state = playing

		elif keys[pygame.K_SPACE] and self.state == playing:
			self.ball_v = [4,-4]
			self.state = ball_in_paddle

		#when you completely win or lose all your lives - hit ENTER to restart the game
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
				self.sound.play()
				self.bricks.remove(brick)
				break

		if len(self.bricks) == 0:
			self.state = won

		#when ball hits the paddle
		if self.ball.colliderect(self.paddle):
			self.ball.top = p_y - b_diameter
			#reverses direction of the ball
			self.ball_v[1] = -self.ball_v[1]

		#status of the gamex
		elif self.ball.top > self.paddle.top:
			self.lives -= 1
			if self.lives > 0:
				self.state = ball_in_paddle
				self.ball.left = self.paddle.left + self.paddle.width / 2
				self.ball.top  = self.paddle.top - self.ball.height
			else:
				self.state = game_over


	def show_score(self):
		font = pygame.font.Font(None, 30)
		score = font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), True, (255,255,255))
		scorerect = score.get_rect()
		scorerect.centerx = screen.get_rect().centerx
		screen.blit(score, scorerect)

	def status_of_game(self):
		screen.blit(bg_image[self.state], (0,0, screen_w, screen_h), (0,0,screen_w, screen_h))
		
		if self.state == playing or self.state == ball_in_paddle:
			self.show_score()
			self.move_ball()
			self.handle_collisions()
			self.draw_things()

		elif self.state == intro:
			pygame.mixer.stop()
			pass

		elif self.state == game_over:
			self.show_score()
			self.sound_lose.play()
			pass

		elif self.state == won:
			self.show_score()
			self.sound_win.play()
			pass


	def run(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit
			
			self.play_game()
			self.status_of_game()


			pygame.display.set_caption("BREAKOUT")

			pygame.display.flip()

if __name__ == "__main__":
    Bricks().run()





