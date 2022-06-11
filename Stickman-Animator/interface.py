class Container:
    def __init__(self, pygame, win, text, pos, fontSize, padding, fontColor, borderColor, borderSize):
        self.pygame = pygame
        self.window = win
        self.text = text
        self.x, self.y = pos
        self.paddingTop, self.paddingBottom = padding[0], padding[1]*2
        self.paddingLeft, self.paddingRight = padding[2], padding[3]*2
        self.font = self.pygame.font.SysFont("Arial", fontSize)
        self.color = fontColor
        self.borderColor, self.borderSize = borderColor, borderSize

    def draw(self, backgroundColor, size, length):
        self.size = size
        self.surface = self.pygame.Surface((self.size[0]+self.paddingRight, self.size[1]+self.paddingBottom))
        self.surface.fill(backgroundColor)
        self.rect = self.pygame.Rect(
            self.x - self.borderSize,
            self.y - self.borderSize,
            length[0] + (self.paddingRight + self.borderSize),
            length[1] + (self.paddingBottom + self.borderSize)
        )

    def show(self, size):
        self.window.blit(self.surface, (self.x, self.y))
        self.pygame.draw.rect(
            self.window,
            self.borderColor,
            self.pygame.Rect(self.x - self.borderSize,
            self.y - self.borderSize,
            size[0] + (self.paddingRight + self.borderSize),
            size[1] + (self.paddingBottom + self.borderSize)),
            self.borderSize
        )

    def click(self):
        x, y = self.pygame.mouse.get_pos()
        return self.rect.collidepoint(x, y)


class Button(Container):
    def __init__(self, pygame, win, text, pos, fontSize, padding=(0, 0, 0, 0), fontColor=(0, 0, 0), backgroundColor=(211, 211, 211), borderColor=(255, 255, 255), borderSize=2):
        super().__init__(pygame, win, text, pos, fontSize, padding, fontColor, borderColor, borderSize)
        self.draw(backgroundColor)

    def draw(self, backgroundColor):
        self.textNode = self.font.render(self.text, True, self.color)
        self.size = self.textNode.get_size()
        super().draw(backgroundColor, self.size, (self.x, self.y))
        self.surface.blit(self.textNode, (self.paddingLeft, self.paddingTop))

    def show(self):
        super().show(self.size)

    def select(self, selected):
        self.draw(((255 if selected else 0), 0, 0))


class Input(Container):
    def __init__(self, pygame, win, pos, fontSize, padding=(0, 0, 0, 0), fontColor=(0, 0, 0), backgroundColor=(255, 255, 255), borderColor=(100, 100, 100), borderSize=2):
        super().__init__(pygame, win, '', (pos[0], pos[1]), fontSize, padding, fontColor, borderColor, borderSize)
        self.backgroundColor = backgroundColor
        self.focus = False; self.length = (pos[2], pos[3])
        self.draw()

    def draw(self):
        self.textNode = self.font.render(self.text, True, self.color)
        self.size = self.textNode.get_size()
        super().draw(self.backgroundColor, self.size, self.length)
        self.surface.blit(self.textNode, (self.paddingLeft, self.paddingTop))

    def show(self):
        if self.focus:
            self.draw()

        super().show(self.length)
