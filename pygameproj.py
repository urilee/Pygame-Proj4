#Breakout version by Uriel Lee

import sys
import pygame
import os

#these are all constants
#dimensions for display screen
display_screen = screen_w, screen_h = 600, 600
screen = pygame.display.set_mode(display_screen)

#game state constants
intro = 0
ball_in_paddle = 1
playing = 2
won = 3
game_over = 4

#images for the background
background_image = (pygame.image.load(os.path.join('images','start.png')), pygame.image.load(os.path.join('images','game.png')),pygame.image.load(os.path.join('images','game2.png')), pygame.image.load(os.path.join('images','won.png')), pygame.image.load(os.path.join('images','lose.png')))


class Colors:

	ball_color = (255, 255, 255) #white
	paddle_color = (139, 137, 137) #snow

class Paddle(pygame.sprite.Sprite):

	def __init__(self):
		self.img = pygame.image.load(os.path.join('images','ship.png'))
		self.rect = self.img.get_rect()
		self.width = self.rect.right - self.rect.left
		self.height = self.rect.bottom - self.rect.top
		
		self.y = display_screen[0] - 70
		self.rect = pygame.Rect(200, self.y, self.width, self.height) #left, top, width, height

		#initial x and y position
		self.rect.x = 200
		self.rect.y = self.y
		self.max_paddle = display_screen[0] - self.width

class Bricks(pygame.sprite.Sprite):

	def __init__(self):
		self.img = pygame.image.load(os.path.join('images','brick.png'))
		self.rect = self.img.get_rect()
		#dimensions
		self.l = self.rect.right - self.rect.left
		self.h = self.rect.bottom - self.rect.top

class Ball(pygame.sprite.Sprite):

	def __init__(self):
		self.diameter = 20
		self.radius = int(self.diameter / 2)
		self.max_ball_x = display_screen[0] - self.diameter
		self.max_ball_y = display_screen[1] - self.diameter

		self.y = display_screen[0] - 70 #how high the paddle is
		self.rect = pygame.Rect(200, self.y - self.diameter, self.diameter, self.radius)

		#initial x and y position
		self.rect.x = 200
		self.rect.y = self.y

		#x and y velocity
		self.v = [6,-6]

class Game(pygame.sprite.Sprite):

	def __init__(self):
		pygame.init()
		self.init_game()

	def init_game(self):
		self.lives = 3
		self.score = 0
		self.state = intro

		#sounds
		self.sound = pygame.mixer.Sound(os.path.join('sounds','power.wav'))
		self.sound_lose = pygame.mixer.Sound(os.path.join('sounds','sad.wav'))
		self.sound_win = pygame.mixer.Sound(os.path.join('sounds','yay.wav'))

		self.bricks = Bricks()
		self.paddle = Paddle()
		self.ball = Ball()

		self.now_bricks()

	def now_bricks(self):
		#brick formation
		y = 25
		self.lists = []
		for i in range(4):
			x = 25
			for k in range(5):
				self.lists.append(pygame.Rect(x,y,self.bricks.l, self.bricks.h))
				x += self.bricks.l + 13
			y += self.bricks.h + 5

	def draw_things(self):
		#brick
		for brick in self.lists:
			screen.blit(self.bricks.img, brick)

		#paddle
		screen.blit(self.paddle.img, self.paddle)

		#ball
		pygame.draw.circle(screen, Colors.ball_color, [(self.ball.rect.x + self.ball.radius), (self.ball.rect.y + self.ball.radius)], self.ball.radius)

	def play_game(self):
		keys = pygame.key.get_pressed()

		#paddle movement
		if keys[pygame.K_LEFT]:
			self.paddle.rect.x -= 8
			if self.paddle.rect.x < 0:
				self.paddle.rect.x = 0

		if keys[pygame.K_RIGHT]:
			self.paddle.rect.x += 8
			if self.paddle.rect.x > self.paddle.max_paddle:
				self.paddle.rect.x = self.paddle.max_paddle
	
		#when the ball is in the paddle - hit SPACE to start
		if keys[pygame.K_SPACE] and self.state == intro:
			self.state = playing

		#when you completely win or lose all your lives - hit ENTER to restart the game
		elif keys[pygame.K_RETURN] and (self.state == game_over or self.state == won):
			self.init_game()

		#press ESC to end the game
		elif keys[pygame.K_ESCAPE]:
			self.state = game_over
		
		#press q to completely quite out of the game	
		elif keys[pygame.K_q]:
			pygame.quit()
			sys.exit()
	
	def ball_movement(self):
		self.ball.rect.x += self.ball.v[0] #x direction
		self.ball.rect.y  += self.ball.v[1] #y direction

		#makes sure that the ball stays in boundaries - reverses direction when hits wall
		#x position
		if self.ball.rect.x <= 0:
			self.ball.rect.x = 0
			self.ball.v[0] = -self.ball.v[0]

		elif self.ball.rect.x >= self.ball.max_ball_x:
			self.ball.rect.x = self.ball.max_ball_x
			self.ball.v[0] = -self.ball.v[0]

		#y position
		if self.ball.rect.y < 0:
			self.ball.rect.y = 0
			self.ball.v[1] = -self.ball.v[1]

		elif self.ball.rect.y >= self.ball.max_ball_y:
			self.ball.rect.y = self.ball.max_ball_y
			self.ball.v[1] = -self.ball.v[1]

	def collisions(self):
		#when ball hits bricks - removes bricks - reverses direction
		for brick in self.lists:
			if self.ball.rect.colliderect(brick):
				self.score += 10
				self.ball.v[1] = -self.ball.v[1]
				self.sound.play()
				self.lists.remove(brick)
				break

		#no more bricks in the list - winner
		if len(self.lists) == 0:
			self.state = won

		#when ball hits the top of the paddle - reverse
		if self.ball.rect.colliderect(self.paddle):
			self.ball.rect.y = self.ball.y - self.ball.diameter
			self.ball.v[1] = -self.ball.v[1]

		#when the ball goes past the paddle aka death
		elif self.ball.rect.y > self.paddle.rect.y:
			self.lives -= 1
			if self.lives > 0:
				self.state = ball_in_paddle
				self.ball.rect.x = self.paddle.rect.x + self.paddle.rect.width / 2
				self.ball.rect.y  = self.paddle.rect.y - self.ball.diameter
				#this prevents the game from immediately
			else:
				self.state = game_over

	def show_score(self):
		font = pygame.font.Font(None, 30)
		score = font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), True, (Colors.ball_color))
		scorerect = score.get_rect()
		scorerect.centerx = screen.get_rect().centerx #places score at the top center
		screen.blit(score, scorerect)

	def show_esc(self):
		font = pygame.font.Font(None, 20)
		text = font.render("press ESC to end game", True, (Colors.ball_color))
		textrect = text.get_rect()
		screen.blit(text, (445, 580))

	def show_quit(self):
		font = pygame.font.Font(None, 20)
		text = font.render("press Q to QUIT", True, (Colors.ball_color))
		textrect = text.get_rect()
		screen.blit(text, (480, 580))

	def status_of_game(self):
		screen.blit(background_image[self.state], (0,0, screen_w, screen_h), (0,0,screen_w, screen_h))
		
		if self.state == ball_in_paddle or self.state == playing:
			self.show_score()
			self.show_esc()
			self.ball_movement()
			self.collisions()
			self.draw_things()
			pygame.display.set_caption("KILL THE ALIENS!!")

		elif self.state == intro:
			pygame.display.set_caption("BREAKOUT")
			pygame.mixer.stop()

		elif self.state == game_over:
			self.show_score()
			self.sound_lose.play()
			pygame.display.set_caption("TRY AGAIN?")

		elif self.state == won:
			self.show_score()
			self.sound_win.play()
			pygame.display.set_caption("CONGRATS!!")

	def run(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			self.play_game()
			self.status_of_game()
			self.show_quit()

			pygame.display.flip()

if __name__ == "__main__":
    Game().run()



