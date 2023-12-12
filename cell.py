import pygame
import random
from itertools import cycle


class RangeDictionary(dict):
    def __getitem__(self, key):
        for r in self.keys():
            if key in r:
                return super().__getitem__(r)
        return super().__getitem__(key)


dict_rules = {
    range(1, 5 + 1): 'pass',
    range(6, 9 + 1): 'forward',
    range(10, 13 + 1): 't_right',
    range(13, 15 + 1): 't_left',
    range(14, 19 + 1): 'pass',
    range(20, 23 + 1): 'jump',
    range(24, 25 + 1): 'back'
}

r_dict = RangeDictionary(dict_rules)


def gen_analyze(_dict, sample_gen):
    actions = []
    for i in range(len(sample_gen)):
        actions.append(r_dict[sample_gen[i]])
    return actions


class Cell:
    # (0, 153, 0)
    def __init__(self, x, y):
        self.reproduction_threshold = {'steps': 17, 'energy': 85}
        self.x = x
        self.y = y
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.genome = self.gen_generation()
        self.genome_iterator = iter(self.genome)
        self.initial_energy = 100
        self.energy = self.initial_energy
        self.initial_color = (0, 153, 0)
        self.color = self.initial_color
        self.size = 20 - 1.5
        self.current_step = 0

    def draw(self, surface):
        dot_coord = (0, 0)
        cell_size = self.size
        pygame.draw.rect(surface, self.color, (self.x, self.y, cell_size, cell_size))
        if self.direction == 'up':
            dot_coord = (self.x + cell_size // 2, self.y + 5)
        elif self.direction == 'down':
            dot_coord = (self.x + cell_size // 2, self.y + cell_size - 5)
        elif self.direction == 'left':
            dot_coord = (self.x + 5, self.y + cell_size // 2)
        elif self.direction == 'right':
            dot_coord = (self.x + cell_size - 5, self.y + cell_size // 2)

        pygame.draw.circle(surface, (0, 0, 0), dot_coord, 2)

    def move_forward(self, distance):
        if self.direction == 'up':
            self.y -= distance
        elif self.direction == 'down':
            self.y += distance
        elif self.direction == 'left':
            self.x -= distance
        elif self.direction == 'right':
            self.x += distance

        self.current_step += 1

    def move_backward(self, distance):
        if self.direction == 'up':
            self.y += distance
        elif self.direction == 'down':
            self.y -= distance
        elif self.direction == 'left':
            self.x += distance
        elif self.direction == 'right':
            self.x -= distance

        self.current_step += 1

    def turn_right(self):
        directions = ['up', 'right', 'down', 'left']
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % 4]

        self.current_step += 1

    def turn_left(self):
        directions = ['up', 'right', 'down', 'left']
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index - 1) % 4]

        self.current_step += 1

    @staticmethod
    def gen_generation():
        gen = [random.choice(['pass', 'forward', 't_right', 't_left', 'jump', 'back']) for _ in range(26)]
        return cycle(gen)

    def is_inside_map(self, map_width, map_height):
        return 0 <= self.x < map_width and 0 <= self.y < map_height

    def collides_with(self, other_cell):
        return self.x == other_cell.x and self.y == other_cell.y

    def reproduce(self, cells, genome_iterators):
        if self.current_step >= self.reproduction_threshold['steps'] and self.energy >= self.reproduction_threshold['energy']:
            for _ in range(10):  # Attempt to create a copy within 10 cells around
                new_x = self.x + random.randint(-10, 10) * 20
                new_y = self.y + random.randint(-10, 10) * 20

                # Create a new cell at the calculated position
                new_cell = Cell(new_x, new_y)

                # Check if the new position is inside the map and there are no collisions with other cells
                if new_cell.is_inside_map(1600, 900) and not any(
                        new_cell.collides_with(other_cell) for other_cell in cells):
                    self.energy -= 27  # Deduct energy for reproduction
                    cells.append(new_cell)
                    genome_iterators.append(iter(new_cell.genome))  # Add the new genome iterator
                    break
