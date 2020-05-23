import pygame
from pygame.locals import *
import random

SPACE = 65
RIGHT = 114
LEFT = 113 #don't mess with these

alien_speed = 30 #how fast the alien moves. The smaller the number, the faster it moves.
num_aliens = 30 #number of aliens
alien_shot_chance = 200 #the smaller the number, the more likely the alien is to shoot.

pygame.init()
pygame.joystick.init()
pygame.key.set_repeat(1, 50)

screen_width = 500 #screen size
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

alien_img = pygame.image.load('small_spaceship.png')
bullet_img = pygame.image.load('small_bullet.png')
player_img = pygame.image.load('small_triangle.png')
bomb_img = pygame.image.load('small_bomb.jpg')

def display_text(text, x, y):
    textsurface = myfont.render(text, False, (255,255,255))
    screen.blit(textsurface, (x, y))

class alien:
    def __init__(self, x, y, speed, img):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.count = 0
        self.direction = 1
        self.bullet = 'empty'
        self.status = "alive"
    def die(self):
        self.status = "dead"
    def update(self):
        if self.status == "alive":
            self.count += 1
            if self.count == self.speed:
                self.count = 0
                self.x += self.direction*25
            if self.x > screen_width-25 or self.x < 25:
                self.direction = self.direction * -1
                self.y += 25
                self.x += self.direction*25
            if self.bullet != 'empty':
                self.bullet.update(1)
            screen.blit(self.img,(self.x,self.y))
    def shoot(self):
        if self.bullet == 'empty':
            self.bullet = bullet(self.x, self.y,4, bomb_img)
    def end_shot(self):
        del(self.bullet)
        self.bullet = 'empty'

class player:
    def __init__(self, x, y, lives, img):
        self.x = x
        self.y = y
        self.lives = lives
        self.img = img
        self.bullet = 'empty'
    def move(self,amount):
        self.x += amount*12.5
        if self.x > screen_width-25:
            self.x = screen_width-25
        elif self.x < 1:
            self.x = 25
    def shoot(self):
        if self.bullet == 'empty':
            self.bullet = bullet(self.x, self.y-25,2,bullet_img)
    def end_shot(self):
        self.bullet = 'empty'
    def update(self):
        screen.blit(self.img,(self.x, self.y))
        if self.bullet != 'empty':
            self.bullet.update(-1)

class bullet:
    def __init__(self, x, y, speed, img):
        self.speed = speed
        self.count = 0
        self.x = x
        self.y = y
        self.img = img
    def update(self, direction):
        self.count += 1
        if self.count == self.speed:
            self.count = 0
            self.y += direction*12.5
        screen.blit(self.img,(self.x,self.y))

def get_joystick():
    wait = 0
    waiting = True
    pygame.init()
    delay = 2
    while waiting:
        wait += 1
        if wait == delay:
            wait = 0
            delay = 10
            screen.fill((0,0,0))
            display_text("No joystick detected, press space to keep looking,",0,0)
            display_text("or the right arrow to use keypad instead", 0, 30)
            pygame.display.update()
            getting_answer = True
            while getting_answer:
                for event in pygame.event.get():
                    if event.type == 2:
                        if event.dict['scancode'] == SPACE:
                            getting_answer = False
                        elif event.dict['scancode'] == RIGHT:
                            return False
        pygame.joystick.quit()
        pygame.joystick.init()
        if pygame.joystick.get_count() >= 1:
            waiting = False
            j1 = pygame.joystick.Joystick(0)
            j1.init()
            return j1

def init():
    p1 = player(250 ,screen_height-25,1,player_img)
    aliens = []
    x_pos = 0
    y_pos = 0
    joystick = get_joystick()
    for i in range(0, num_aliens):
        x_pos += 50
        if x_pos > screen_width:
            x_pos = 50
            y_pos += 50
            aliens.append(alien(x_pos, y_pos, alien_speed, alien_img))
        print pygame.mouse.get_pos()
        pygame.display.update()
    return p1, aliens, joystick

running = True
player, aliens, j1 = init()
while running:
    num_live_ships = 0
    screen.fill((0,0,0))
    player.update()
    if player.bullet != 'empty':
        if player.bullet.y < 0:
            player.end_shot()
    for ship in aliens:
        if ship.status == 'alive':
            num_live_ships += 1
        ship.update()
        if ship.bullet != 'empty' and ship.status != 'dead':
            if ship.bullet.y > player.y - 25 and ship.bullet.y < player.y+25:
                if ship.bullet.x > player.x - 25 and ship.bullet.x < player.x + 25:
                    screen.fill((0,0,0))
                    display_text("YOU LOSE!",0,0)
                    pygame.display.update()
                    clock.tick(1)
                    exit()
            if ship.bullet.y > screen_height:
                ship.end_shot()
        if ship.x < player.x + 50 and ship.x > player.x - 50:
            if random.randint(0, alien_shot_chance) == 4:
                ship.shoot()
                if player.bullet != 'empty':
            if ship.status != 'dead':
                            if player.bullet.y > ship.y - 25 and player.bullet.y < ship.y + 25:
                                    if player.bullet.x < ship.x + 25 and player.bullet.x > ship.x - 25:
                        ship.end_shot()
                                        ship.die()
                                            player.end_shot()
    if num_live_ships == 0:
        screen.fill((0,0,0))
        display_text("YOU WIN!",0,0)
        running = False
        clock.tick(1)
    pygame.display.update()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == 7:
            if event.dict['axis'] == 0:
                player.move(int(event.dict['value']))
        elif event.type == 10:
            if event.dict['button'] == 0:
                player.shoot()
        elif event.type == 2:
            if event.dict['scancode'] == SPACE:
                player.shoot()
            elif event.dict['scancode'] == RIGHT:
                player.move(1)
            elif event.dict['scancode'] == LEFT:
                player.move(-1)
