import pygame


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20 - 7
        self.color = (253, 150, 15)  # Red color for food

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x + 3, self.y + 3, self.size, self.size))

    def is_eaten(self, cell):
        return cell.x == self.x and cell.y == self.y
