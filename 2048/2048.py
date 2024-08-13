import pygame
from random import randint

pygame.init()
win = pygame.display.set_mode((400, 400))
pygame.display.set_caption("2048")

font24 = pygame.font.SysFont('cambria', 24)
font32 = pygame.font.SysFont('cambria', 32)
font42 = pygame.font.SysFont('cambria', 42)
font72 = pygame.font.SysFont('cambria', 72)

INITIAL_NUMBER = 16


def random_square_location() -> tuple[int, int]:
    return randint(0, 3), randint(0, 3)


def draw(lst) -> None:
    z = 0
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] != 0:
                x = j * 100 if 1 <= j <= 3 else 0
                y = i * 100 if 1 <= i <= 3 else 0

                pygame.draw.rect(win, colour(lst[i][j]), (x, y, 100, 100))

                title = font42.render(str(lst[i][j]), True, (255, 255, 255))

                if len(str(lst[i][j])) == 4:
                    z = 0  # four-digit number
                elif len(str(lst[i][j])) == 3:
                    z = 15  # triple digit number
                elif len(str(lst[i][j])) == 2:
                    z = 25  # double-digit number
                elif len(str(lst[i][j])) == 1:
                    z = 35  # single digit number

                win.blit(title, (x + z, y + 20))


def colour(num) -> tuple[int, int, int]:
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


def draw_grid(w, rows, surface) -> None:
    size_between = w // rows
    x = y = 0
    for i in range(rows):
        x += size_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        if i < rows:
            y += size_between
            pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def randomize(lst) -> None:
    while True:
        a, b = random_square_location()
        if lst[a][b] == 0:
            lst[a][b] = 2
            break


def is_game_playable(lst) -> bool:
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == 0:
                return True

    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if (j != 0 and lst[i][j] == lst[i][j - 1]) or (i != 0 and lst[i][j] == lst[i - 1][j]) or (
                    j != 3 and lst[i][j] == lst[i][j + 1]) or (i != 3 and lst[i][j] == lst[i + 1][j]):
                return True

    return False


def left(lst) -> int:
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


def up(lst) -> int:
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


def right(lst) -> int:
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


def down(lst) -> int:
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


def start_menu(surface) -> bool:
    surface.fill((0, 0, 0))
    while True:
        title = font72.render('2048', True, (255, 0, 0))
        prompt = font24.render('Press ENTER to start the game...', True, (225, 225, 225))
        surface.blit(title, (130, 100))
        surface.blit(prompt, (40, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    return True


def game_over(surface, score) -> None:
    surface.fill((0, 0, 0))

    title = font72.render('Game Over', True, (255, 0, 0))
    prompt = font32.render('Your Score: ' + str(score), True, (0, 0, 255))
    surface.blit(title, (30, 100))
    surface.blit(prompt, (100, 200))

    pygame.display.update()

    pygame.time.delay(1200)
    pygame.time.Clock().tick(5)


square = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
score = 0

while True:
    x1, y1 = random_square_location()
    x2, y2 = random_square_location()
    if x1 != x2 or y1 != y2:
        square[x1][y1] = square[x2][y2] = INITIAL_NUMBER
        break

run = start_menu(win)
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
                score += up(square)
                randomize(square)
                break
            elif keys[pygame.K_DOWN]:
                score += down(square)
                randomize(square)
                break
            elif keys[pygame.K_LEFT]:
                score += left(square)
                randomize(square)
                break
            elif keys[pygame.K_RIGHT]:
                score += right(square)
                randomize(square)
                break

    win.fill((0, 0, 0))
    draw_grid(400, 4, win)
    draw(square)
    if not is_game_playable(square):
        run = False
        game_over(win, score)

pygame.quit()
