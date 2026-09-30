import pygame

class Snake:
    def __init__(self, x, y, cell_size):
        self.cell_size = cell_size
        # body is a list of (x, y) grid-cell positions, head is body[0]
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = (1, 0)  # moving right
        self.next_direction = (1, 0)
        self.last_moved_direction = (1, 0)
        self.grow_pending = False

    def set_direction(self, dx, dy):
        # Prevent 180-degree reversal relative to the direction of the last completed move
        last_dx, last_dy = self.last_moved_direction
        if (dx == -last_dx and dy == -last_dy) or (dx == -self.direction[0] and dy == -self.direction[1]):
            return

        # Double-check against the neck segment if the body has multiple segments
        if len(self.body) > 1:
            head_x, head_y = self.body[0]
            if (head_x + dx, head_y + dy) == self.body[1]:
                return

        self.next_direction = (dx, dy)

    def move(self):
        self.direction = self.next_direction
        self.last_moved_direction = self.direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def head_rect(self):
        x, y = self.body[0]
        return pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def segment_rects(self):
        return [
            pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            for (x, y) in self.body
        ]

    def collides_with_self(self):
        head = self.body[0]
        return head in self.body[1:]

    def collides_with_wall(self, grid_width, grid_height):
        x, y = self.body[0]
        return x < 0 or y < 0 or x >= grid_width or y >= grid_height
