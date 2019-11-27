def colored(r, g, b, text):
	return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


print("\033[2J")
print("\033[0;0H")

print(colored(0, 255, 255, "##########READ ME##########"))
print("""The goal of this game is to be the last standing. Don't run into your opponents trails or your trails, and make sure to stay on the board.
Use the sdfe keys for first (blue) players left, down, right up, and jkli keys for the second (red) player. 
NOTE: Click on the output section when the board says press any key.""")
print(colored(0,255,255,"###########READ ME##########"))

control_type = input("Type j to play with joysticks or gamepads or type k to play with keyboard, then press enter.").lower()

speed_setting = input("Choose game speed: s = slow, m = medium, f = fast(default)")

if speed_setting == 's':
	game_speed = 100
elif speed_setting == 'm':
	game_speed = 200
else:
	game_speed = 1000

print("Importing libraries")
try:
	import pygame, os, sys
	from math import cos, sin, sqrt, pi
	from time import sleep
except:
	print(colored(255, 0, 0, "Please make sure you have the following libraries installed:"))
	print("PyGame")
	print("Math")
	print("Time")

print("Initializing PyGame")
pygame.quit()
pygame.joystick.quit()
pygame.init()
pygame.joystick.init()

screen_width = 400
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 50)
pygame.display.set_caption("Tron")

joysticks = []
lines = []
joystick_timeout = 30

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

print("\033[2J")
print("\033[0;0H")

def display_text(text, x, y, color):
	textsurface = myfont.render(text, False, color)
	screen.blit(textsurface, (x, y))

def get_joysticks():
	waiting = True
	seconds = 0
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
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
		else:
			screen.fill(BLACK)
			display_text("Please insert joysticks", 10, 10, WHITE)
			pygame.display.update()
		sleep(1)
		seconds += 1
		if seconds == joystick_timeout:
			screen.fill(BLACK)
			display_text("Timed Out", 10, 10, RED)
			pygame.display.update()
			sleep(1)
			sys.exit()


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
	while running:
		lines = p2.lines + p1.lines
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
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
					if key in [u's',u'd',u'f',u'e']:
						to_change = p1
						to_change.new_line()
					else:
						to_change = p2
						to_change.new_line()
					if key == u's' or key == u'j':
						to_change.move_y = 0
						to_change.move_x = -1
					elif key == u'd' or key == u'k':
						to_change.move_y = 1
						to_change.move_x = 0
					elif key == u'f' or key == u'l':
						to_change.move_y = 0
						to_change.move_x = 1
					elif key == u'e' or key == u'i':
						to_change.move_y = -1
						to_change.move_x = 0
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
		clock.tick(game_speed)
		screen.fill((0, 0, 0))

try:
	pygame.init()
	while True:
		waiting = True
		if control_type == 'j':
			j1, j2 = get_joysticks()
		while waiting:
			screen.fill(BLACK)
			if control_type != 'j':
				display_text("Press Any Key", 10, 10, WHITE)
			else:
				display_text("Press Any Button", 10, 10, WHITE)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == 2:
					waiting = False
		p1 = Player(0, 10, 10, BLUE, 1)
		p2 = Player(1, screen_width-10, screen_height-10, RED, -1)
		p2.new_line()
		p1.new_line()
		main()
finally:
	print("\033[2J")
	print("\033[0;0H")
	print(colored(0, 150, 255, "Thanks for playing!"))
	pygame.quit()
	sys.exit()
