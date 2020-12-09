import pygame
from network import Network
from player import Player

pygame.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))
FPS = 60





def redrawWindow(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)

    pygame.display.update()



def main():
    run = True
    n = Network()
    p = n.getP()

    clock = pygame.time.Clock()
    while run:
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        p.move()
        redrawWindow(win, p, p2)

        clock.tick(FPS)

    pygame.quit()


main()
