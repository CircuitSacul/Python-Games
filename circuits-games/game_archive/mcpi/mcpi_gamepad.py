from mcpi import minecraft
from sys import exit
import pygame
from pygame.locals import *

try:
	mc = minecraft.Minecraft.create()
except:
	print "No game to connect, please start up mcpi and join world, then press \"a\" on your game pad"
print "Connected to mcpi"


pygame.init()
pygame.joystick.init()

screen = pygame.display.set_mode((100, 100))

clock = pygame.time.Clock()

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

def user_choice():
	print "Up, down, left, right: teleports"
	print "L, R: teleports up and down"

def refresh_gamepad():
	if pygame.joystick.get_init():
		pygame.joystick.quit()
	pygame.joystick.init()
	if pygame.joystick.get_count() >= 1:
		joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
		gamepad = joysticks[0]
		gamepad.init()
		print "{} joystick(s) connected. Only one will be used.".format(pygame.joystick.get_count())
		return True
	else:
		return False

def startup():
	print "Please connect gamepad"
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
		connected_gamepad = refresh_gamepad()
		if connected_gamepad:
			print "connected"
			waiting = False
			return True

def update_pos(x, y, z):
	mc.player.setPos(x, y, z)

startup()
user_choice()


while True:
	for event in pygame.event.get():
		pos = mc.player.getPos()
		try:
			if event.dict['axis'] == 0:
				update_pos(pos.x+event.dict['value'], pos.y, pos.z)
			elif event.dict['axis'] == 1:
				update_pos(pos.x, pos.y, pos.z+event.dict['value'])
		except KeyError:
			try:
				if event.dict['button'] == 5 and event.type == 10:
					update_pos(pos.x, pos.y+1, pos.z)
				elif event.dict['button'] == 4 and event.type == 10:
					update_pos(pos.x, pos.y-1, pos.z)
			except KeyError:
				pass
