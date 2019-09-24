import pygame

pygame.init()

screen = pygame.display.set_mode((20, 20))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		print event


