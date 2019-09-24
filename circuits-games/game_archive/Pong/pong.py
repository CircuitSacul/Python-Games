import pygame
from math import cos, sin, sqrt, pi

pygame.quit()
pygame.joystick.quit()
pygame.init()
pygame.joystick.init()
pygame.key.set_repeat(1, 50)
pygame.mouse.set_visible(False)

screen_width = 600
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
pygame.display.set_caption("Pong")

joysticks = []

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

players = 1
player_height = 60
player_width = 2
ball_r = 10
ball_countdown = 0
player_countdown = 0
player_speed = 5
game_speed = 120


def display_text(text, x, y):
        textsurface = myfont.render(text, False, (255,255,255))
        screen.blit(textsurface, (x, y))

def get_joystick():
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


class Ball:
	def __init__(self, x, y, radius, speed, angle_num):
		self.x = x
		self.y = y
		self.r = radius
		self.speed = speed
		self.countdown = speed
		self.angle = (angle_num*pi)/180
		self.angle_y = sin(self.angle)
		self.angle_x = cos(self.angle)
	def update(self):
		self.countdown -= 1
		if self.y >= screen_height or self.y <= 0:
			self.angle_y = self.angle_y*-1.01
		if self.countdown <= 0:
			self.x += (self.angle_x)
			self.y += (self.angle_y)
			self.countdown = self.speed
		pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), int(ball.r), 0)


class Player:
	def __init__(self, x, y, height, width, countdown):
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.speed = countdown
		self.countdown = self.speed
		self.to_move = 0
	def update(self):
		self.countdown -= 1
		if self.countdown <= 0:
			self.y += self.to_move
			self.to_move = 0
			self.countdown = self.speed
		pygame.draw.rect(screen, RED, (self.x, self.y, player_width, player_height))


users = []
p1 = Player(20, screen_width/2, player_height, player_width, player_countdown)
users.append(p1)
if players == 1:
	ai = Player(screen_width-20, screen_height/2, player_height, player_width, player_countdown)
	users.append(ai)
else:
	p2 = Player(screen_width-20, screen_height/2, player_height, player_width, player_countdown)
	users.append(p2)
ball = Ball(screen_height/2, screen_width/2+ 10, ball_r, ball_countdown, 180)

while True:
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		#Other commands
	x, y = pygame.mouse.get_pos()
	p1.y = y
	p1.y -= player_height/2
	if ball.x > screen_width:
		ball.__init__(screen_height/2, screen_width/2+ 10, ball_r, ball_countdown, 180)
		clock.tick(1)
	elif ball.x < 0:
		ball.__init__(screen_height/2, screen_width/2+ 10, ball_r, ball_countdown, 180)
		clock.tick(1)
	if players == 1:
		if ball.y > ai.y+(player_height/2):
			ai.to_move = player_speed
		elif ball.y < (ai.y+player_height/2):
			ai.to_move = -1*player_speed
	for user in users:
		if int(ball.y) in range(user.y,user.y + player_height):
			if int(ball.x) < user.x + 10 and int(ball.x) > user.x - 10:
				ball.angle_x = ball.angle_x*-1.1
				h = user.y + (player_height/2)
				ball.angle_y += (ball.y - h)/15
	p1.update()
	if players == 2:
		p2.update()
	else:
		ai.update()
	ball.update()
	pygame.display.update()
	clock.tick(game_speed)
