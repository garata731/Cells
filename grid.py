class Grid:
    def __init__(self, cell_size, map_width, map_height):
        self.cell_size = cell_size
        self.map_width = map_width
        self.map_height = map_height
        self.grid = {}

    def add_cell(self, cell):
        key = (cell.x // self.cell_size, cell.y // self.cell_size)
        if key not in self.grid:
            self.grid[key] = []
        self.grid[key].append(cell)

    def get_nearby_cells(self, cell):
        key = (cell.x // self.cell_size, cell.y // self.cell_size)
        nearby_cells = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor_key = (key[0] + dx, key[1] + dy)
                nearby_cells.extend(self.grid.get(neighbor_key, []))
        return nearby_cells

