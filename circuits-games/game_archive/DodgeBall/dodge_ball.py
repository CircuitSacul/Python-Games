import random
import pygame
from pygame.locals import * #so we have all locals, without have to type pygame. first

pygame.quit()	#quit and re-init pygame
pygame.joystick.quit()
pygame.init()
pygame.joystick.init()

screen = pygame.display.set_mode((600, 700))
screen.fill((255,255,255))
pygame.display.update
clock = pygame.time.Clock()

p1_fig = pygame.image.load('small_triangle.png').convert()
p2_fig = pygame.image.load('small_square.png').convert()
ball_img = pygame.image.load('small_ball.jpg').convert()

players = {}
balls = {}

def safe_input(type, prompt): # so game doesn't crash if player doesn't enter correct type, like if they enter a string instead of an int
	if type == 'int':
		try:
			response = int(raw_input(prompt))
		except:
			print 'not an int'
			return safe_input(type, prompt)
	elif type == 'float':
		try:
			response = float(raw_input(prompt))
		except:
			print 'not a float'
			return safe_input(type, prompt)
	return response

class ball:
	def __init__(self):
		try:
			self.x_pos = players[random.choice(('p1','p2'))].x_pos + random.randint(-50, 50)
		except KeyError:
			self.x_pos = random.randint(100, 500)
		self.y_pos = 10
		self.speed = random.randint(1,3)
	def update(self):
		self.y_pos += self.speed
		screen.blit(ball_img, (self.x_pos, self.y_pos))

class player:
	def __init__(self, joystick, img):
		self.x_pos = random.randint(100, 500)
		self.y_pos = 590
		self.lives = 5
		self.joystick = joystick
		self.figure = img
	def got_hit(self):
		self.lives += -1
	def go_up_lvl(self):
		self.y_pos += 20
	def update(self):
		screen.blit(self.figure,(self.x_pos, self.y_pos))
	def move(self, amount):
		self.x_pos += amount
		if self.x_pos > 500: #make sure player hasn't moved to far
			self.x_pos = 500
		elif self.x_pos < 100:
			self.x_pos = 100

def reprint():
	screen.fill((255,255,255)) #wipe screen
	for ball in balls:
		balls[ball].update() #move balls down the screen and print the ball
		players['p1'].update() #print the player figure
		players['p2'].update()
	pygame.display.update() #update display

def begin():
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
			players['p1'] = player(0, p1_fig)
                	j2 = joysticks[1]
			j2.init()
                	players['p2'] = player(1, p2_fig)

def set_difficulty():
	difficulty = safe_input('int', 'Set difficulty between 1 and 60')
	if difficulty > 0 and difficulty < 61:
		return difficulty
	else:
		print "Difficulty is between 1 and 60"
		return set_difficulty()

difficulty = set_difficulty()
begin() #initialize everything

balls['b1'] = ball()
balls['b2'] = ball()
balls['b3'] = ball()

while True:
	clock.tick(10*difficulty) #timing the speed of game and balls
	reprint() #update the display
	for event in pygame.event.get():
		if event.type == QUIT: #has close pygame window
			exit() #leave game
		elif event.type == 7: #checking if joystick is being moved
			if event.dict['axis'] == 0: #make sure joystick is being move left or right
				for person in players:
					if players[person].joystick == event.dict['joy']: #move the right player, so both joysticks don't move both players
						players[person].move(event.dict['value']*25) #move player
	for ball in balls:
		if balls[ball].y_pos > 725: #is ball off board
			balls[ball].__init__() # reset ball
		for person in players:
			if players[person].y_pos < balls[ball].y_pos + 25 and players[person].y_pos > balls[ball].y_pos - 25: #has player been hit
				if players[person].x_pos < balls[ball].x_pos + 25 and players[person].x_pos > balls[ball].x_pos - 25: #has player been hit
					players[person].got_hit() #lose a life
					print "{} got hit!".format(person)
					balls[ball].__init__() #reset ball after hitting player
					if players[person].lives == 0: #has player died
						if players['p1'].lives == 0: #which player has 0 lives?
							print "Player 2 wins!"
						else:
							print "  Player 1 wins!"
						exit() #end game
