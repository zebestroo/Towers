import pygame
import copy
import sys
import os.path
from pygame.locals import *

pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((1200, 990))

pygame.display.set_caption("Towers")

pygame.mixer.music.load(os.path.abspath("music/wait.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
music_battle = pygame.mixer.Sound(os.path.abspath("music/battle.mp3"))
music_tower_install = pygame.mixer.Sound(os.path.abspath("music/tower_install.mp3"))

music_battle.set_volume(0.5)
#os.path.abspath("main.png")
scr = pygame.image.load(os.path.abspath("main.png"))
nodes_first = [(0, 90), (765, 90), (765, 315), (135, 315), (135, 810), (630, 810), (630, 675), (270, 675), (270, 450), (855, 450), (855, 945)]
nodes_second = [(0, 135), (720,135), (720, 270), (90, 270), (90, 855), (675, 855), (675, 630), (315, 630), (315, 495), (810, 495), (810, 945)]
list_of_available = []


run = True

class standart_enemy:
    price = 200
    def __init__(self, image, health, speed, x, y, stage, tp, index):
        self.image = image
        self.health = health
        self.speed = speed
        self.x = x
        self.y = y
        self.stage = stage
        self.tp = tp
        self.index = index

class tower:
    def __init__(self, image, damage, radius, x, y, name="Black"):
        self.image = image
        self.damage = damage
        self.radius = radius
        self.x = x
        self.y = y
        self.name = name
        self.cost = 200

    def check_radius(self, enemy):
        if ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**(1/2) <= self.radius:
            return True
        else:
            return False
        

    def attack(self, enemy):
        enem.health -= 0.05

    def radius_up(self):
        self.radius += 10

    def damage_up(self):
        self.damage += 5

class line:
    def __init__(self, color, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color
        
        
unavailable_set = set() 
width = 45
height = 45
TOWER = False
tw = None
enemies = []
Towers = []
lines = []
main_counter = 0
cash = 400
hp = 1


def create_list(nodes):
    unavailable_set.add(nodes[0])
    for index, tup in enumerate(nodes):
        if index < len(nodes) - 1:
            k_x = 1
            k_y = 1
            if nodes[index+1][0] - tup[0] < 0:
                k_x = -1
            if nodes[index+1][1] - tup[1] < 0:
                k_y = -1
            delta_x = abs(nodes[index+1][0] - tup[0])
            delta_y = abs(nodes[index+1][1] - tup[1])
            rng_x = list(range(0, delta_x, 45))
            rng_y = list(range(0, delta_y, 45))
            for x in rng_x:
                unavailable_set.add((nodes[index+1][0] - k_x * x, tup[1]))
            for y in rng_y:
                unavailable_set.add((tup[0], nodes[index+1][1] - k_y * y))
        index += 1 


create_list(nodes_first)
create_list(nodes_second)

def create_enemies(health):
    i = 0
    x = 0
    while i < 16:
        y = 90
        if i % 2 == 0:
            enemies.append(standart_enemy(pygame.image.load(os.path.abspath("enemy.png")), 16 * health, 0.5, x, y, 1, 1, i))
        else:
            enemies.append(standart_enemy(pygame.image.load(os.path.abspath("enemy.png")), 16 * health, 0.5, x, y + 45, 1, 2, i))
        x -= 45
        i += 1



def move(enemy, total_speed, counter):
    
    if enemy.tp == 1:
        if enemy.x == nodes_first[enemy.stage][0] and enemy.y == nodes_first[enemy.stage][1]:
            enemy.stage += 1
    else:
        if enemy.x == nodes_second[enemy.stage][0] and enemy.y == nodes_second[enemy.stage][1]:
            enemy.stage += 1

    if enemy.health == 0:
        enemies.remove(enemy)
    if enemy.stage == 11:
        counter += 1
        if enemy.index % 2 == 0:
            enemy.x = 0
            enemy.y = 90
            enemy.stage = 1
        else:
            enemy.x = 0
            enemy.y = 135
            enemy.stage = 1

    if enemy.stage == 1 or enemy.stage == 5 or enemy.stage == 9:
        enemy.x += enemy.speed
    if enemy.stage == 2 or enemy.stage == 4 or enemy.stage == 10:
        enemy.y += enemy.speed
    if enemy.stage == 3 or enemy.stage == 7:
        enemy.x -= enemy.speed
    if enemy.stage == 6 or enemy.stage == 8:
        enemy.y -= enemy.speed
    return counter

def DrawTowers():
    for twr in Towers:
        screen.blit(twr.image, (twr.x, twr.y))

def DrawLines():
    for line in lines:
        pygame.draw.line(screen, line.color, (line.start_x, line.start_y), (line.end_x, line.end_y))

def DrawEnemies():
    global cash
    for enem in enemies:
        if enem.health/hp < 1:
            enemies.remove(enem)
            cash += 5
            continue

        a = int(enem.health)
        enem.image = pygame.image.load(os.path.abspath("enemy.png"))
        health = pygame.image.load(os.path.abspath(f"images/health/hp_{int(a/hp)}.png"))
        enem.image.blit(health, (0, 0))
        screen.blit(enem.image, (enem.x, enem.y))

def DrawWindow():
    screen.blit(scr, (0, 0))
    DrawTowers()
    DrawEnemies()
    DrawLines()
    pygame.display.update()


while run:
    #pygame.time.delay(100)
    speed = 45
    if TOWER:
        pygame.time.delay(50)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    screen.blit(scr, (0, 0))

    if keys[pygame.K_SPACE]:
        create_enemies(hp)
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(music_battle)
        while len(enemies) != 0 and main_counter != 10:
            for enem in enemies:
                for twr in Towers:
                    if twr.check_radius(enem):
                        twr.attack(enem)
                        lines.append(line((0, 0, 0), twr.x + 22, twr.y + 22, enem.x + 22, enem.y + 22))
                main_counter = move(enem, 1, main_counter)
            DrawWindow()
            lines = []

        enemies = []
        hp += 1
        pygame.mixer.Sound.stop(music_battle)
        pygame.mixer.music.play(-1)
        cash *= 1.1
        print(cash)

    main_counter = 0


    if cash >= standart_enemy.price and (keys[pygame.K_t] or TOWER):
        if tw == None:
            print(type(tw))
            tw = tower(pygame.image.load(os.path.abspath("tower_black_1.png")), 1, 150, 0, 0)
        TOWER = True

        if keys[pygame.K_LEFT] and tw.x >= speed:
            tw.x -= speed

        if keys[pygame.K_RIGHT] and tw.x <= 900 - width - speed:
            tw.x += speed

        if keys[pygame.K_UP] and tw.y >= speed:
            tw.y -= speed

        if keys[pygame.K_DOWN] and tw.y <= 990 - height - speed:
            tw.y += speed

        screen.blit(tw.image, (tw.x, tw.y))

        pygame.draw.circle(screen, (0, 0, 0), (tw.x + 22, tw.y + 22),  tw.radius, 1)

        if keys[pygame.K_q]:
            unavailable_set.remove((tw.x, tw.y))
            TOWER = False
            tw = None


        if keys[pygame.K_p] and not((tw.x, tw.y) in unavailable_set):
            cash -= standart_enemy.price
            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(music_tower_install)
            Towers.append(tw)
            unavailable_set.add((tw.x, tw.y))
            tw = None
            TOWER = False
            print(cash)

        pygame.mixer.music.unpause()

        DrawTowers()
        pygame.display.update()

    if not TOWER:
        DrawWindow()

pygame.quit()
