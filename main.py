import pygame, sys
from pygame.locals import *
import socket
import time
from threading import Thread
import json



hote = "localhost"
port = 3333

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print("Connection on {}".format(port))

# set up pygame
pygame.init()

SCREEN_SIZE_X = 500
SCREEN_SIZE_Y = 500

CELL_SIZE_X = SCREEN_SIZE_X / 100
CELL_SIZE_Y = SCREEN_SIZE_Y / 100

# set up the window
windowSurface = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y), 0, 32)
pygame.display.set_caption('Hello world!')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

windowSurface.fill(BLACK)

pygame.draw.rect(windowSurface, GREEN, (0, 0, CELL_SIZE_X, CELL_SIZE_Y))

# get a pixel array of the surface
pixArray = pygame.PixelArray(windowSurface)
del pixArray

# draw the window onto the screen
pygame.display.update()

x = 0


def pull_map():
    while True:
        socket.send(b"GET MAP")

        buffer = socket.recv(4096)
        data = buffer
        while len(buffer) == 4096:
            buffer = socket.recv(4096)
            data += buffer

        data_json = json.loads(data.decode("utf-8"))
        windowSurface.fill(BLACK)
        for x in range(len(data_json)):
            for y in range(len(data_json[x])):
                cell = data_json[x][y]
                if cell["Alive"]:
                    print(cell)
                    pygame.draw.rect(windowSurface, GREEN, (x * CELL_SIZE_X, y * CELL_SIZE_Y, CELL_SIZE_X, CELL_SIZE_Y))
                    pygame.display.update()
        time.sleep(.5)



t = Thread(target=pull_map, args=())
t.start()

# run the game loop
while True:
    # socket.send(b"Hey my name is Olivier!")
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            socket.close()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            pos_x = int(pos[0] // CELL_SIZE_X)
            pos_y = int(pos[1] // CELL_SIZE_Y)
            message = "ADD " + str(pos_x) + " " + str(pos_y)
            pygame.draw.rect(windowSurface, GREEN, (pos_x * CELL_SIZE_X, pos_y * CELL_SIZE_Y, CELL_SIZE_X, CELL_SIZE_Y))
            pygame.display.update()
            arr = bytearray(message, 'utf-8')
            socket.send(arr)
