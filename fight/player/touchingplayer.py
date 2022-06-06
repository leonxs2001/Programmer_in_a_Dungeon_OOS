import pygame
from fight.player.player import Player
from overworld.config import asset


class TouchingPlayer(Player):
    def __init__(self, initial_sequence_string: str, sequence_string: str, is_opponent: bool, damage=10):
        super().__init__(initial_sequence_string, sequence_string, is_opponent, damage)
        self.hit_delay = 1000  # min delay between the single hits in ms
        self.elapsed_time = self.hit_delay + 1

    def load_image(self, is_opponent, damage):
        if is_opponent:
            if damage == 10:
                return pygame.image.load(asset["melee_e"])
            else:
                return pygame.image.load(asset["big_melee_e"])
        else:
            return super().load_image(is_opponent, damage)

    def update(self, elapsed_time):
        if self.elapsed_time <= self.hit_delay:
            self.elapsed_time += elapsed_time
        super().update(elapsed_time)

    def process_collision(self, elapsed_time):
        super().process_collision(elapsed_time)
        if self.elapsed_time > self.hit_delay:
            self.opponent_player.life_controller.lifes -= self.damage
            self.elapsed_time = 0

    def get_max_time_to_attack(self):
        return self.hit_delay
