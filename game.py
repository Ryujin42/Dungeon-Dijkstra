import pygame
from constants import *
from dungeon import Dungeon


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.clock = pygame.time.Clock()

        self.dungeon = Dungeon()
        self.grid, self.corridors = self.dungeon.generate(DUNGEON_X, DUNGEON_Y, NUM_ROOMS, MAX_WEIGTH)     

        self.start = ()
        self.end = ()
        self.pathfind = []
        
        self.run = True


    def draw_dungeon(self):
        # background:
        pygame.draw.rect(
            self.screen,
            (100, 100, 100),
            pygame.Rect(0, 0, WINDOW_SIZE, WINDOW_SIZE)
        )

        # rooms
        for y in range(DUNGEON_Y):
            for x in range(DUNGEON_X):
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
                            ROOM_SIZE * (x*2 + .5),
                            ROOM_SIZE * (y*2 + .5),
                            ROOM_SIZE,
                            ROOM_SIZE
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
                        ROOM_SIZE * (corridor[0][0]*2 + 1.5),
                        ROOM_SIZE * (corridor[0][1]*2 + .5) + ROOM_SIZE // 3,
                        ROOM_SIZE,
                        ROOM_SIZE // 3
                    )
                )

            else: # vertical corridor
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        ROOM_SIZE * (corridor[0][0]*2 + .5) + ROOM_SIZE //3,
                        ROOM_SIZE * (corridor[0][1]*2 + 1.5),
                        ROOM_SIZE // 3,
                        ROOM_SIZE
                    )
                )


    def loop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start = ()
                        self.end = ()
                        self.grid, self.corridors = self.dungeon.generate(DUNGEON_X, DUNGEON_Y, NUM_ROOMS, MAX_WEIGTH)
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
                    mouse_pos = event.pos
                    if ROOM_SIZE//2 <= mouse_pos[0] < WINDOW_SIZE - ROOM_SIZE//2:
                        coords = mouse_pos[1] // (ROOM_SIZE*2), mouse_pos[0] // (ROOM_SIZE*2)
                        if self.grid[coords[0]][coords[1]]:
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

            pygame.display.update()
            self.clock.tick(60)

