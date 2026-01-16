import time
import random
import math
import os

# Display dimensions
WIDTH = 64
HEIGHT = 16

# --- ASCII Characters ---
BACKGROUND_CHAR = ' '
SNOW_CHAR = '*'
TREE_CHAR = 'T'
LAKE_CHAR = '~'
SKATER_CHAR = 'S'
SUN_CHAR = 'O'

# Create a 2D grid for the display
grid = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

# --- Drawing functions ---
def set_pixel(x, y, char):
    """Sets a character in the 2D grid."""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        grid[y][x] = char

def draw_background():
    """Draws the static background."""
    # Sky
    for y in range(HEIGHT):
        for x in range(WIDTH):
            set_pixel(x, y, BACKGROUND_CHAR)

    # Snowy ground
    for y in range(12, HEIGHT):
        for x in range(WIDTH):
            set_pixel(x, y, SNOW_CHAR)

    # Forest
    for i in range(10):
        draw_tree(i * 6, 11)

    # Frozen lake
    for y in range(13, HEIGHT):
        for x in range(20, 44):
            set_pixel(x, y, LAKE_CHAR)

def draw_tree(x, y):
    """Draws a simple pine tree."""
    set_pixel(x, y, TREE_CHAR)
    set_pixel(x, y - 1, TREE_CHAR)
    set_pixel(x, y - 2, TREE_CHAR)
    set_pixel(x - 1, y - 1, TREE_CHAR)
    set_pixel(x + 1, y - 1, TREE_CHAR)

# --- Animation Classes ---
class Skater:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.x = (self.x + self.speed)
        if self.x > 42:
            self.x = 22
        elif self.x < 22:
            self.x = 42

    def draw(self):
        set_pixel(int(self.x), int(self.y), SKATER_CHAR)

class Snowflake:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self, wind):
        self.y += self.speed
        self.x += wind
        if self.y >= HEIGHT:
            self.y = 0
            self.x = int(random.uniform(0, WIDTH))
        if self.x >= WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH - 1

    def draw(self):
        set_pixel(int(self.x), int(self.y), SNOW_CHAR)

class Sun:
    def __init__(self):
        self.angle = 0
        self.speed = 0.01

    def update(self):
        self.angle = (self.angle + self.speed) % (2 * math.pi)

    def get_position(self):
        x = int((WIDTH / 2) + (WIDTH / 2 - 1) * math.cos(self.angle))
        y = int((HEIGHT) - (HEIGHT - 1) * abs(math.sin(self.angle)))
        return x, y

    def draw(self):
        x, y = self.get_position()
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            set_pixel(x, y, SUN_CHAR)

# --- Animation setup ---
skaters = [
    Skater(22, 14, 0.2),
    Skater(30, 15, -0.3),
    Skater(25, 13, 0.4),
    Skater(35, 14, -0.25),
    Skater(28, 15, 0.35),
]
snowflakes = [Snowflake(random.uniform(0, WIDTH), 0, random.uniform(0.1, 0.5)) for _ in range(50)]
sun = Sun()
wind = 0
last_wind_change = time.time()

def update_animation():
    """Updates the positions of animated elements."""
    global wind, last_wind_change
    if time.time() - last_wind_change > 5:
        wind = random.uniform(-0.2, 0.2)
        last_wind_change = time.time()

    for skater in skaters:
        skater.update()
    for snowflake in snowflakes:
        snowflake.update(wind)
    sun.update()

def draw_scene():
    """Draws all elements of the scene."""
    draw_background()
    for skater in skaters:
        skater.draw()
    for snowflake in snowflakes:
        snowflake.draw()
    sun.draw()

def print_grid():
    """Prints the grid to the console."""
    os.system('clear' if os.name == 'posix' else 'cls')
    for row in grid:
        print("".join(row))

# Main loop
for _ in range(500): # Run for 500 frames
    update_animation()
    draw_scene()
    print_grid()
    time.sleep(0.01)
