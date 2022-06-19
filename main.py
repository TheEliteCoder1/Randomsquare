"""
A simple shape manipulation program.
"""

import pygame, random, time
from datetime import datetime
pygame.init()

screenW, screenH = 800, 500
screen = pygame.display.set_mode((screenW, screenH))

fps = 60
clock = pygame.time.Clock()
run = True
start = False

squareVelX = 5
squareVelY = 5

backgroundColor = (255,255,255)
squareW, squareH = 50, 50
bounds = pygame.Rect(0, 0, screenW-squareW, screenH-squareH)
squareColor = (0,0,0)
squareBorderRad = 0
squareBorderWidth = 1
squareSize = (squareW, squareH)
showLines = False
squares = []
prev_time = time.time()
dt = 0
lineWidth = 1
closeLines = False
changeSquareColor = pygame.time.set_timer(pygame.USEREVENT+1, 10)
showStats = True

def draw_text(screen: pygame.Surface, font_file: str, text: str, 
    font_size: int, color: tuple, pos: tuple, backg=None, bold=False, italic=False, underline=False):
    """Draws text to the screen given a font file and text."""
    font = pygame.font.Font(font_file, font_size)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    if backg == None:
        t = font.render(text, 1, color)
    t = font.render(text, 1, color, backg)
    textRect = t.get_rect()
    textRect.center = pos
    screen.blit(t, textRect)

def screenshot():
	now = datetime.now()
	pygame.image.save(screen, f'Randomsquare-{now.strftime("%d-%m-%Y %H-%M-%S")}.png')
	
while run:
	clock.tick(fps)
	now = time.time()
	dt = now - prev_time
	prev_time = now
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()			

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_c: # change color of background
				backgroundColor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
			if event.key == pygame.K_r: # increase border radius
				squareBorderRad += 1
				for square in squares:
					square["squareBorderRad"] = squareBorderRad
			if event.key == pygame.K_t: # decrease border radius
				squareBorderRad -= 1
				for square in squares:
					square["squareBorderRad"] = squareBorderRad
			if event.key == pygame.K_b:
				squareBorderWidth += 1
				for square in squares: # increase border width
					square["squareBorderWidth"] = squareBorderWidth
			if event.key == pygame.K_n:
				squareBorderWidth -= 1
				for square in squares: # decrease border width
					square["squareBorderWidth"] = squareBorderWidth
			if event.key == pygame.K_w:
				squareW += 1
				bounds.width = screenW - squareW
				for square in squares: # increase width
					square["squareW"] = squareW
			if event.key == pygame.K_e:
				squareW -= 1
				bounds.width = screenW - squareW
				for square in squares: # decrease width
					square["squareW"] = squareW
			if event.key == pygame.K_h:
				squareH += 1
				bounds.height = screenH - squareH
				for square in squares: # increase height
					square["squareH"] = squareH
			if event.key == pygame.K_j:
				squareH -= 1
				bounds.height = screenH - squareH
				for square in squares: # decrease height
					square["squareH"] = squareH
			if event.key == pygame.K_RIGHT:
				for square in squares: # increase x position
					square["x"] += 1

			if event.key == pygame.K_LEFT:
				for square in squares:
					square["x"] -= 1 # decrease x position

			if event.key == pygame.K_DOWN:
				for square in squares:
					square["y"] += 1 # increase y position

			if event.key == pygame.K_UP:
				for square in squares:
					square["y"] -= 1 # decrease y position

			if event.key == pygame.K_l:
				showLines = not showLines

			if event.key == pygame.K_p:
				closeLines = not closeLines

			if event.key == pygame.K_BACKSLASH:
				backgroundColor = (0,0,0)

			if event.key == pygame.K_SLASH:
				backgroundColor = (255,255,255)

			if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
				screenshot()

			if event.key == pygame.K_1:
				squares.clear()
				
			if event.key == pygame.K_SPACE:
				start = not start

			if event.key == pygame.K_u:
				squareVelY += 1
				squareVelX += 1

			if event.key == pygame.K_i:
				squareVelY -= 1
				squareVelX -= 1


		if event.type == pygame.USEREVENT+1:
			for square in squares:
				squareColor = (
					random.randint(0, 255),
					random.randint(0, 255),
					random.randint(0, 255)
				)
				square["squareColor"] = squareColor
			

	screen.fill(backgroundColor)
	# Addds and removes square objects
	if pygame.mouse.get_pressed()[0]:
		mpos = pygame.mouse.get_pos()
		if mpos not in [(square["x"], square["y"]) for square in squares]:
			squares.append({
				"x":mpos[0],
				"y":mpos[1],
				"squareColor":squareColor,
				"squareW":squareW,
				"squareH":squareH,
				"squareBorderRad":squareBorderRad,
				"squareBorderWidth":squareBorderWidth
			})
	if pygame.mouse.get_pressed()[2]:
		for square in squares:
			if pygame.Rect(square["x"], square["y"], square["squareW"], square["squareH"]).collidepoint(mpos):
				squares.remove(square)
	if showLines:
		if len(squares) >= 2:
			pygame.draw.lines(screen, squareColor, closed=False, points=[(square["x"], square["y"]) for square in squares], width=lineWidth)

	if start:
		for square in squares:
			if square["x"] > 0 or square["x"] < screenW:
				square["x"] += squareVelX
			if square["y"] > 0 or square["y"] < screenH:
				square["y"] += squareVelY
			else:
				square["x"] = 0
				square["y"] = 0
 
			if square["x"] < 0 or square["x"] > screenW:
				squareVelX *= -1
			if square["y"] < 0 or square["y"] > screenH:
				squareVelY *= -1
	
	for square in squares:
		pygame.draw.rect(
			screen, 
			square["squareColor"],
			(
				square["x"],
				square["y"],
				squareW,
				squareH
			),
			squareBorderWidth,
			squareBorderRad
		)

	if showStats:
		if backgroundColor == (0,0,0):
			statColor = (255,255,255)
		else:
			statColor = (0,0,0)
		draw_text(screen, "fira.ttf", f"BG Color:", 15, statColor, (46, 20))
		draw_text(screen, "fira.ttf", f"X-Velocity:", 15, statColor, (55, 40))
		draw_text(screen, "fira.ttf", f"Y-Velocity:", 15, statColor, (55, 60))
		draw_text(screen, "fira.ttf", f"Width:", 15, statColor, (34, 80))
		draw_text(screen, "fira.ttf", f"Height:", 15, statColor, (36, 100))
		draw_text(screen, "fira.ttf", f"Border Radius:", 15, statColor, (67, 120))
		draw_text(screen, "fira.ttf", f"Border Width:", 15, statColor, (63, 140))
		draw_text(screen, "fira.ttf", f"Objects:", 15, statColor, (40, 160))



		draw_text(screen, "fira.ttf", f"{backgroundColor}", 15, statColor, (180, 20))
		draw_text(screen, "fira.ttf", f"{squareVelX}", 15, statColor, (55+100, 40))
		draw_text(screen, "fira.ttf", f"{squareVelY}", 15, statColor, (55+100, 60))
		draw_text(screen, "fira.ttf", f"{squareW}", 15, statColor, (34+100, 80))
		draw_text(screen, "fira.ttf", f"{squareH}", 15, statColor, (36+100, 100))
		draw_text(screen, "fira.ttf", f"{squareBorderRad}", 15, statColor, (67+100, 120))
		draw_text(screen, "fira.ttf", f"{squareBorderWidth}", 15, statColor, (63+100, 140))
		draw_text(screen, "fira.ttf", f"{len(squares)}", 15, statColor, (40+100, 160))
		
		

	pygame.display.update()
