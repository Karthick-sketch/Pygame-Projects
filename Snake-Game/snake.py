import pygame

from square import Square


class Snake(object):
    def __init__(self, pos):
        self.head = Square(pos)
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
        self.head = Square(pos)
        self.body = [self.head]
        self.add_square()
        self.add_square()
        self.turns = {}
        self.dir_x = self.dir_y = 0

    def add_square(self) -> None:
        tail = self.body[-1]
        dx, dy = tail.dir_x, tail.dir_y

        if dx == 1 and dy == 0:
            self.body.append(Square((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Square((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Square((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Square((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dir_x = dx
        self.body[-1].dir_y = dy

    def draw(self, surface) -> None:
        for i, c in enumerate(self.body):
            c.draw(surface, i == 0)
