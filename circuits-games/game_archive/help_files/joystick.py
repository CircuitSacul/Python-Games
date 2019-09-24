from sys import exit
import pygame
from pygame.locals import *

A = 0
B = 1
X = 2
Y = 3
L = 4
R = 5
SELECT = 6
START = 7
UP = {'value':-1.000030518509476, 'axis':1}
DOWN = {'value':1, 'axis':1}
RIGHT = {'value':1, 'axis':0}
LEFT = {'value':-1.000030518509476, 'axis':0}


if pygame.joystick.get_init():
	pygame.joystick.quit()
	pygame.quit()


pygame.init()
pygame.joystick.init()

print 'number of joysticks', pygame.joystick.get_count()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

print joysticks

j1 = joysticks[0]
j2 = joysticks[1]

j1.init()
j2.init()
screen = pygame.display.set_mode((100,100))
clock = pygame.time.Clock()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		try:
			if event.dict['value'] == UP['value'] and event.dict['axis'] == UP['axis']:
				print event
		except KeyError:
			pass
