import pygame

from random import randrange
from snake import Snake
from square import Square

pygame.init()
win = pygame.display.set_mode((500, 540))
pygame.display.set_caption("Snake game")

font32 = pygame.font.SysFont('cambria', 32)
font72 = pygame.font.SysFont('cambria', 72)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

score = 0


def redraw_window(surface) -> None:
    global width, s, snk
    surface.fill(BLACK)
    s.draw(surface)
    snk.draw(surface)
    pygame.draw.line(surface, WHITE, (0, width), (width, width))
    text = font32.render('Score: {}'.format(score), True, WHITE)
    win.blit(text, (10, 505))

    pygame.display.update()


def food(position) -> tuple[int, int]:
    global rows
    while True:
        pos = (randrange(rows), randrange(rows))
        if len(list(filter(lambda z: z.pos == pos, position))) <= 0:
            return pos


def start_menu(surface) -> bool:
    surface.fill(BLACK)
    dis = width // rows
    while True:
        title = font72.render('Snake Game', True, GREEN)
        surface.blit(title, (60, 100))
        # Head
        pygame.draw.rect(surface, GREEN, (10 * dis - 25, 10 * dis + 1, dis - 2, dis - 2))
        # Eyes
        pygame.draw.circle(surface, BLACK, (10 * dis - 8, 10 * dis + 8), 3)
        pygame.draw.circle(surface, BLACK, (10 * dis - 17, 10 * dis + 8), 3)
        # Body
        pygame.draw.rect(surface, GREEN, (10 * dis - 50, 10 * dis + 1, dis - 2, dis - 2))
        pygame.draw.rect(surface, GREEN, (10 * dis - 75, 10 * dis + 1, dis - 2, dis - 2))
        # Food
        pygame.draw.rect(surface, RED, (10 * dis + 25, 10 * dis + 1, dis - 2, dis - 2))

        prompt = font32.render('Press ENTER to start the game...', True, WHITE)
        surface.blit(prompt, (35, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    return True


def game_over(surface) -> None:
    global score
    title = font72.render('Game Over', True, (255, 0, 0))
    prompt = font32.render('Your Score: ' + str(score), True, WHITE)

    surface.fill(BLACK)
    surface.blit(title, (80, 100))
    surface.blit(prompt, (150, 300))

    pygame.display.update()
    pygame.time.delay(2500)
    pygame.time.Clock().tick(5)

    score = 0
    if start_menu(win):
        game_play(win)


def game_play(surface) -> None:
    global snk, s, score
    s.reset((10, 10))
    run = True
    while run:
        pygame.time.delay(120)
        clock.tick(10)
        if s.move():
            if s.body[0].pos == snk.pos:
                score += 1
                s.add_square()
                snk = Square(food(s.body), RED)

            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                    game_over(win)
                    run = False
                    break
            redraw_window(surface)
        else:
            run = False


width, rows = 500, 20
s = Snake((10, 10))
s.add_square()
s.add_square()
snk = Square(food(s.body), RED)
clock = pygame.time.Clock()

if start_menu(win):
    game_play(win)


pygame.quit()
