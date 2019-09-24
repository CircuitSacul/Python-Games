import pygame, sys, os, math
from time import sleep
import numpy as np

screen_width = 600
screen_height = 600
pygame.init()
SCREEN = pygame.display.set_mode((screen_width, screen_height))
board = np.zeros(screen_width*screen_height)
board = board.reshape(screen_height, screen_width)

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
backends = ['midleft', 'midtop', 'midright', 'midbottom']

board[0, :] = 3
board[screen_height-1, :] = 3
board[:,0] = 3
board[:,screen_width-1] = 3

bike1 = pygame.image.load('bike1.png').convert_alpha()
bike2 = pygame.image.load('bike2.png').convert_alpha()

update_rects = []

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Player:
	def __init__(self, pos, color, ID, img):
		self.direction = 0
		self.pos = pos
		self.original_img = img
		self.img = img
		self.color = color
		self.ID = ID
		self.img_rect = self.img.get_rect()
		self.to_move = directions[self.direction]
		self.facing = (0, 0)
		self.img_rect.topleft = self.pos
		self.pixels = []
		self.angle = 0
		self.backend = backends[0]
		self.pixels = []

	def update(self):
		global update_rects
		if self.direction == 4:
			self.direction = 0
		elif self.direction == -1:
			self.direction = 3
		if self.facing != directions[self.direction]:
			self.to_move = directions[self.direction]
			self.rotate()
			self.facing = self.to_move
		if self.to_move[0] != 0 or self.to_move[1] != 0:
			spawn_pos = self.pos
			update_rects.append(self.img_rect)
			board[self.pos[1], self.pos[0]] = 0
			sx, sy = spawn_pos
			self.pos = (self.to_move[0]+x, self.to_move[1]+y)
			if self.check_collision(self.img_rect) == True:
				sleep(2)
				print "GAME OVER"
				print "PLAYER {} LOST".format(self.ID)
				pygame.quit()
				sys.exit()
			self.img_rect = self.img.get_rect()
			self.img_rect.center = self.pos
			self.pixels.append((x, y))
			board[x,y] = self.ID
			board[self.pos[1], self.pos[0]] = self.ID
			update_rects.append(self.img_rect)

	def rotate(self):
		self.angle = (self.direction+1)*(-90)
		self.backend = backends[self.direction]
		print self.backend
		self.img = pygame.transform.rotate(self.original_img, self.angle)

	def check_collision(self, rect):
		for row in board[rect.top:rect.bottom, rect.left:rect.right]:
		#for row in board[self.pos[0], self.pos[1]]:
			for x in row:
				if x != 0:
					return True
		return False

	def blit(self):
		print "hi"
		SCREEN.blit(self.img, self.img_rect)
		pixelobj = pygame.PixelArray(SCREEN)
		for pixel in self.pixels:
			x, y = pixel
			pixelobj[x, y] = self.color
		#self.pixels = []
		pixelobj.transpose()


def main():
	global update_rects
	update_rects = []
	player1 = Player((50, 50), BLUE, 1, bike1)
	player2 = Player((50, 150), RED, 2, bike2)
	blit_speed = 10
	game_speed = 0
	blit_countdown = blit_speed
	game_countdown = game_speed
	while True:
		if game_countdown == 0:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == 2:
					if event.dict['key'] == 275: #right arrow
						player1.direction += 1
					elif event.dict['key'] == 276: #left arrow
						player1.direction -= 1
					elif event.dict['unicode'] == u's':
						player2.direction -= 1
					elif event.dict['unicode'] == u'f':
						player2.direction += 1
			game_countdown = game_speed+1
			player1.update()
			player2.update()
		if blit_countdown == 0:
			blit_countdown = blit_speed+1
			SCREEN.fill(BLACK)
			player1.blit()
			player2.blit()
			#pygame.display.flip()
			pygame.display.update(update_rects)
			update_rects = []
		blit_countdown -= 1
		game_countdown -= 1


#try:
main()
#except Exception, e:
	#print "An error occured."
	#print Exception, e
#finally:
	#print "Thank you for playing"
