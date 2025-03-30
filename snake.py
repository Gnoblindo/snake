import random
from tkinter import messagebox
import pygame;
import tkinter as tk;

fac_img = pygame.image.load('fughed.png')
fac_img = pygame.transform.scale(fac_img, (48, 48))
blank_img = pygame.image.load('koc.png')
blank_img = pygame.transform.scale(blank_img, (48, 48))

class Cube(object):
    rows = 20
    def __init__(self, start, dirnx=1, dirny=0, color=(132, 122, 159), blank=False):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
        self.blank = blank
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    def draw(self, surface, eyes=False):
        dis = size // rows
        rw = self.pos[0]
        cm = self.pos[1]
        if self.blank:
            surface.blit(blank_img, (rw * dis, cm * dis))
        elif eyes:
            surface.blit(fac_img, (rw * dis, cm * dis))
        else:
            pygame.draw.rect(surface, self.color, (rw*dis+1, cm*dis+1, dis-2, dis-2))

class Snake(object):
    end_game = False
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    self.game_over("ze zmęczenia")
                    return False
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    self.game_over("ze zmęczenia")
                    return False
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    self.game_over("ze zmęczenia")
                    return False
                elif c.dirny == -1 and c.pos[1] <= 0:
                    self.game_over("ze zmęczenia")
                    return False
                else:
                    c.move(c.dirnx, c.dirny)

        if self.head.pos in [c.pos for c in self.body[1:]]:
            self.game_over("przez podziwianie się")
            return False

        return True
        
    def game_over(self, przyczyna):
        root = tk.Tk()
        root.withdraw()
        odpowiedz = messagebox.askyesno(
            "Fulgrim poszedł spać", 
            "Fulgrim poszedł spać " + przyczyna + "\nZdobyte kocyki: " + str(len(self.body)-1) + "\nCzy chcesz zagrać jeszcze raz?"
            )
        
        if odpowiedz == True:
            root.destroy()
            reset_game()
        else:
            self.end_game = True

    def reset(self, pos):
        self.body = []
        self.turns = {}
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, rows, surface):
    size_between = w // rows

    x = 0
    y = 0
    for i in range(rows):
        x = x + size_between
        y = y + size_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def draw_window(surface):
    surface.fill((120, 30, 120))
    s.draw(surface)
    blanket.draw(surface)
    draw_grid(size, rows, surface)
    pygame.display.update()

def random_blanket(snake):
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def reset_game():
    global s, blanket
    s = Snake((0, 0, 0), (10, 10))
    blanket = Cube(random_blanket(s), blank=True)
    s.reset((10, 10))

def show_splash_screen(window):
    splash_image = pygame.image.load('spla.png')
    splash_image = pygame.transform.scale(splash_image, (1000, 1000))
    window.blit(splash_image, (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global size, rows, s, blanket
    size = 1000
    rows = 20
    window = pygame.display.set_mode((size, size))

    pygame.display.set_caption('Fugim the snake')
    show_splash_screen(window)

    s = Snake((0, 0, 0), (10, 10))
    blanket = Cube(random_blanket(s), blank=True)

    flag = True
    clock = pygame.time.Clock()

    while flag:

        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == blanket.pos:
            s.addCube()
            blanket = Cube(random_blanket(s), blank=True)
        if s.end_game == True:
            pygame.quit()
            return
        else:
            draw_window(window)

main()
