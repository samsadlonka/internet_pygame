import pygame
from network_rock_paper_scissors import Network
import pickle

pygame.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')
FPS = 60


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 40)
        text = font.render(self.text, True, (255, 255, 255))
        d_x, d_y = self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2
        win.blit(text, (self.x + d_x, self.y + d_y))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and \
                self.y <= y1 <= self.y + self.height:
            return True
        return False


def redrawWindow(win, game, p):
    win.fill((120, 120, 120))

    if not game.connected():
        font = pygame.font.Font(None, 80)
        text = font.render('Waiting for player...', True, (255, 0, 0), True)
        win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    else:
        font = pygame.font.Font(None, 60)
        text = font.render('Your Move', True, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render('Opponents', True, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.both_went():
            text1 = font.render(move1, True, (0, 0, 0))
            text2 = font.render(move2, True, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, True, (0, 0, 0))
            elif game.p1Went and p == 1:
                text1 = font.render('Locked in', True, (0, 0, 0))
            else:
                text1 = font.render('Waiting...', True, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, True, (0, 0, 0))
            elif game.p2Went and p == 0:
                text2 = font.render('Locked in', True, (0, 0, 0))
            else:
                text2 = font.render('Waiting...', True, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button('Rock', 50, 500, (0, 0, 0)), Button('Scissors', 250, 500, (255, 0, 0)),
        Button('Paper', 450, 500, (0, 255, 0))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print('You are player', player)

    while run:
        clock.tick(FPS)
        try:
            game = n.send('get')
        except:
            run = False
            print("Couldn't get game")
            break
        if game.both_went():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send('reset')
            except:
                run = False
                print("Couldn't get game")

            font = pygame.font.Font(None, 90)
            if (game.winner() == 1 and player == 1) or \
                    (game.winner() == 0 and player == 0):
                text = font.render('You won!', True, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render('Tie game!', True, (255, 0, 0))
            else:
                text = font.render('You Lost...', True, (255, 0, 0))

            win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    if btn.click(event.pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    win.fill((120, 120, 120))
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

        win.fill((120, 120, 120))
        font = pygame.font.Font(None, 60)
        text = font.render('Click to play!', True, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

    main()


while True:
    menu_screen()
