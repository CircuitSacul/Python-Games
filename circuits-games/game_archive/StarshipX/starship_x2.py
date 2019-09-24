#notes:
#angle_num is 1 - 360
#angle = (angle_num*pi)/180
#y-angle = sin(angle)
#x-angle = cos(angle)

import pygame
import random
from pygame.locals import *
from math import cos, sin, sqrt, pi

screen_x = 1000
screen_y = 1000

pygame.init()
pygame.key.set_repeat(1, 1)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_y, screen_x))
gamefont = pygame.font.SysFont('Comic Sans MS', 30)

#images
myimg = pygame.image.load('small_triangle.png').convert()

all_borg = []
borg_shots = []
player_shots = []

#shot types
BOMB = {'id':1, 'speed':0, 'dmg':10, 'img':myimg, 'fire_rate':100} #explosive, doesn't move
BULLET = {'id':2, 'speed':20, 'dmg':3, 'img':myimg, 'fire_rate':25} #normal
LASER = {'id':3, 'speed':200, 'dmg':2, 'img':myimg, 'fire_rate':0} #passes throught, very high speed
MISSILE = {'id':4, 'speed': 10, 'dmg':5, 'img':myimg, 'fire_rate':75} #moves, explosive, slower than bullet

fire_types = [BOMB, BULLET, LASER, MISSILE]
current_fire_type = 2

NUM_BORG = 1


def abs(number):
	return sqrt(number**2)


class Shot:
	def __init__(self, x, y, angle_num, type):
		self.x = x
		self.y = y
		self.img = type['img']
		self.speed = type['speed']
		self.damgae = type['dmg']
		self.angle_num = angle_num
		self.type = type
	def update(self):
		angle = (self.angle_num*pi)/180
		self.x += cos(angle)*self.speed
		self.y += sin(angle)*self.speed
		screen.blit(self.img, (self.x, self.y))


class Borg:
	def __init__(self, x, y, img, strength, speed, angle_num, fire_type):
		self.x = x
		self.y = y
		self.img = img
		self.strength = strength
		self.speed = speed
		self.fire_rate = fire_type['fire_rate']
		self.fire_countdown = self.fire_rate
		self.fire_type = fire_type
		self.angle_num = 0
	def shoot(self):
		borg_shots.append(Shot(self.x, self.y, self.angle_num, self.fire_type))

	def update(self):
		self.fire_countdown -= 1
		angle = (self.angle_num*pi)/180
		self.x += self.speed*cos(angle)
		self.y += self.speed*sin(angle)
		if self.fire_countdown <= 0:
			self.shoot()
			self.fire_countdown = self.fire_rate
		screen.blit(self.img, (self.x, self.y))


class Player:
	def __init__(self, x, y, img, strength, speed, angle_num, fire_type):
		self.x = x
		self.y = y
		self.img = img
		self.strength = strength
		self.speed = speed
		self.angle_num = angle_num
		self.fire_rate = fire_type['fire_rate']
		self.fire_countdown = self.fire_rate
		self.fire_type = fire_type
	def shoot(self):
		player_shots.append(Shot(self.x, self.y, self.angle_num, self.fire_type))
        def change_fire_type(self, new_fire_type):
                self.fire_type = new_fire_type
                self.fire_rate = self.fire_type['fire_rate']
                self.fire_countdown = self.fire_rate
	def update(self, shoot):
		self.fire_countdown -= 1
		if shoot == True and self.fire_countdown <= 0:
			self.shoot()
			self.fire_countdown = self.fire_rate
		angle = (self.angle_num*pi)/180
		self.x += cos(angle)*self.speed
		self.y += sin(angle)*self.speed
		screen.blit(self.img, (self.x, self.y))


for i in range(0, NUM_BORG): #initialize borg ships
	all_borg.append(Borg(25, 25, myimg, 3, 5, 0, BULLET))

player = Player(500, 500, myimg, 3, 5, 0, fire_types[current_fire_type]) #initialize player

player_to_shoot = False

print "RIGHT and LEFT ARROW = ROTATE RIGHT and LEFT. 1 = BOMB, 2 = BULLET, 3 = LASER, 4 = MISSILE. Press SPACE BAR to SHOOT."
print "Press SPACE BAR to BEGIN"

start_game = False

while start_game == False: #wait until space bar is pressed to start game
	for event in pygame.event.get():
		if event.type == 2: #is input from keyboard
			if event.dict['scancode'] == 65: #if is space bar
				start_game = True


while 1:
	for event in pygame.event.get():
		if event.type == 2:
			if event.dict['scancode'] == 114: #arrow right
				player.angle_num += 5
			elif event.dict['scancode'] == 113: #arrow left
				player.angle_num += -5
			elif event.dict['scancode'] == 111: #arrow up
				current_fire_type += 1
				if current_fire_type == 4:
					current_fire_type = 0
				player.change_fire_type(fire_types[current_fire_type])
			elif event.dict['scancode'] == 116: #arrow down
				pass
			if event.dict['scancode'] == 65: #space bar
				player_to_shoot = True
#		if event.type == EXIT():
#			exit()
	screen.fill((0,0,0))
	player.update(player_to_shoot)
	player_to_shoot = False
	player_mv_dis = 0
	for borg in all_borg:
		borg.update()
	for x, shot in enumerate(borg_shots):
		shot.update()
		if shot.x > screen_x or shot.x < 0 or shot.y > screen_y or shot.y < 0:
			del borg_shots[x]
	for x, shot in enumerate(player_shots):
		shot.update()
		if shot.x > screen_x or shot.x < 0 or shot.y > screen_y or shot.y < 0:
			del player_shots[x]
		print "shot in use"
	pygame.display.update()
	clock.tick(40)
