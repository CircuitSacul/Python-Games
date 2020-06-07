import gameboard as gb
import getkey as gk
import random
import time

player = {'marker' : 'D', 'x_position' : 10, 'y_position' : 25}

ball1 = {'marker': '0', 'x_position': 1, 'y_position': 30, 'speed': 5}  # need more balls
ball2 = {'marker': '0', 'x_position': 2, 'y_position': 30, 'speed': 5}  # need more balls
ball3 = {'marker': '0', 'x_position': 3, 'y_position': 30, 'speed': 5}  # need more balls
ball4 = {'marker': '0', 'x_position': 4, 'y_position': 30, 'speed': 5}  # need more balls
ball5 = {'marker': '0', 'x_position': 5, 'y_position': 30, 'speed': 5}
ball6 = {'marker': '0', 'x_position': 6, 'y_position': 30, 'speed': 5}
ball7 = {'marker': '0', 'x_position': 7, 'y_position': 30, 'speed': 5}
ball8 = {'marker': '0', 'x_position': 8, 'y_position': 30, 'speed': 5}

treasure = {'marker': '#', 'x_position': 2, 'y_position': 10}
treasureline = [treasure, treasure, treasure, treasure, treasure, treasure, treasure, treasure, treasure]

levellength = 100

def player_on_valid_space():
    if player['x_position'] <= min_x or player['y_position'] <= min_y or player['x_position'] >= max_x-1 or player['y_position'] >= max_y:
        return False
    else:
        for wall in allwalls:
            if player['x_position'] == wall['x_position'] and player['y_position'] == wall['y_position']:
                return False
            else:
                return True


def move_figure(figure, y_change, x_change):
    figure['x_position'] += x_change
    figure['y_position'] += y_change

allballs = [ball1, ball2, ball3, ball4, ball5, ball6, ball7, ball8]
allwalls = []
allmovingfigures = [ball1, ball2, ball3,ball4, ball5, ball6, ball7,ball8, player]

max_x = 13
max_y = 35
min_x = 1
min_y = 1


def figure_loop():
    for ball in allballs:
        if ball['y_position'] == max_y:
            ball['y_position'] = 2
            ball['speed'] = random.randint(1, 3)
            ball['x_position'] = player['x_position'] + random.randint(-1, 1)
    for figure in allmovingfigures:
        if figure['x_position'] >= max_x-1:
            figure['x_position'] = max_x-2
        if figure['x_position'] <= min_x:
            figure['x_position'] = min_x+1
        if figure['y_position'] == max_y:
            figure['y_position'] = max_y-1
        if figure['y_position'] == min_y:
            figure['y_position'] = min_y+1


def player_dead():
    for ball in allballs:
        if player['x_position'] == ball['x_position'] and player['y_position'] == ball['y_position']:
            return True
    return False


def update_board():
    allfigures = []
    for ball in allballs:
        allfigures.append(ball)
    for wall in allwalls:
        allfigures.append(wall)
    o = 0
    for treasures in treasureline:
        o += 1
        treasures['x_position'] += o
        allfigures.append(treasure)
    allfigures.append(player)
    gb.create_board(allfigures, max_y, max_x)


def nextlevel(new_level):
    player['y_position'] = 25-new_level
    if new_level == 11:
        for ball in allballs:
            ball['y_position'] = 25
            ball['speed'] = 8



def run():
    currentlevel = 0
    t = 0
    nextlvl = 0
    while 1:
        print "\033[2J\033[0;0H"
        update_board()
        t += 1
        nextlvl += 1
        key = gk.read_key()
        time.sleep(0.05)
        for ball in allballs:
            if int(t/ball['speed'])*ball['speed']==t:
                move_figure(ball, 1, 0)
        figure_loop()
        if key == 'l':
            move_figure(player, 0, 1)
        if key == 'j':
            move_figure(player, 0, -1)
        if player_dead():
            print "O"
            print "X"
            print "GAME OVER. You made it {} levels.".format(currentlevel)
            return False
        if nextlvl == levellength:
            if currentlevel == 11:
                print "YOU WON!"
                return True
            currentlevel = currentlevel + 1
            nextlevel(currentlevel)
            nextlvl = 0
