print """The goal of this game is to be the last standing. Don't run into your opponents trails or your trails, and make sure to stay on the board.
Use the sdfe keys for first (blue) players left, down, right up, and jkli keys for the second (red) player."""
control_type = raw_input("Type j to play with joysticks or gamepads or type k to play with keyboard, then press enter.").lower()
speed_setting = raw_input("Choose game speed: s = slow, m = medium, f = fast(default)")
if speed_setting == 's':
	game_speed = 100
elif speed_setting == 'm':
	game_speed = 250
else:
	game_speed = 400

import pygame
from math import cos, sin, sqrt, pi
from time import sleep

pygame.quit()
pygame.joystick.quit()
pygame.init()
pygame.joystick.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 100)
pygame.display.set_caption("Tron")

joysticks = []
lines = []

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

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


def display_text(text, x, y, color):
        textsurface = myfont.render(text, False, color)
        screen.blit(textsurface, (x, y))

def get_joysticks():
        print "This game requires two joysticks/gamepads."
        waiting = True
        while waiting:
                if pygame.joystick.get_init(): #is joystick intialized
                        pygame.joystick.quit() #uninitialize joystick
                pygame.joystick.init() #re-initialize joystick
                if pygame.joystick.get_count() == 2: #are 2 joysticks connected
                        waiting = False
                        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())] #create list containing both joysticks
                        j1 = joysticks[0]
                        j1.init()
                        j2 = joysticks[1]
                        j2.init()
                        return j1, j2


def inclusive_range(x, z):
	if x > z:
		return range(z, x+1)
	else:
		return range(x, z+1)


class Line:
	def __init__(self, sx, sy, ex, ey, color): #start_x, start_y, end_x, end_y
		self.sx = sx
		self.sy = sy
		self.ex = ex
		self.ey = ey
		self.color = color
	def update(self):
		pygame.draw.line(screen, self.color, (self.sx, self.sy), (self.ex, self.ey), 1)


class Player:
	def __init__(self, joy_num, x, y, color, move_x):
		self.joy_num = joy_num
		self.x = x
		self.y = y
		self.sx = self.x
		self.sy = self.y
		self.color = color
		self.move_x = move_x
		self.move_y = 0
		self.lines = []
	def update(self, lines):
		self.lines[-1].ex = self.x
		self.lines[-1].ey = self.y
		if self.x >= screen_width or self.x <= 0 or self.y >= screen_height or self.y <= 0:
			display_text("Player {} ran into wall".format(self.joy_num), 10, 10, self.color)
			pygame.display.update()
			sleep(1)
			return False
		self.x += self.move_x
		self.y += self.move_y
		for line in lines:
			if self.x in inclusive_range(line.sx, line.ex):
				if self.y in inclusive_range(line.sy, line.ey):
					display_text("Player {} lost".format(self.joy_num), 10, 10, self.color)
					pygame.display.update()
					sleep(1)
					return False
		pygame.draw.rect(screen, self.color, (self.x-3, self.y-3, 6, 6))
	def new_line(self):
		self.sx = self.x
		self.sy = self.y
		self.lines.append(Line(self.sx, self.sy, self.x, self.y, self.color))


def main():
	running = True
	print(p1.move_y, p1.move_x)
	while running:
		lines = p2.lines + p1.lines
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if control_type == 'j':
				try:
                        		if event.dict['value'] != 0:
						if event.dict['joy'] == p1.joy_num:
							to_change = p1
							p1.new_line()
						else:
							to_change = p2
							p2.new_line()
						if event.dict['axis'] == 0:
							to_change.move_x = int(round(event.dict['value']))
							to_change.move_y = 0
						else:
							to_change.move_y = int(round(event.dict['value']))
							to_change.move_x = 0
                		except KeyError:
                        		pass
			else:
				try:
					key = event.dict['unicode'].lower()
					if key in [u's',u'f']:
						to_change = p1
						to_change.new_line()
					else:
						to_change = p2
						to_change.new_line()
					if key == u's' or key == u'j':
						to_change.move_y -= 1
						if to_change.move_y == -2:
							to_change.move_y = 0
						to_change.move_x -= 1
						if to_change.move_x == -2:
							to_change.move_x = 0
						print(to_change.move_x, to_change.move_y)
					elif key == u'f' or key == u'l':
						to_change.move_y += 1
						if to_change.move_y == 2:
							to_change.move_y = 0
						to_change.move_x += 1
						if to_change.move_x == 2:
							to_change.move_x = 0
						print(to_change.move_x, to_change.move_y)
				except:
					pass
		for line in lines:
			line.update()
		end = p2.update(lines)
		if end == False:
			return
		end = p1.update(lines)
		if end == False:
			return
		pygame.display.update()
		#clock.tick(game_speed)
		screen.fill((0, 0, 0))


while True:
	waiting = True
	while waiting:
		screen.fill(BLACK)
		display_text("Press Any Key", 10, 10, WHITE)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == 2:
				waiting = False
	if control_type == 'j':
        	j1, j2 = get_joysticks()
	p1 = Player(0, 1, 1, BLUE, 1)
	p2 = Player(1, 1, 100, RED, 1)
	p2.new_line()
	p1.new_line()
	main()

