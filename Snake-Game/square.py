import pygame


class Square(object):
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
