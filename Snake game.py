import pygame
from random import randrange

pygame.init()
win = pygame.display.set_mode((500, 540))
pygame.display.set_caption("Snake game")


class Cube(object):
	rows = 20
	w = 500
	def __init__(self, start, color = (0, 255, 0)):
		self.pos = start
		self.dirx = 1
		self.diry = 0
		self.color = color

	def move(self, dirx, diry):
		self.dirx = dirx
		self.diry = diry
		self.pos = (self.pos[0] + dirx, self.pos[1] + diry)

	def draw(self, surface, eyes = False):
		dis = self.w//self.rows
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
		if eyes:
			centre = dis//2
			radius = 3
			circleMiddle = (i*dis+centre-radius, j*dis+8)
			circleMiddle2 = (i*dis + dis-radius*2, j*dis+8)
			pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
			pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class Snake(object):
	body = []
	turns = {}
	def __init__(self, color, pos):
		self.color = color
		self.head = Cube(pos)
		self.body.append(self.head)
		self.dirx = 0
		self.diry = 0

	def move(self):
		Continue = True
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Continue = False
			else:
				keys = pygame.key.get_pressed()

				for key in keys:
					if keys[pygame.K_UP] and self.diry != 1:
						self.dirx = 0
						self.diry = -1
						self.turns[self.head.pos[:]] = [self.dirx, self.diry]

					elif keys[pygame.K_DOWN] and self.diry != -1:
						self.dirx = 0
						self.diry = 1
						self.turns[self.head.pos[:]] = [self.dirx, self.diry]

					elif keys[pygame.K_LEFT] and self.dirx != 1:
						self.dirx = -1
						self.diry = 0
						self.turns[self.head.pos[:]] = [self.dirx, self.diry]

					elif keys[pygame.K_RIGHT] and self.dirx != -1:
						self.dirx = 1
						self.diry = 0
						self.turns[self.head.pos[:]] = [self.dirx, self.diry]


		if Continue:
			for i, c in enumerate(self.body):
				p = c.pos[:]
				if p in self.turns:
					turn = self.turns[p]
					c.move(turn[0], turn[1])
					if i == len(self.body)-1:
						self.turns.pop(p)
				else:
					if c.dirx == -1 and c.pos[0] <= 0:
						c.pos = (c.rows-1, c.pos[1])
					elif c.dirx == 1 and c.pos[0] >= c.rows-1:
						c.pos = (0, c.pos[1])
					elif c.diry == -1 and c.pos[1] <= 0:
						c.pos = (c.pos[0], c.rows-1)
					elif c.diry == 1 and c.pos[1] >= c.rows-1:
						c.pos = (c.pos[0], 0)
					else:
						c.move(c.dirx, c.diry)

		return Continue

	def reset(self, pos):
		self.head = Cube(pos)
		self.body = []
		self.body.append(self.head)
		self.addCube()
		self.addCube()
		self.turns = {}
		self.dirx = 0
		self.diry = 0


	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dirx, tail.diry

		if dx == 1 and dy == 0:
			self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
		elif dx == 0 and dy == 1:
			self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
		elif dx == 0 and dy == -1:
			self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

		self.body[-1].dirx = dx
		self.body[-1].diry = dy


	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i == 0:
				c.draw(surface, True)
			else:
				c.draw(surface)


def redrawWindow(surface):
	global width, s, snk
	surface.fill((0, 0, 0))
	s.draw(surface)
	snk.draw(surface)
	pygame.draw.line(surface, (0, 0, 255), (0, width), (width, width))
	text = font.render('Score: {}'.format(len(s.body)-3), True, (0, 0, 255))
	win.blit(text, (10, 500))

	pygame.display.update()


def snack(rows, item):
	position = item.body
	run = True
	while run:
		x = randrange(rows)
		y = randrange(rows)
		if len(list(filter(lambda z:z.pos == (x,y), position))) > 0:
			continue
		else:
			run = False

	return (x, y)


def startMenu(surface):
	surface.fill((0, 0, 0))
	fnt1 = pygame.font.SysFont('cambria', 72)
	fnt2 = pygame.font.SysFont('cambria', 16)

	start = False
	run = True
	dis = width//rows

	while run:
		title = fnt1.render('Snake Game', True, (0, 255, 0))
		surface.blit(title, (50, 100))

		pygame.draw.rect(surface, (0, 255, 0), (10*dis-25, 10*dis+1, dis-2, dis-2))

		pygame.draw.circle(surface, (0, 0, 0), (10*dis-8, 10*dis+8), 3)
		pygame.draw.circle(surface, (0, 0, 0), (10*dis-17, 10*dis+8), 3)

		pygame.draw.rect(surface, (0, 255, 0), (10*dis-50, 10*dis+1, dis-2, dis-2))
		pygame.draw.rect(surface, (0, 255, 0), (10*dis-75, 10*dis+1, dis-2, dis-2))

		pygame.draw.rect(surface, (255, 0, 0), (10*dis+25, 10*dis+1, dis-2, dis-2))

		prompt =  fnt2.render('Press ENTER to start the game....', True, (255, 0, 0))
		surface.blit(prompt, (125, 350))

		pygame.display.update()

		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				else:
					keys = pygame.key.get_pressed()

					for key in keys:
						if keys[pygame.K_RETURN]:
							run = False
							start = True


	return start


def gameOver(surface, score):
	surface.fill((0, 0, 0))
	fnt1 = pygame.font.SysFont('cambria', 72)
	fnt2 = pygame.font.SysFont('cambria', 32)

	run = True

	title = fnt1.render('Game Over', True, (255, 0, 0))
	surface.blit(title, (70, 100))

	prompt =  fnt2.render('Your Score: {}'.format(score), True, (0, 0, 255))
	surface.blit(prompt, (130, 300))

	pygame.display.update()

	pygame.time.delay(1100)
	pygame.time.Clock().tick(5)

	if startMenu(win):
		gamePlay(win)



def gamePlay(surface):
	global snk, s, font
	s.reset((10, 10))
	run = True
	while run:
		pygame.time.delay(50)
		clock.tick(10)
		if s.move():
			if s.body[0].pos == snk.pos:
				s.addCube()
				snk = Cube(snack(rows, s), (255, 0, 0))

			for x in range(len(s.body)):
				if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
					gameOver(win, len(s.body)-3)
					run = False
					break
			redrawWindow(surface)
		else:
			run = False


width = 500
rows = 20
s = Snake((255, 0, 0), (10, 10))
s.addCube()
s.addCube()
snk = Cube(snack(rows, s), (255, 0, 0))
clock = pygame.time.Clock()

font = pygame.font.SysFont('cambria', 32)

if startMenu(win):
	gamePlay(win)

pygame.quit()
