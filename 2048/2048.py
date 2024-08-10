import pygame
from random import randint

pygame.init()
win = pygame.display.set_mode((400, 400))
pygame.display.set_caption("2048")

font24 = pygame.font.SysFont('cambria', 24)
font32 = pygame.font.SysFont('cambria', 32)
font42 = pygame.font.SysFont('cambria', 42)
font72 = pygame.font.SysFont('cambria', 72)


def draw(lst):
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] != 0:
                x = j * 100 if 1 <= j <= 3 else 0
                y = i * 100 if 1 <= i <= 3 else 0

                pygame.draw.rect(win, colour(lst[i][j]), (x, y, 100, 100))

                title = font42.render(str(lst[i][j]), True, (255, 255, 255))

                if len(str(lst[i][j])) == 4:
                    z = 0  # four digit number
                elif len(str(lst[i][j])) == 3:
                    z = 15  # triple digit number
                elif len(str(lst[i][j])) == 2:
                    z = 25  # double digit number
                elif len(str(lst[i][j])) == 1:
                    z = 35  # single digit number

                win.blit(title, (x + z, y + 20))


def colour(num):
    clr = (0, 0, 0)
    if num == 2:
        clr = (255, 0, 0)
    elif num == 4:
        clr = (255, 128, 0)
    elif num == 8:
        clr = (255, 255, 0)
    elif num == 16:
        clr = (128, 255, 0)
    elif num == 32:
        clr = (0, 255, 0)
    elif num == 64:
        clr = (0, 255, 128)
    elif num == 128:
        clr = (0, 255, 255)
    elif num == 256:
        clr = (0, 128, 255)
    elif num == 512:
        clr = (0, 0, 255)
    elif num == 1024:
        clr = (127, 0, 255)
    elif num == 2048:
        clr = (255, 0, 255)
    elif num == 4096:
        clr = (255, 0, 127)
    elif num == 8192:
        clr = (128, 128, 128)

    return clr


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = y = 0

    for l in range(rows):
        x += sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        if l < rows:
            y += sizeBtwn
            pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def randomize(lst):
    a, b = randint(0, 3), randint(0, 3)

    i = 0
    while lst[a][b] != 0 and i < 32:
        a, b = randint(0, 3), randint(0, 3)
        i += 1

    if i < 32: lst[a][b] = 2


def isGameOver(lst):
    run = False
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == 0:
                run = True
                break

        if run: break

    if not run:
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                run = (
                        (j != 0 and lst[i][j] == lst[i][j - 1]) or
                        (i != 0 and lst[i][j] == lst[i - 1][j]) or
                        (j != 3 and lst[i][j] == lst[i][j + 1]) or
                        (i != 3 and lst[i][j] == lst[i + 1][j])
                )
                if run: break

            if run: break

    return run


def left(lst):
    score = 0
    for i in range(len(lst)):
        for j in range(len(lst)):
            if lst[i][2] == 0:
                lst[i][2], lst[i][3] = lst[i][3], lst[i][2]
            if lst[i][1] == 0:
                lst[i][1], lst[i][2] = lst[i][2], lst[i][1]
            if lst[i][0] == 0:
                lst[i][0], lst[i][1] = lst[i][1], lst[i][0]

        if lst[i][0] != 0 and lst[i][1] != 0 and lst[i][0] == lst[i][1]:
            lst[i][0] *= 2
            score += lst[i][0]
            lst[i][1] = lst[i][2]
            lst[i][2] = lst[i][3]
            lst[i][3] = 0
            if lst[i][0] != 0 and lst[i][1] != 0 and lst[i][2] == lst[i][1]:
                lst[i][1] *= 2
                score += lst[i][1]
                lst[i][2] = lst[i][3]
                lst[i][3] = 0
        elif lst[i][1] != 0 and lst[i][2] != 0 and lst[i][1] == lst[i][2]:
            lst[i][1] *= 2
            score += lst[i][1]
            lst[i][2] = lst[i][3]
            lst[i][3] = 0
        elif lst[i][2] != 0 and lst[i][3] != 0 and lst[i][2] == lst[i][3]:
            lst[i][2] *= 2
            score += lst[i][2]
            lst[i][3] = 0

    return score


def up(lst):
    score = 0
    for i in range(len(lst)):
        for j in range(len(lst)):
            if lst[2][i] == 0:
                lst[2][i], lst[3][i] = lst[3][i], lst[2][i]
            if lst[1][i] == 0:
                lst[1][i], lst[2][i] = lst[2][i], lst[1][i]
            if lst[0][i] == 0:
                lst[0][i], lst[1][i] = lst[1][i], lst[0][i]

        if lst[0][i] != 0 and lst[1][i] != 0 and lst[0][i] == lst[1][i]:
            lst[0][i] *= 2
            score += lst[0][i]
            lst[1][i] = lst[2][i]
            lst[2][i] = lst[3][i]
            lst[3][i] = 0
            if lst[2][i] != 0 and lst[1][i] != 0 and lst[2][i] == lst[1][i]:
                lst[1][i] *= 2
                score += lst[1][i]
                lst[2][i] = lst[3][i]
                lst[3][i] = 0
        elif lst[1][i] != 0 and lst[2][i] != 0 and lst[1][i] == lst[2][i]:
            lst[1][i] *= 2
            score += lst[1][i]
            lst[2][i] = lst[3][i]
            lst[3][i] = 0
        elif lst[2][i] != 0 and lst[3][i] != 0 and lst[2][i] == lst[3][i]:
            lst[2][i] *= 2
            score += lst[2][i]
            lst[3][i] = 0

    return score


def right(lst):
    score = 0
    for i in range(len(lst)):
        for j in range(len(lst)):
            if lst[i][1] == 0:
                lst[i][0], lst[i][1] = lst[i][1], lst[i][0]
            if lst[i][2] == 0:
                lst[i][1], lst[i][2] = lst[i][2], lst[i][1]
            if lst[i][3] == 0:
                lst[i][3], lst[i][2] = lst[i][2], lst[i][3]

        if lst[i][2] != 0 and lst[i][3] != 0 and lst[i][2] == lst[i][3]:
            lst[i][3] *= 2
            score += lst[i][3]
            lst[i][2] = lst[i][1]
            lst[i][1] = lst[i][0]
            lst[i][0] = 0
            if lst[i][1] != 0 and lst[i][2] != 0 and lst[i][1] == lst[i][2]:
                lst[i][2] *= 2
                score += lst[i][2]
                lst[i][1] = lst[i][0]
                lst[i][0] = 0
        elif lst[i][1] != 0 and lst[i][2] != 0 and lst[i][1] == lst[i][2]:
            lst[i][2] *= 2
            score += lst[i][2]
            lst[i][1] = lst[i][0]
            lst[i][0] = 0
        elif lst[i][1] != 0 and lst[i][0] != 0 and lst[i][1] == lst[i][0]:
            lst[i][1] *= 2
            score += lst[i][1]
            lst[i][0] = 0

    return score


def down(lst):
    score = 0
    for i in range(len(lst)):
        for j in range(len(lst)):
            if lst[1][i] == 0:
                lst[1][i], lst[0][i] = lst[0][i], lst[1][i]
            if lst[2][i] == 0:
                lst[1][i], lst[2][i] = lst[2][i], lst[1][i]
            if lst[3][i] == 0:
                lst[2][i], lst[3][i] = lst[3][i], lst[2][i]

        if lst[3][i] != 0 and lst[3][i] == lst[2][i]:
            lst[3][i] *= 2
            score += lst[3][i]
            lst[2][i] = lst[1][i]
            lst[1][i] = lst[0][i]
            lst[0][i] = 0
            if lst[2][i] != 0 and lst[2][i] == lst[1][i]:
                lst[2][i] *= 2
                score += lst[2][i]
                lst[1][i] = lst[0][i]
                lst[0][i] = 0
        elif lst[2][i] != 0 and lst[1][i] == lst[2][i]:
            lst[2][i] *= 2
            score += lst[2][i]
            lst[1][i] = lst[0][i]
            lst[0][i] = 0
        elif lst[1][i] != 0 and lst[1][i] == lst[0][i]:
            lst[1][i] *= 2
            score += lst[1][i]
            lst[0][i] = 0

    return score


def startMenu(surface, width, rows):
    surface.fill((0, 0, 0))
    start, run = False, True
    while run:
        title = font72.render('2048', True, (255, 0, 0))
        prompt = font24.render('Press ENTER to start the game...', True, (255, 255, 255))
        surface.blit(title, (130, 100))
        surface.blit(prompt, (40, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            else:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_RETURN]:
                    run, start = False, True

    return start


def gameOver(surface, score):
    surface.fill((0, 0, 0))

    title = font72.render('Game Over', True, (255, 0, 0))
    prompt = font32.render('Your Score: ' + str(score), True, (0, 0, 255))
    surface.blit(title, (30, 100))
    surface.blit(prompt, (100, 200))

    pygame.display.update()

    pygame.time.delay(1200)
    pygame.time.Clock().tick(5)


lst = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
score = 0

x1 = x2 = y2 = y2 = 0
while True:
    x1, y1 = randint(0, 3), randint(0, 3)
    x2, y2 = randint(0, 3), randint(0, 3)
    if x1 != x2 or y1 != y2: break

lst[x1][y1] = lst[x2][y2] = 2

run = startMenu(win, 400, 4)
while run:
    pygame.display.update()
    pygame.time.delay(50)
    pygame.time.Clock().tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        else:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                score += up(lst)
                randomize(lst)
                break
            elif keys[pygame.K_DOWN]:
                score += down(lst)
                randomize(lst)
                break
            elif keys[pygame.K_LEFT]:
                score += left(lst)
                randomize(lst)
                break
            elif keys[pygame.K_RIGHT]:
                score += right(lst)
                randomize(lst)
                break

    win.fill((0, 0, 0))
    drawGrid(400, 4, win)
    draw(lst)
    if not isGameOver(lst):
        run = False
        gameOver(win, score)

pygame.quit()
