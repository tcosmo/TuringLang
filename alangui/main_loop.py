import alang
import pygame


def run():
    pygame.init()

    screen = pygame.display.set_mode([1200, 800])
    pygame.display.set_caption("alangui")

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Flip the display
        pygame.display.flip()

    pygame.quit()
