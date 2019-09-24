import pygame, random
from math import cos, sin, sqrt, pi

pygame.quit()
pygame.joystick.quit()
pygame.init()
pygame.joystick.init()
pygame.key.set_repeat(1, 50)
pygame.mouse.set_visible(False)


screen_width = 600
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
pygame.display.set_caption("Ball Buster")

joysticks = []
balls_in_play = []

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

player_lives = 3
player_shoot_countdown = 20

ball_move_countdown = 0

bullet_jump_speed = 10
bullet_move_countdown = 0
bullet_damage = 100

game_fps = 120


def display_text(text, x, y):
        textsurface = myfont.render(text, False, (255,255,255))
        screen.blit(textsurface, (x, y))


class Ball:
	def __init__(self, lvl, strength, x, y):
		self.lvl = lvl
		self.r = self.lvl*20
		self.start_strength = strength
		self.strength = strength
		self.exists = True
		self.move_countdown = ball_move_countdown
		self.countdown = self.move_countdown
		self.x = x
		self.y = y
		self.move_x = random.randint(-10, 10)/10
		self.move_y = random.randint(-10, 10)/10
	def update(self):
		self.countdown -= 1
		if self.countdown <= 0:
			self.countdown = self.move_countdown
			self.x += self.move_x
			self.y += self.move_y
			if self.strength <= 0:
				self.exists = False
				if self.lvl > 1:
					for i in range(0, 1):
						balls_in_play.append(Ball(self.lvl - 1, self.start_strength, self.x, self.y))
			if self.x >= screen_width or self.x <= 0:
				self.move_x = self.move_x*-1
			if self.y >= screen_height or self.y <= 0:
				self.move_y = self.move_y*-1
		pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), int(self.r), 0)


class Player:
	def __init__(self):
		self.lives = player_lives
		self.shoot_countdown = player_shoot_countdown
		self.countdown_s = self.shoot_countdown
		self.bullets = []
		self.x = screen_width/2
		self.y = screen_height - 10
	def update(self):
		self.countdown_s -= 1
		if self.countdown_s <= 0:
			self.countdown_s = self.shoot_countdown
			self.bullets.append(Bullet(self.x, self.y,1, 0))
			self.bullets.append(Bullet(self.x, self.y,-1,0))
			self.bullets.append(Bullet(self.x, self.y,0, 1))
			self.bullets.append(Bullet(self.x, self.y,0,-1))
		for x, bullet in enumerate(self.bullets):
			bullet.update()
			if bullet.alive == False:
				del self.bullets[x]
		pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), int(5), 0)


class Bullet:
	def __init__(self, x, y, mv_x, mv_y):
		self.x = x
		self.y = y
		self.move_countdown = bullet_move_countdown
		self.countdown = self.move_countdown
		self.damage = bullet_damage
		self.alive = True
		self.mv_x = mv_x
		self.mv_y = mv_y
	def update(self):
		self.countdown -= 1
		if self.countdown <= 0:
			self.countdown = self.move_countdown
			self.y += bullet_jump_speed*self.mv_y
			self.x += bullet_jump_speed*self.mv_x
		if self.x > screen_width or self.x < 0 or self.y > screen_height or self.y < 0:
			self.alive = False
		for ball in balls_in_play:
			if self.x in range(ball.x-ball.r, ball.x+ball.r):
				if self.y in range(ball.y-ball.r, ball.y+ball.r):
					self.alive = False
					ball.strength -= self.damage
		pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), int(2), 0)


player = Player()
for i in range(0, 100):
	balls_in_play.append(Ball(5, 20, 10, 10))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	screen.fill(BLACK)
	player.x, player.y = pygame.mouse.get_pos()
	player.update()
	for x, ball in enumerate(balls_in_play):
		if ball.exists == False:
			del balls_in_play[x]
		ball.update()
	pygame.display.update()
	clock.tick(game_fps)

