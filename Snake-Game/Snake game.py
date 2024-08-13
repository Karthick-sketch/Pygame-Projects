import pygame
from random import randrange

pygame.init()
win = pygame.display.set_mode((500, 540))
pygame.display.set_caption("Snake game")

font32 = pygame.font.SysFont('cambria', 32)
font72 = pygame.font.SysFont('cambria', 72)


class Cube(object):
    rows, w = 20, 500

    def __init__(self, start, color=(0, 255, 0)):
        self.pos = start
        self.dir_x, self.dir_y = 1, 0
        self.color = color

    def move(self, dir_x, dir_y) -> None:
        self.dir_x, self.dir_y = dir_x, dir_y
        self.pos = (self.pos[0] + dir_x, self.pos[1] + dir_y)

    def draw(self, surface, eyes=False) -> None:
        dis = self.w // self.rows
        i, j = self.pos[0], self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            centre, radius = dis // 2, 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class Snake(object):
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.dir_x = self.dir_y = 0

    def move(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            else:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP] and self.dir_y != 1:
                    self.dir_x, self.dir_y = 0, -1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_DOWN] and self.dir_y != -1:
                    self.dir_x, self.dir_y = 0, 1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_LEFT] and self.dir_x != 1:
                    self.dir_x, self.dir_y = -1, 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_RIGHT] and self.dir_x != -1:
                    self.dir_x, self.dir_y = 1, 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dir_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dir_x == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dir_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                elif c.dir_y == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                else:
                    c.move(c.dir_x, c.dir_y)

        return True

    def reset(self, pos) -> None:
        self.head = Cube(pos)
        self.body = [self.head]
        self.add_square()
        self.add_square()
        self.turns = {}
        self.dir_x = self.dir_y = 0

    def add_square(self) -> None:
        tail = self.body[-1]
        dx, dy = tail.dir_x, tail.dir_y

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dir_x = dx
        self.body[-1].dir_y = dy

    def draw(self, surface) -> None:
        for i, c in enumerate(self.body):
            c.draw(surface, i == 0)


def redraw_window(surface) -> None:
    global width, s, snk
    surface.fill((0, 0, 0))
    s.draw(surface)
    snk.draw(surface)
    pygame.draw.line(surface, (0, 0, 255), (0, width), (width, width))
    text = font32.render('Score: {}'.format(len(s.body) - 3), True, (0, 0, 255))
    win.blit(text, (10, 500))

    pygame.display.update()


def food(rows, item) -> tuple[int, int]:
    position = item.body
    while True:
        pos = (randrange(rows), randrange(rows))
        if len(list(filter(lambda z: z.pos == pos, position))) <= 0:
            return pos


def start_menu(surface) -> bool:
    surface.fill((0, 0, 0))
    dis = width // rows
    while True:
        title = font72.render('Snake Game', True, (0, 255, 0))
        surface.blit(title, (60, 100))
        # Head
        pygame.draw.rect(surface, (0, 255, 0), (10 * dis - 25, 10 * dis + 1, dis - 2, dis - 2))
        # Eyes
        pygame.draw.circle(surface, (0, 0, 0), (10 * dis - 8, 10 * dis + 8), 3)
        pygame.draw.circle(surface, (0, 0, 0), (10 * dis - 17, 10 * dis + 8), 3)
        # Body
        pygame.draw.rect(surface, (0, 255, 0), (10 * dis - 50, 10 * dis + 1, dis - 2, dis - 2))
        pygame.draw.rect(surface, (0, 255, 0), (10 * dis - 75, 10 * dis + 1, dis - 2, dis - 2))
        # Food
        pygame.draw.rect(surface, (255, 0, 0), (10 * dis + 25, 10 * dis + 1, dis - 2, dis - 2))

        prompt = font32.render('Press ENTER to start the game...', True, (0, 0, 255))
        surface.blit(prompt, (35, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    return True


def game_over(surface, score) -> None:
    title = font72.render('Game Over', True, (255, 0, 0))
    prompt = font32.render('Your Score: ' + str(score), True, (0, 0, 255))

    surface.fill((0, 0, 0))
    surface.blit(title, (80, 100))
    surface.blit(prompt, (130, 300))

    pygame.display.update()
    pygame.time.delay(1200)
    pygame.time.Clock().tick(5)

    if start_menu(win):
        game_play(win)


def game_play(surface) -> None:
    global snk, s
    s.reset((10, 10))
    run = True
    while run:
        pygame.time.delay(50)
        clock.tick(10)
        if s.move():
            if s.body[0].pos == snk.pos:
                s.add_square()
                snk = Cube(food(rows, s), (255, 0, 0))

            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                    game_over(win, len(s.body) - 3)
                    run = False
                    break
            redraw_window(surface)
        else:
            run = False


width, rows = 500, 20
s = Snake((255, 0, 0), (10, 10))
s.add_square()
s.add_square()
snk = Cube(food(rows, s), (255, 0, 0))
clock = pygame.time.Clock()

if start_menu(win):
    game_play(win)

pygame.quit()
