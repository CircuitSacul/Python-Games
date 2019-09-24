import pygame, math, random
import numpy as np
from time import sleep

pygame.init()

screen_width = 300
screen_height = 500

WALL = 1
CAR = 2

computers = []
blit_speed = 10
game_speed = 0

screen = pygame.display.set_mode((screen_width, screen_height))
board = np.zeros(screen_width*screen_height)
board = board.reshape(screen_height, screen_width)

board[:, screen_width-1] = WALL
board[:, 0] = WALL


class Car:
	def __init__(self, center_pos, uddirection, img):
		self.x, self.y = center_pos
		self.move_x = uddirection
		self.img = img
		self.rect = self.img.get_rect()
		self.rect.center = (self.x, self.y)
	def check_collision(self):
		for x in board[self.rect.top-1:self.rect.bottom+1, self.rect.left-1:self.rect.right+1]:
			if x != 0:
				return True
		return False
	def update(self):
		self.x += self.x_move
		self.rect.center = (self.x, self.y)
		if self.check_collision() == True:
			self.x -= self.x_move
	def blit(self):
		pygame.display.blit(self.img, self.rect)

def main():
	player = Car((screen_width/2, screen_height-50), car_img)
	blit_countdown = blit_speed
	game_countdown = game_speed
	while True:
		if game_countdown == 0:
			game_countdown = game_speed
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if random.randint(0, 10) == 5:
				computers.append(Car((player.x, player.y), 1, car_img))
			for computer in computers:
				computer.update()
				if computer.x >= screen_height:
					computers.pop(computer)
			player.update()
		if blit_countdown == 0:
			blit_countdown = blit_speed
			screen.fill((0, 0, 0))
			for computer in computers:
				computer.blit()
			player.blit()
			pygame.display.flip()
		blit_countdown -= 1
		game_countdown -= 1

if __name__ == '__main__':
	main()
