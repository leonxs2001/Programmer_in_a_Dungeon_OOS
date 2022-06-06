
from map import Map
from typing import List, Tuple
import pygame


class Outerwall(pygame.sprite.Sprite):
    def __init__(self, assets, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load(assets['outer_wall']), size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Wall(pygame.sprite.Sprite):
    def __init__(self, assets, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load(assets['wall']), size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Ground(pygame.sprite.Sprite):
    def __init__(self, assets, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load(assets['ground']), size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class End(pygame.sprite.Sprite):
    def __init__(self, assets, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load(assets['end']), size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class MapRenderer(pygame.sprite.Sprite, Map):

    def __init__(self, assets, maps: List):
        self.map_index = -1
        self.loc_maps = maps
        print()

        pygame.sprite.Sprite.__init__(self)
        self.done_map = self.get_map()
        self.uni_size = (40, 40)
        self.assets = assets
        self.render()

    def draw(self, screen: pygame.Surface):
        self.walls.draw(screen)
        self.ground.draw(screen)
        self.end.draw(screen)

    def get_map(self) -> List:
        self.map_index += 1
        map = Map(self.loc_maps[self.map_index])
        # parse the csv and check if input is valid
        # raise error if necessary
        err = map.parse_level_csv()
        if err is not None:
            raise err
        err = map.check_level()
        if err is not None:
            raise err
        render_map = map.preProcessLevel()

        return render_map

    def checkend(self, group):
        return pygame.sprite.groupcollide(self.end, group, False, False)

    def render(self):
        self.walls = pygame.sprite.Group()
        self.ground = pygame.sprite.Group()
        self.end = pygame.sprite.Group()
        for x in range(len(self.done_map)):
            for y in range(len(self.done_map[x])):
                if (self.done_map[x][y])[0] == 'outer_wall':
                    temp = Outerwall(self.assets, self.uni_size,
                                     ((self.done_map[x][y])[1]))
                    self.walls.add(temp)
                elif (self.done_map[x][y])[0] == 'wall':
                    temp = Wall(self.assets, self.uni_size,
                                ((self.done_map[x][y])[1]))
                    self.walls.add(temp)
                elif (self.done_map[x][y])[0] == 'ground':
                    temp = Ground(self.assets, self.uni_size,
                                  ((self.done_map[x][y])[1]))
                    self.ground.add(temp)
                elif (self.done_map[x][y])[0] == 'end':
                    temp = End(self.assets, self.uni_size,
                               ((self.done_map[x][y])[1]))
                    self.end.add(temp)
                else:
                    temp = Ground(self.assets, self.uni_size,
                                  ((self.done_map[x][y])[1]))
                    self.ground.add(temp)
