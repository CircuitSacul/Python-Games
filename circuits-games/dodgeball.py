# Libraries
import sys, pygame, random
from time import sleep
# Setup 1
pygame.quit()
pygame.init()

BLACK = (  0,   0,   0)
GREY = (100, 100, 100)
DARK_GREY = (40, 40, 40)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 100)
LIGHT_BLUE = (0, 0, 255)

balls = []

player_color = WHITE
ball_color = WHITE
ball_r = 12 # Ball radius
screen_size = (500, 600)
screen_x, screen_y = screen_size
version = '1.2.0'
fps = 128

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
smallfont = pygame.font.SysFont('Comic Sans MS', 30)
mediumfont = pygame.font.SysFont('Comic Sans MS', 50)
bigfont = pygame.font.SysFont('Comic Sans MS', 100)
pygame.display.set_caption("Dodge Ball")

#Functions
def pause_menu():
	#screen.fill(WHITE)
	#display_text("PAUSE MENU", ('center', 10), True, GREY, bigfont)
	pygame.draw.rect(screen, WHITE, ((50, 100), (400, 200)))
	resume_button.blit()
	exit_button.blit()
	pygame.display.update()
	while True:
		x, y = wait_for_click()
		if resume_button.check_press(x, y) == True:
			return 1
		elif exit_button.check_press(x, y) == True:
			return 0


def menu():
	screen.fill(WHITE)
	display_text("Dodge Ball", ('center', 10), True, GREY, bigfont)
	display_text("Welcome to my GUI(Graphical User Interface)", ('center', 90), True, BLACK, smallfont)
	display_text("Dodge Ball. Use your mouse to move your figure", ('center', 110), True, BLACK, smallfont)
	display_text("(The white square). Dodge balls to gain points.", ('center', 130), True, BLACK, smallfont)
	display_text("As you play, you will level up and more balls", ('center', 150), True, BLACK, smallfont)
	display_text("will be added. Enjoy!", ('center', 170), True, BLACK, smallfont)
	display_text("v-{}".format(version), (5, screen_y-20), True, BLACK, smallfont)
	play_button.blit()
	quit_button.blit()
	pygame.display.update()
	while True:
		x, y = wait_for_click()
		if play_button.check_press(x, y) == True:
			return 1
		elif quit_button.check_press(x, y) == True:
			sys.exit()


def clear():
	print("\033[2J")
	print("\033[0;0H")


def rectpos(textrect):
	tlx, tly = textrect.topleft
	cx, cy = textrect.center
	return tlx, tly, cx, cy


def display_text(text, pos, tidy, color, font):
	x, y = pos
	textsurface = font.render(text, tidy, color)
	textrect = textsurface.get_rect()
	tlx, tly, cx, cy = rectpos(textrect)
	if x != 'center':
		textrect.topleft = (x, tly)
		tlx, tly, cx, cy, = rectpos(textrect)
	else:
		textrect.center = (screen_x/2, cy)
		tlx, tly, cx, cy = rectpos(textrect)
	if y != 'center':
		textrect.topleft = (tlx, y)
		tlx, tly, cx, cy = rectpos(textrect)
	else:
		textrect.center = (cx, screen_y/2)
		tlx, tly, cx, cy = rectpos(textrect)
	screen.blit(textsurface, textrect)


def colored(color, text):
	r, g, b = color
	return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


def safe_input(input_type, text):
	if input_type.lower() == 'float':
		try:
			return float(input(text))
		except ValueError:
			print(colored(RED, "Value Error. Please enter a float or integer."))
			return safe_input(input_type, text)
	elif input_type.lower() == 'int':
		try:
			return int(input(text))
		except ValueError:
			print(colored(RED, "Value Error. Please enter an integer."))
			return safe_input(input_type, text)
	else:
		return input(text)


def wait_for_click():
	clock.tick(1)
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == 5:
				waiting = False
				return pygame.mouse.get_pos()


#Classes
class Button:
	def __init__(self, cx, cy, text, font, color, high_quality, bkcolor, bkcolor2):
		self.textsurface = font.render(text, high_quality, color)
		self.textrect = self.textsurface.get_rect()
		self.textrect.center = (cx, cy)
		self.tlx, self.tly = self.textrect.topleft
		self.brx, self.bry = self.textrect.bottomright
		self.bkcolor = bkcolor
		self.bkcolor2 = bkcolor2
	def blit(self):
		pygame.draw.rect(screen, self.bkcolor, self.textrect)

		pygame.draw.polygon(screen, self.bkcolor2, (self.textrect.topright, self.textrect.bottomright, (self.textrect.bottomright[0]+5, self.textrect.bottomright[1]+5), (self.textrect.topright[0]+5, self.textrect.topright[1]+5)))
		pygame.draw.polygon(screen, self.bkcolor2, (self.textrect.bottomleft, self.textrect.bottomright, (self.textrect.bottomright[0]+5, self.textrect.bottomright[1]+5), (self.textrect.bottomleft[0]+5, self.textrect.bottomleft[1]+5)))

		screen.blit(self.textsurface, self.textrect)
	def check_press(self, x, y):
		if x >= self.tlx and x <= self.brx:
			if y >= self.tly and y <= self.bry:
				return True
		return False


class Player:
	def __init__(self):
		self.x = screen_x/2
		self.y = screen_y-100
		self.color = player_color
	def update(self):
		pygame.draw.rect(screen, self.color, (self.x, self.y, 25, 25))


class Ball:
	def __init__(self):
		self.color = ball_color
		self.move_x = random.randint(-3, 3)/3
		self.move_y = random.randint(3, 15)/3
		if int(self.move_y) == 0:
			self.move_y += 1
		self.x = player.x
		self.y = -1*ball_r
	def update(self):
		self.x += self.move_x
		self.y += self.move_y
		if self.x <= ball_r or self.x >= screen_x-ball_r:
			self.move_x = self.move_x*-1
		pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(ball_r), 0)

#Setup 2
clear()

player = Player()

play_button = Button(screen_x/2, screen_y/2, "    PLAY    ", bigfont, BLACK, True, GREY, BLACK)
quit_button = Button(screen_x/2, screen_y/2+90, "    QUIT    ", bigfont, BLACK, True, GREY, BLACK)
pause_button = Button(screen_x/2, 50, "PAUSE", mediumfont, GREY, False, BLACK, BLACK)
exit_button = Button(screen_x/2, 240, "    EXIT    ", bigfont, BLACK, True, GREY, BLACK)
resume_button = Button(screen_x/2, 150, " RESUME ", bigfont, BLACK, True, GREY, BLACK)


#Main
def main():
	balls = []
	balls.append(Ball())
	dodged_balls = 0
	lives = 3
	hits = 0
	countdown = 4000
	nxtlvlcountdown = countdown
	lvl = 0
	while True:
		nxtlvlcountdown -= 1
		if nxtlvlcountdown <= 0:
			nxtlvlcountdown = countdown
			lvl += 1
			display_text("LEVEL UP!", ('center', 'center'), True, WHITE, bigfont)
			pygame.display.update()
			balls.append(Ball())
			sleep(2)
		screen.fill(BLACK)
		display_text("HITS: {} LIVES: {} SCORE: {} LEVEL {}".format(hits, lives, dodged_balls, lvl), ('center', 10), False, GREY, smallfont)
		player.update()
		pause_button.blit()
		for ball in balls:
			if ball.y > screen_y+ball_r:
				ball.__init__()
				dodged_balls += 1
			ball.update()
			if ball.x - ball_r < player.x + 25 and ball.x + ball_r > player.x:
				if ball.y - ball_r < player.y + 25 and ball.y + ball_r > player.y:
					lives -= 1
					hits += 1
					ball.__init__()
		if lives <= 0:
			display_text("GAME OVER", ('center', 250), True, RED, bigfont)
			display_text("You dodged {} balls and made it to level {}".format(dodged_balls, lvl), ('center', 320), True, WHITE, smallfont)
			display_text("Click to Continue", ('center',340), True, GREY, smallfont)
			pygame.display.update()
			wait_for_click()
			return True

		for event in pygame.event.get(pygame.MOUSEMOTION):
			player.x, ignore = pygame.mouse.get_pos()
			break
		for event in pygame.event.get(pygame.QUIT):
			pygame.QUIT
			return True
		for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
			x, y = pygame.mouse.get_pos()
			if pause_button.check_press(x, y) == True:
				choice = pause_menu()
				if choice == 1:
					pass
				elif choice == 0:
					return True
		clock.tick(fps)
		pygame.display.update()


try:
    while True:
	    if menu() == 1:
		    main()
	    elif menu() == 0:
		    break
except Exception:
	print("Error Msg:", e)
finally:
	clear()
	print(colored(LIGHT_BLUE, "Thanks for playing!"))
	pygame.quit()
	sys.exit()
