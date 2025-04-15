import pygame
from constants import WIDTH, HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    bg_image = pygame.image.load("./src/botw.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.blit(bg_image,(0, 0))

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()

