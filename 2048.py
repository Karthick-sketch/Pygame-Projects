import pygame
from random import randrange

pygame.init()
win = pygame.display.set_mode((400, 400))
pygame.display.set_caption("2048")


fnt = pygame.font.SysFont('cambria', 42)



def draw(lst):
	for i in range(len(lst)):
		for j in range(len(lst[i])):
			if lst[i][j] != 0:
				if j == 0:		x = 0;
				elif j == 1:	x = 100;
				elif j == 2:	x = 200;
				elif j == 3:	x = 300;

				if i == 0:		y = 0;
				elif i == 1:	y = 100;
				elif i == 2:	y = 200;
				elif i == 3:	y = 300;

				pygame.draw.rect(win, colour(lst[i][j]), (x, y, 100, 100))

				title = fnt.render(str(lst[i][j]), True, (255, 255, 255))

				if len(str(lst[i][j])) == 3:		z = 15	# triple
				elif len(str(lst[i][j])) == 2:	z = 25	# double
				elif len(str(lst[i][j])) == 1:	z = 35	# single

				win.blit(title, (x+z, y+20));



def colour(num):
	clr = (0, 0, 0)
	if num == 2:	clr = (255, 0, 0)
	elif num == 4:	clr = (255, 128, 0)
	elif num == 8:	clr = (255, 255, 0)
	elif num == 16:	clr = (128, 255, 0)
	elif num == 32:	clr = (0, 255, 0)
	elif num == 64:	clr = (0, 255, 128)
	elif num == 128:	clr = (0, 255, 255)
	elif num == 256:	clr = (0, 128, 255)
	elif num == 512:	clr = (0, 0, 255)
	elif num == 1024:	clr = (127, 0, 255)
	elif num == 2048:	clr = (255, 0, 255)
	elif num == 4096:	clr = (255, 0, 127)
	elif num == 8192:	clr = (128, 128, 128)
	return clr



def drawGrid(w, rows, surface):
	sizeBtwn = w//rows
	x = 0
	y = 0

	for l in range(rows):
		x += sizeBtwn
		pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
		if l < rows:
			y += sizeBtwn
			pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


from random import randint;

def randomize(lst):
	a, b = randint(0,3), randint(0,3);

	i = 0;
	while lst[a][b] != 0 and i < 32:
		a, b = randint(0,3), randint(0,3);
		i += 1;

	if i < 32:
		lst[a][b] = 2;


def gameOver(lst):
	run = False;
	for i in range(len(lst)):
		for j in range(len(lst[i])):
			if lst[i][j] == 0:
				run = True;
				break;
		if run:
			break;

	if not run:
		for i in range(len(lst)):
			for j in range(len(lst[i])):
				if j != 0 and lst[i][j] == lst[i][j-1]:
					run = True;
				elif j != 3 and lst[i][j] == lst[i][j+1]:
					run = True;
				elif i != 0 and lst[i][j] == lst[i-1][j]:
					run = True;
				elif i != 3 and lst[i][j] == lst[i+1][j]:
					run = True;
				if run:
				  	break;
			if run:
				break;

	return run;



def left(lst):
	for i in range(len(lst)):
		for j in range(len(lst)):
			if lst[i][2] == 0:
				lst[i][2], lst[i][3] = lst[i][3], lst[i][2];
			if lst[i][1] == 0:
				lst[i][1], lst[i][2] = lst[i][2], lst[i][1];
			if lst[i][0] == 0:
				lst[i][0], lst[i][1] = lst[i][1], lst[i][0];

		if lst[i][0] != 0 and lst[i][1] != 0 and lst[i][0] == lst[i][1]:
			lst[i][0] *= 2;
			lst[i][1] = lst[i][2];
			lst[i][2] = lst[i][3];
			lst[i][3] = 0;
			if lst[i][0] != 0 and lst[i][1] != 0 and lst[i][2] == lst[i][1]:
				lst[i][1] *= 2;
				lst[i][2] = lst[i][3];
				lst[i][3] = 0;
		elif lst[i][1] != 0 and lst[i][2] != 0 and lst[i][1] == lst[i][2]:
			lst[i][1] *= 2;
			lst[i][2] = lst[i][3];
			lst[i][3] = 0;
		elif lst[i][2] != 0 and lst[i][3] != 0 and lst[i][2] == lst[i][3]:
			lst[i][2] *= 2;
			lst[i][3] = 0;



def up(lst):
	for i in range(len(lst)):
		for j in range(len(lst)):
			if lst[2][i] == 0:
				lst[2][i], lst[3][i] = lst[3][i], lst[2][i];
			if lst[1][i] == 0:
				lst[1][i], lst[2][i] = lst[2][i], lst[1][i];
			if lst[0][i] == 0:
				lst[0][i], lst[1][i] = lst[1][i], lst[0][i];

		if lst[0][i] != 0 and lst[1][i] != 0 and lst[0][i] == lst[1][i]:
			lst[0][i] *= 2;
			lst[1][i] = lst[2][i];
			lst[2][i] = lst[3][i];
			lst[3][i] = 0;
			if lst[2][i] != 0 and lst[1][i] != 0 and lst[2][i] == lst[1][i]:
				lst[1][i] *= 2;
				lst[2][i] = lst[3][i];
				lst[3][i] = 0;
		elif lst[1][i] != 0 and lst[2][i] != 0 and lst[1][i] == lst[2][i]:
			lst[1][i] *= 2;
			lst[2][i] = lst[3][i];
			lst[3][i] = 0;
		elif lst[2][i] != 0 and lst[3][i] != 0 and lst[2][i] == lst[3][i]:
			lst[2][i] *= 2;
			lst[3][i] = 0;



def right(lst):
	for i in range(len(lst)):
		for j in range(len(lst)):
			if lst[i][1] == 0:
				lst[i][0], lst[i][1] = lst[i][1], lst[i][0];
			if lst[i][2] == 0:
				lst[i][1], lst[i][2] = lst[i][2], lst[i][1];
			if lst[i][3] == 0:
				lst[i][3], lst[i][2] = lst[i][2], lst[i][3];

		if lst[i][2] != 0 and lst[i][3] != 0 and lst[i][2] == lst[i][3]:
			lst[i][3] *= 2;
			lst[i][2] = lst[i][1];
			lst[i][1] = lst[i][0];
			lst[i][0] = 0;
			if lst[i][1] != 0 and lst[i][2] != 0 and lst[i][1] == lst[i][2]:
				lst[i][2] *= 2;
				lst[i][1] = lst[i][0];
				lst[i][0] = 0;
		elif lst[i][1] != 0 and lst[i][2] != 0 and lst[i][1] == lst[i][2]:
			lst[i][2] *= 2;
			lst[i][1] = lst[i][0];
			lst[i][0] = 0;
		elif lst[i][1] != 0 and lst[i][0] != 0 and lst[i][1] == lst[i][0]:
			lst[i][1] *= 2;
			lst[i][0] = 0;



def down(lst):
	for i in range(len(lst)):
		for j in range(len(lst)):
			if lst[1][i] == 0:
				lst[1][i], lst[0][i] = lst[0][i], lst[1][i];
			if lst[2][i] == 0:
				lst[1][i], lst[2][i] = lst[2][i], lst[1][i];
			if lst[3][i] == 0:
				lst[2][i], lst[3][i] = lst[3][i], lst[2][i];

		if lst[3][i] != 0 and lst[3][i] == lst[2][i]:
			lst[3][i] *= 2;
			lst[2][i] = lst[1][i];
			lst[1][i] = lst[0][i];
			lst[0][i] = 0;
			if lst[2][i] != 0 and lst[2][i] == lst[1][i]:
				lst[2][i] *= 2;
				lst[1][i] = lst[0][i];
				lst[0][i] = 0;
		elif lst[2][i] != 0 and lst[1][i] == lst[2][i]:
			lst[2][i] *= 2;
			lst[1][i] = lst[0][i];
			lst[0][i] = 0;
		elif lst[1][i] != 0 and lst[1][i] == lst[0][i]:
			lst[1][i] *= 2;
			lst[0][i] = 0;



lst = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];

a, b = randint(0,3), randint(0,3);
x, y = randint(0,3), randint(0,3);

while a == x and b == y:
	a, b = randint(0,3), randint(0,3);
	x, y = randint(0,3), randint(0,3);

lst[a][b] = 2;
lst[x][y] = 2;

run = True;
while run:
	pygame.display.update();
	pygame.time.delay(50);
	pygame.time.Clock().tick(10);

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False;
		else:
			keys = pygame.key.get_pressed();

			if keys[pygame.K_UP]:
				up(lst);
				randomize(lst);
				break;
			elif keys[pygame.K_DOWN]:
				down(lst);
				randomize(lst);
				break;
			elif keys[pygame.K_LEFT]:
				left(lst);
				randomize(lst);
				break;
			elif keys[pygame.K_RIGHT]:
				right(lst);
				randomize(lst);
				break;

	win.fill((0, 0, 0));
	drawGrid(400, 4, win);
	draw(lst);
	if not gameOver(lst):
		run = False;
		print("Game over");



pygame.quit();
