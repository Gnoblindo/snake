import math;
import random;
import pygame;
import tkinter as tk;
from tkinter import messagebox;


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
    draw_grid(size, rows, surface)
    pygame.display.update()

def main():
    global size, rows
    size = 500
    rows = 20
    window = pygame.display.set_mode((size, size))

    flag = True
    clock = pygame.time.Clock()

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        pygame.time.delay(50)
        clock.tick(10)

        draw_window(window)

main()