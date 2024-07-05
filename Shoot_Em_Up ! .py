from kandsky import *
from time import *
from random import *
from kandinsky import *
from ion import *

WIDTH, HEIGHT = 320, 222


# creation de notre joueur
class Player():
    def __init__(self):
        self.x = 5
        self.y = int(HEIGHT / 2)
        self.up = KEY_UP
        self.down = KEY_DOWN
        self.shoot = KEY_OK
        self.speed = 2
        self.life = 3

    def move(self):
        if keydown(self.up):
            self.y -= self.speed
        if keydown(self.down):
            self.y += self.speed

    def fire(self):
        fill_rect(self.x + 15, self.y - 5, 320, 1, color(255, 0, 0))
        fill_rect(self.x + 15, self.y + 15, 320, 1, color(255, 0, 0))

    def draw(self):
        fill_rect(self.x, self.y, 15, 10, 'gray')
        fill_rect(self.x + 5, self.y - 5, 1, 5, 'gray')
        fill_rect(self.x + 5, self.y + 10, 1, 5, 'gray')
        fill_rect(self.x + 5, self.y - 5, 10, 1, 'gray')
        fill_rect(self.x + 5, self.y + 15, 10, 1, 'gray')


class Enemie:
    def __init__(self):
        self.x = 320
        self.y = randint(0, 210)
        self.speed = 3
        self.width = 20
        self.height = 10

    def draw(self):
        draw_line(self.x + self.width, self.y, self.x, self.y + round(self.height / 2), 'white')
        draw_line(self.x, self.y + int(self.height / 2), self.x + self.width, self.y + self.width / 2, 'white')
        fill_rect(self.x + self.width, self.y, 1, self.height, 'white')


class Star:
    def __init__(self):
        self.x = randint(0, 320)
        self.y = randint(0, 222)
        self.luminosity = randint(150, 255)
        self.size = randint(1, 5)

    def draw(self):
        fill_rect(self.x, self.y, self.size, self.size, color(self.luminosity, self.luminosity, self.luminosity))


stars = []
# init stars
number_of_stars = 24
enemies = []
number_of_enemies = 1
for i in range(number_of_enemies):
    enemies.append(Enemie())
for i in range(number_of_stars):
    stars.append(Star())
score = 0
player = Player()
while True:
    player.move()
    player.draw()
    player.fire()
    sleep(0.04)
    fill_rect(0, 0, WIDTH, HEIGHT, 'black')
    for i in range(number_of_stars):
        stars[i].x -= 10
        if stars[i].x <= 0:
            stars[i] = Star()
            stars[i].x = 320
        stars[i].draw()
    for i in range(number_of_enemies):
        enemies[i].x -= enemies[i].speed
        if enemies[i].y < player.y:
            enemies[i].y -= 1
        else:
            enemies[i].y += 1
        if enemies[i].x <= 0:
            enemies[i].x = 320
            player.life -= 1
            enemies[i].y = randint(0, 200)
        if enemies[i].y <= player.y + 15 and enemies[i].y >= player.y - 5:
            enemies[i] = Enemie()
            score += 10
        if enemies[i].y == 222:
            enemies[i] = Enemie()
        if enemies[i].y == 0:
            enemies[i] = Enemie()
        enemies[i].draw()
    draw_string("score : " + str(score), 0, 0)