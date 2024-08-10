class Container:
    def __init__(self, pygame, win, text, pos, font_size, padding, font_color, border_color, border_size):
        self.pygame = pygame
        self.window = win
        self.text = text
        self.x, self.y = pos
        self.paddingTop, self.padding_bottom = padding[0], padding[1] * 2
        self.paddingLeft, self.padding_right = padding[2], padding[3] * 2
        self.font = self.pygame.font.SysFont("Arial", font_size)
        self.color = font_color
        self.border_color, self.border_size = border_color, border_size

    def draw(self, background_color, size, length):
        self.size = size
        self.surface = self.pygame.Surface((self.size[0] + self.padding_right, self.size[1] + self.padding_bottom))
        self.surface.fill(background_color)
        self.rect = self.pygame.Rect(
            self.x - self.border_size,
            self.y - self.border_size,
            length[0] + (self.padding_right + self.border_size),
            length[1] + (self.padding_bottom + self.border_size)
        )

    def show(self, size):
        self.window.blit(self.surface, (self.x, self.y))
        self.pygame.draw.rect(
            self.window,
            self.border_color,
            self.pygame.Rect(self.x - self.border_size, self.y - self.border_size,
                             size[0] + (self.padding_right + self.border_size),
                             size[1] + (self.padding_bottom + self.border_size)),
            self.border_size
        )

    def click(self):
        x, y = self.pygame.mouse.get_pos()
        return self.rect.collidepoint(x, y)


class Button(Container):
    def __init__(self, pygame, win, text, pos, font_size, padding=(0, 0, 0, 0), font_color=(0, 0, 0),
                 background_color=(211, 211, 211), border_color=(255, 255, 255), border_size=2):
        super().__init__(pygame, win, text, pos, font_size, padding, font_color, border_color, border_size)
        self.draw(background_color)

    def draw(self, background_color):
        self.text_node = self.font.render(self.text, True, self.color)
        self.size = self.text_node.get_size()
        super().draw(background_color, self.size, (self.x, self.y))
        self.surface.blit(self.text_node, (self.paddingLeft, self.paddingTop))

    def show(self):
        super().show(self.size)

    def select(self, selected):
        self.draw(((255 if selected else 0), 0, 0))


class Input(Container):
    def __init__(self, pygame, win, pos, font_size, padding=(0, 0, 0, 0), font_color=(0, 0, 0),
                 background_color=(255, 255, 255), border_color=(100, 100, 100), border_size=2):
        super().__init__(pygame, win, '', (pos[0], pos[1]), font_size, padding, font_color, border_color, border_size)
        self.background_color = background_color
        self.focus = False;
        self.length = (pos[2], pos[3])
        self.draw()

    def draw(self):
        self.text_node = self.font.render(self.text, True, self.color)
        self.size = self.text_node.get_size()
        super().draw(self.background_color, self.size, self.length)
        self.surface.blit(self.text_node, (self.paddingLeft, self.paddingTop))

    def show(self):
        if self.focus:
            self.draw()

        super().show(self.length)
