import pygame
from constants import *
from dungeon import Dungeon
from ui import Slider


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.clock = pygame.time.Clock()

        self.dungeon_size = DUNGEON_X
        self.num_rooms = NUM_ROOMS
        self.extra_vertexes = EXTRA_VERTEXES

        self.sliders = [
            Slider(HEIGHT + 20, 450, 400, 2, 50, self.dungeon_size, "Dungeon Size"),
            Slider(HEIGHT + 20, 500, 400, 2, 500, self.num_rooms, "Rooms"),
            Slider(HEIGHT + 20, 550, 400, 0.0, 1.0, self.extra_vertexes, "Extra vertexes", is_float=True)
        ]


        self.dungeon = Dungeon()
        self.grid, self.corridors = self.dungeon.generate(
            self.dungeon_size,
            self.num_rooms, 
            self.extra_vertexes
        )     
        self.room_size = HEIGHT // (max(DUNGEON_X, DUNGEON_Y)*2)

        self.start = ()
        self.end = ()
        self.pathfind = []
        
        self.run = True


    def draw_dungeon(self):
        # background:
        pygame.draw.rect(
            self.screen,
            (100, 100, 100),
            pygame.Rect(0, 0, WIDTH, HEIGHT)
        )

        if not self.grid:
            return

        # rooms
        for y in range(self.dungeon_size):
            for x in range(self.dungeon_size):
                if self.grid[y][x]:
                    if self.start == (y, x):
                        color = (0, 0, 255)
                    elif self.end == (y, x):
                        color = (255, 0, 0)
                    elif (y, x) in self.pathfind:
                        color = (0, 255, 0)
                    else:
                        color = (255, 255, 255)
                    pygame.draw.rect(
                        self.screen,
                        color,
                        pygame.Rect(
                            self.room_size * (x*2 + .5),
                            self.room_size * (y*2 + .5),
                            self.room_size,
                            self.room_size
                        )
                    )

        # corridors
        for corridor in self.corridors:
            # top-left first
            if sum(corridor[0]) > sum(corridor[1]):
                corridor = corridor[::-1]

            if corridor[0][::-1] in self.pathfind and corridor[1][::-1] in self.pathfind:
                color = (0, 255, 0)
            else:
                color = (255, 255, 255)

            if corridor[0][1] == corridor[1][1]: # horizontal corridor
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        self.room_size * (corridor[0][0]*2 + 1.5),
                        self.room_size * (corridor[0][1]*2 + .5) + self.room_size // 3,
                        self.room_size,
                        self.room_size // 3
                    )
                )

            else: # vertical corridor
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        self.room_size * (corridor[0][0]*2 + .5) + self.room_size // 3,
                        self.room_size * (corridor[0][1]*2 + 1.5),
                        self.room_size // 3,
                        self.room_size
                    )
                )


    def write_instructions(self):
        texts = [
                    "Instructions",
                    "",
                    "<SPACE> to generate a new dungeon",
                    "<R> to reset the dungeon",
                    "<LEFT-CLICK> to set the `Start` room",
                    "<RIGHT-CLICK> to set the `End` room"
                ]

        for i in range(len(texts)):
            text_surface = pygame.font.Font.render(self.font, texts[i], True, (255, 255, 255))
            self.screen.blit(text_surface, (HEIGHT, 50 * (i+1)))


    def loop(self):
        while self.run:
            for event in pygame.event.get():
                for slider in self.sliders:
                    slider.handle_event(event)

                if event.type == pygame.QUIT:
                    self.run = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.start = ()
                        self.end = ()
                    elif event.key == pygame.K_SPACE:
                        self.start = ()
                        self.end = ()
                        self.dungeon_size = self.sliders[0].val
                        self.rooms = self.sliders[1].val
                        self.extra = self.sliders[2].val
                        self.room_size = HEIGHT // (self.dungeon_size*2)
                        self.grid, self.corridors = self.dungeon.generate(
                            self.dungeon_size,
                            self.rooms,
                            self.extra
                        )
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
                    mouse_pos = event.pos
                    if (not self.room_size//2 <= mouse_pos[0] < HEIGHT - self.room_size//2) or \
                            (not self.room_size//2 <= mouse_pos[1] < HEIGHT - self.room_size//2):
                        continue

                    coords = mouse_pos[1] // (self.room_size*2), mouse_pos[0] // (self.room_size*2)
                    if not self.grid or not self.grid[coords[0]][coords[1]]:
                        continue

                    if event.button == 1: # left click
                        self.start = coords
                        if self.end == coords: self.end = ()

                    elif event.button == 3: # right click
                        self.end = coords
                        if self.start == coords: self.start = ()


            if self.start and self.end:
                self.dungeon.prepare_dungeon_graph()
                self.pathfind = self.dungeon.calculate(self.start, self.end)[1]
            else:
                self.pathfind = []
                
            self.draw_dungeon()
            self.write_instructions()

            for slider in self.sliders:
                slider.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)

