import pygame
from pygame.locals import *
from math import cos,sin,pi,sqrt
import random

pygame.init()
pygame.key.set_repeat(1, 1)

screen_height = 1000
screen_width = 1000

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
myfont = pygame.font.SysFont('Comic Sans MS', 30)

myimg = pygame.image.load('small_triangle.png').convert()

num_aliens = 7

aliens = []

def display_text(text, x, y):
        textsurface = myfont.render(text, False, (255,255,255))
        screen.blit(textsurface, (x, y))


class starbase:
	def __init__(self, x, y, img, pointer_img):
		self.x = x
		self.y = y
		self.img = img
		self.pointer = pointer_img
		self.bullets = []
		self.angle = (0*pi)/180
	def shoot(self, img):
		self.bullets.append(bullet(self.x, self.y, self.angle, img))
	def update(self, angle):
		i = 0
		for shot in self.bullets:
			print shot
			if shot.x >= screen_width or shot.y >= screen_height or shot.x <= 0 or shot.y <= 0:
				shot.off_board()
				del self.bullets[i]
			i += 1
		for shot in self.bullets:
			if shot.gone == False:
				shot.update()
		self.angle = (angle*pi)/180
		screen.blit(self.img,(self.x,self.y))
		screen.blit(self.pointer,(self.x + (cos(self.angle)*100), (self.y + (sin(self.angle)*100))))


class bullet:
	def __init__(self, x, y, angle, img):
		self.x = x
		self.y = y
		self.img = img
		self.angle = angle
		self.speed = 1
		self.gone = False
	def update(self):
		self.speed -= 1
		if self.speed == 0:
			self.speed = 1
			self.x += cos(self.angle)*25
			self.y += sin(self.angle)*25
		screen.blit(self.img,(self.x,self.y))
	def off_board(self):
		self.gone = True


class alien:
	def __init__(self, x, y, img):
		self.img = img
		self.x = x
		self.y = y
		self.speed = 20
		self.speed_count = 0
		self.fire_rate = 50
		self.fire_count = 0
		self.angle = 0
		self.bullets = []
		self.change_angle = True
		self.bool_shoot = False
	def move_angle(self, bool_change_angle):
		self.change_angle = bool_change_angle
	def update(self):
		self.speed_count += 1
		self.fire_count += 1
		if self.speed_count == self.speed:
			self.speed_count = 0
			if self.change_angle:
				rand_angle = random.randint(0, 360)
				self.angle = rand_angle
			else:
				self.angle = random.randint(self.angle-25,self.angle+25)
			self.x += cos((self.angle*pi)/180)*25
			self.y += sin((self.angle*pi)/180)*25
			if self.x >= screen_width:
				self.x = screen_width - 25
				self.change_angle = True
			elif self.x <= 0:
				self.x = 25
				self.change_angle = True
			if self.y >= screen_height:
				self.y = screen_height - 25
				self.change_angle = True
			elif self.y <= 0:
				self.y = 25
				self.change_angle = True
                for shot in self.bullets:
                        if shot.x >= screen_width or shot.x <= 0 or shot.y >= screen_height or shot.y <= 0:
                                del(self.bullets[0])
		for shot in self.bullets:
			shot.update()
		if self.fire_count >= self.fire_rate:
			self.fire_count = 0
			self.bool_shoot = True
		screen.blit(self.img, (self.x, self.y))
	def shoot(self, angle):
		self.bullets.append(bullet(self.x, self.y, angle, self.img))

def abs(value):
	if value < 0:
		value = value*-1
	return value

def is_closer(before_x, before_y, after_x,after_y, reference_x, reference_y):
	before_x -= reference_x
	before_y -= reference_y
	after_x -= reference_x
	after_y -= reference_y

	before_x = abs(before_x)
	before_y = abs(before_y)
	after_x = abs(after_x)
	after_y = abs(after_y)

	before = before_x**2 + before_y**2
	after = after_x**2 + after_y**2

	if sqrt(after) < 200:
		return True
	if sqrt(after) < 100:
		return False
	if after < before:
		return True
	else:
		return False


for i in range(0, num_aliens):
	aliens.append(alien(random.choice([50,950,]) , random.choice([50,950]) , myimg))

angle = 0
base = starbase(487.5,487.5,myimg,myimg)
shot_delay = 25

while True:
	screen.fill((0,0,0))
	ax = -1
	count = 0
	for ship in aliens:
		count += 1
		ax += 1
		if ship.speed_count == ship.speed -1:
			before_x = ship.x
			before_y = ship.y
			ship.update()
			after_x = ship.x
			after_y = ship.y
			if is_closer(before_x, before_y, after_x,after_y, base.x, base.y) == False:
				ship.move_angle(True)
			else:
				ship.move_angle(False)
		else:
			ship.update()
		if ship.bool_shoot == True and sqrt((base.x - ship.x)**2 + (base.y - ship.y)**2) < 400:
			ship.shoot(ship.angle)
			ship.bool_shoot = False
		for shot in base.bullets:
			if abs(ship.x - shot.x) < 25 and abs(ship.y - shot.y) < 25:
				del(aliens[ax])
		for shot in ship.bullets:
			if abs(base.x - shot.x) < 50 and abs(base.y - shot.y) < 50:
				print "YOU LOSE!!!"
				exit()
	if count == 0:
		print "YOU WIN!!!"
		pygame.quit()
		exit()
	shot_delay += -1
	for event in pygame.event.get():
		if event.type == 2:
			if event.dict['scancode'] == 114:
				angle += 5
			elif event.dict['scancode'] == 65:
		 		if shot_delay <= 0:
					base.shoot(myimg)
					shot_delay = 25
			elif event.dict['scancode'] == 113:
				angle -= 5
	base.update(angle)
	pygame.display.update()
	clock.tick(40)
