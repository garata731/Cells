import pygame.display
from cell import *
from itertools import cycle, islice
from food import Food


def formula(cell):
    cell.color = (int(0 + (100 - (cell.energy / cell.initial_energy * 100))),
                  int(153 - (100 - (cell.energy / cell.initial_energy * 100))), 0)


def cellMovementAnalyzer(cells_, genome_iterators_, cell_movement_enabled_, foods_):
    cells_to_remove = []

    for food in foods:
        for cell in cells:
            if food.is_eaten(cell):
                cell.energy += 80
                foods.remove(food)
                break

    if cell_movement_enabled_:

        for cell, genome_iterator in zip(cells_, genome_iterators_):
            # Get the next action from the genome iterator
            action = next(genome_iterator)

            cell.reproduce(cells_, genome_iterators_)


            # Check if cell movement is enabled
            if 0 < cell.energy <= cell.initial_energy:
                # Print the current action and cell coordinates (commented out)
                # Perform actions based on the current action
                if action == 'pass':
                    cell.energy += 0.5
                    # If the action is 'pass', do nothing
                    pass
                elif action == 'forward':

                    # If the action is 'forward', calculate new position and move the cell forward
                    new_x, new_y = cell.x, cell.y
                    if cell.direction == 'up':
                        new_y -= CELL_SIZE
                    elif cell.direction == 'down':
                        new_y += CELL_SIZE
                    elif cell.direction == 'left':
                        new_x -= CELL_SIZE
                    elif cell.direction == 'right':
                        new_x += CELL_SIZE

                    # Create a new cell at the calculated position
                    new_cell_ = Cell(new_x, new_y)

                    # Check if the new position is inside the map and there are no collisions with other cells
                    if new_cell_.is_inside_map(MAP_WIDTH, MAP_HEIGHT) and not any(
                            new_cell_.collides_with(other_cell) for other_cell in cells_):
                        formula(cell)
                        # Move the cell forward by the specified cell size
                        cell.move_forward(CELL_SIZE)
                        cell.energy -= 1
                    else:
                        cell.energy += 0.5

                elif action == 't_right':
                    cell.energy -= 0.5
                    formula(cell)
                    cell.turn_right()
                # If the action is "t_right", turn the cell to the right
                elif action == 't_left':
                    cell.energy -= 0.5
                    formula(cell)
                    # If the action is "t_left", turn the cell to the left
                    cell.turn_left()

                elif action == 'jump':
                    # If the action is 'jump', calculate new position and move the cell forward by double the cell size
                    new_x, new_y = cell.x, cell.y
                    if cell.direction == 'up':
                        new_y -= CELL_SIZE * 2
                    elif cell.direction == 'down':
                        new_y += CELL_SIZE * 2
                    elif cell.direction == 'left':
                        new_x -= CELL_SIZE * 2
                    elif cell.direction == 'right':
                        new_x += CELL_SIZE * 2

                    # Create a new cell at the calculated position
                    new_cell_ = Cell(new_x, new_y)

                    # Check if the new position is inside the map and there are no collisions with other cells
                    if new_cell_.is_inside_map(MAP_WIDTH, MAP_HEIGHT) and not any(
                            new_cell_.collides_with(other_cell) for other_cell in cells_):
                        formula(cell)
                        # Move the cell forward by double the cell size
                        cell.move_forward(CELL_SIZE * 2)
                        cell.energy -= 3
                    else:
                        cell.energy += 0.5

                elif action == 'back':

                    # If the action is 'back', calculate new position and move the cell backward
                    new_x, new_y = cell.x, cell.y
                    if cell.direction == 'up':
                        new_y += CELL_SIZE
                    elif cell.direction == 'down':
                        new_y -= CELL_SIZE
                    elif cell.direction == 'left':
                        new_x += CELL_SIZE
                    elif cell.direction == 'right':
                        new_x -= CELL_SIZE

                    # Create a new cell at the calculated position
                    new_cell_ = Cell(new_x, new_y)

                    # Check if the new position is inside the map and there are no collisions with other cells
                    if new_cell_.is_inside_map(MAP_WIDTH, MAP_HEIGHT) and not any(
                            new_cell_.collides_with(other_cell) for other_cell in cells_):
                        formula(cell)
                        # Move the cell backward by the specified cell size
                        cell.move_backward(CELL_SIZE)
                        cell.energy -= 2
                    else:
                        cell.energy += 0.5
            elif cell.energy > cell.initial_energy:
                cell.energy = cell.initial_energy
            else:
                cells_to_remove.append(cell)
                del cell

    for cell_to_remove in cells_to_remove:
        cells_.remove(cell_to_remove)


pygame.init()

MAP_WIDTH = 1600
MAP_HEIGHT = 900
SIDE_PANEL_WIDTH = 200
CELL_SIZE = 20
NUM_CELLS = 69
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (200, 200, 200)
#MAX_FOOD_PERCENTAGE = 10
#max_allowed_food = int(NUM_CELLS * MAX_FOOD_PERCENTAGE)

max_allowed_food = 750

# Screen initialization
screen_width = MAP_WIDTH + SIDE_PANEL_WIDTH
screen = pygame.display.set_mode((screen_width, MAP_HEIGHT))
pygame.display.set_caption('Cell Map')

# Surfaces
map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
side_panel_surface = pygame.Surface((SIDE_PANEL_WIDTH, MAP_HEIGHT))
side_panel_surface.fill(BACKGROUND_COLOR)


# Function to draw grid lines
def draw_grid(surface, width_, height, cell_size, line_color):
    for xx in range(0, width_, cell_size):
        pygame.draw.line(surface, line_color, (xx, 0), (xx, height), 1)
    for yy in range(0, height, cell_size):
        pygame.draw.line(surface, line_color, (0, yy), (width_, yy), 1)


# Draw grid lines on the map surface
draw_grid(map_surface, MAP_WIDTH, MAP_HEIGHT, CELL_SIZE, LINE_COLOR)

foods = []
cells = []
genomes = []

for _ in range(NUM_CELLS):
    while True:
        new_cell = Cell(random.randrange(0, MAP_WIDTH, CELL_SIZE),
                        random.randrange(0, MAP_HEIGHT, CELL_SIZE))

        # Check for collisions with existing cells
        if not any(new_cell.collides_with(other_cell) for other_cell in cells):
            cells.append(new_cell)
            genomes.append(new_cell.genome)
            break

genome_iterators = [cycle(genome) for genome in genomes]

running = True
clock = pygame.time.Clock()

font = pygame.font.Font(None, 14)

increase_button = pygame.Rect(50, 100, 100, 50)
decrease_button = pygame.Rect(50, 160, 100, 50)
stop_button = pygame.Rect(50, 220, 100, 50)
next_tick_button = pygame.Rect(50, 280, 100, 50)
regenerate_button = pygame.Rect(50, 340, 100, 50)
clear_map_button = pygame.Rect(50, 400, 100, 50)
input_rect = pygame.Rect(50, 30, 80, 50)
num_cell_input_rect = (50, 40, 80, 50)

input_color_inactive = pygame.Color('lightskyblue3')
input_color_active = pygame.Color('dodgerblue2')
input_font = pygame.font.Font(None, 32)
input_active = False
input_text = ''

selected_cell = None
info_rect = pygame.Rect(20, 450, 160, 300)

max_food_spawn_attempts = 10
food_spawn_amount = 1
a = 30  # clock fps
i = 0
time_stop = True  # time stop condition
cell_movement_enabled = False  # cell_movement condition
selected_cell_index = None
food_enabled = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if increase_button.collidepoint(mouse_x - MAP_WIDTH, mouse_y) and a < 60:
                a += 1
                pygame.display.flip()
            elif decrease_button.collidepoint(mouse_x - MAP_WIDTH, mouse_y) and a > 1:
                a -= 1
                pygame.display.flip()
            elif stop_button.collidepoint(mouse_x - MAP_WIDTH, mouse_y):
                time_stop = not time_stop
                cell_movement_enabled = not time_stop
                pygame.display.flip()
            elif next_tick_button.collidepoint(mouse_x - MAP_WIDTH, mouse_y) and time_stop:
                cell_movement_enabled = True
                cellMovementAnalyzer(cells, genome_iterators, cell_movement_enabled, foods)

                # Check if it's time to create new food
                if random.random() < 0.1:  # Adjust the probability as needed
                    while True:
                        new_food = Food(random.randrange(0, MAP_WIDTH, CELL_SIZE),
                                        random.randrange(0, MAP_HEIGHT, CELL_SIZE))

                        # Check for collisions with existing cells and other food
                        if not any(new_food.is_eaten(cell) for cell in cells) and not any(
                                new_food.is_eaten(existing_food) for existing_food in foods):
                            foods.append(new_food)
                            break

                pygame.display.flip()
                cell_movement_enabled = False
            elif regenerate_button.collidepoint(mouse_x - MAP_WIDTH, mouse_y):
                selected_cell = None
                cells.clear()
                genomes.clear()
                genome_iterators.clear()
                foods.clear()
                food_enabled = True
                for _ in range(NUM_CELLS):
                    while True:
                        new_cell = Cell(random.randrange(0, MAP_WIDTH, CELL_SIZE),
                                        random.randrange(0, MAP_HEIGHT, CELL_SIZE))

                        # Check for collisions with existing cells
                        if not any(new_cell.collides_with(other_cell) for other_cell in cells):
                            cells.append(new_cell)
                            genomes.append(new_cell.genome)
                            break
                genome_iterators = [cycle(genome) for genome in genomes]
            elif clear_map_button.collidepoint(mouse_x - MAP_WIDTH, mouse_y):
                cells.clear()
                genomes.clear()
                genome_iterators.clear()
                foods.clear()  # Clear the foods list
                selected_cell = None
                food_enabled = False
            elif input_rect.collidepoint(event.pos):
                input_active = not input_active
            else:
                input_active = False

            cell_rectangles = [pygame.Rect(cell.x, cell.y, CELL_SIZE, CELL_SIZE) for cell in cells]

            for cell, cell_rect in zip(cells, cell_rectangles):
                if cell_rect.collidepoint(mouse_x, mouse_y):
                    selected_cell = cell
                    selected_cell_genome = cell.genome  # Update selected_cell_genome with the current cell's genome
                    break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Handle the entered number (convert input_text to int, etc.)
                try:
                    a = int(input_text)
                    input_text = ''
                except ValueError:
                    # Handle the case when the input is not a valid number
                    print("Invalid input. Please enter a number.")
            elif event.key == pygame.K_RETURN:
                try:
                    NUM_CELLS = int(input_text)
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    cellMovementAnalyzer(cells, genome_iterators, cell_movement_enabled, foods)

    map_surface.fill((150, 150, 150))

    for x in range(0, MAP_WIDTH, CELL_SIZE):
        pygame.draw.line(map_surface, LINE_COLOR, (x, 0), (x, MAP_HEIGHT), 1)

    for y in range(0, MAP_HEIGHT, CELL_SIZE):
        pygame.draw.line(map_surface, LINE_COLOR, (0, y), (MAP_WIDTH, y), 1)

    for cell in cells:
        cell.draw(map_surface)
        if selected_cell is not None and cell == selected_cell:
            pygame.draw.rect(map_surface, (255, 0, 0), (cell.x, cell.y, CELL_SIZE, CELL_SIZE), 2)

    for food in foods:
        for cell in cells:
            if food.is_eaten(cell):
                cell.energy += 10
                foods.remove(food)

    for food in foods:
        food.draw(map_surface)

    for _ in range(max_food_spawn_attempts):
        if random.random() < 2 and not time_stop and food_enabled and len(foods) < max_allowed_food:
            for _ in range(food_spawn_amount):
                new_food = Food(random.randrange(0, MAP_WIDTH, CELL_SIZE),
                                random.randrange(0, MAP_HEIGHT, CELL_SIZE))

                # Check for collisions with existing cells and other food
                if not any(new_food.is_eaten(cell) for cell in cells) and not any(
                        new_food.is_eaten(existing_food) for existing_food in foods):
                    foods.append(new_food)

    side_panel_surface.fill((180, 180, 180))

    pygame.draw.rect(side_panel_surface, (255, 0, 0), increase_button)
    pygame.draw.rect(side_panel_surface, (0, 255, 0), decrease_button)
    pygame.draw.rect(side_panel_surface, (0, 0, 255), stop_button)
    pygame.draw.rect(side_panel_surface, (100, 255, 100), next_tick_button)
    pygame.draw.rect(side_panel_surface, (255, 100, 100), regenerate_button)
    pygame.draw.rect(side_panel_surface, (100, 100, 255), clear_map_button)

    color = input_color_active if input_active else input_color_inactive
    pygame.draw.rect(side_panel_surface, color, input_rect, 2)
    text_surface = input_font.render(input_text, True, (0, 0, 0))
    width = max(200, text_surface.get_width() + 10)
    input_rect.w = width
    side_panel_surface.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    pygame.draw.rect(side_panel_surface, (0, 0, 0), input_rect, 2)

    text = font.render(f"Clock Tick: {a}", True, (0, 0, 0))
    side_panel_surface.blit(text, (10, 10))

    pygame.draw.rect(side_panel_surface, (190, 190, 190), info_rect)

    # Display information about the selected cell
    if selected_cell is not None:
        text = font.render(f"Selected Cell: ({selected_cell.x}, {selected_cell.y}):", True, (0, 0, 0))
        text_energy = font.render(f"Energy: {selected_cell.energy}", True, (0, 0, 0))
        side_panel_surface.blit(text, (30, 460))
        side_panel_surface.blit(text_energy, (30, 740))

        for i, info in enumerate(list(islice(selected_cell.genome, 26))):
            if i > 25:
                break
            action = info  # Extract genome information from the tuple
            text_gen = font.render(str(action), True, (0, 0, 0))  # Convert action to string
            side_panel_surface.blit(text_gen, (30, 470 + i * 10))

    screen.blit(map_surface, (0, 0))
    screen.blit(side_panel_surface, (MAP_WIDTH, 0))
    pygame.display.flip()

    if len(cells) == 0:
        time_stop = True
        cell_movement_enabled = False

    if not time_stop:
        pygame.display.flip()
        clock.tick(a)

pygame.quit()
