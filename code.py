import board
import neopixel
import time
import random
import math

# Display dimensions
WIDTH = 64
HEIGHT = 16

# --- Colors ---
BACKGROUND = (0, 0, 0)
SNOW = (255, 255, 255)
TREE = (0, 100, 0)
LAKE = (0, 0, 139)
SKATER_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
SUN = (255, 255, 0)

# Create a NeoPixel object
pixels = neopixel.NeoPixel(board.D18, WIDTH * HEIGHT, auto_write=False)

# --- Drawing functions ---
def set_pixel(x, y, color):
    """Sets a pixel in the 2D grid."""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        pixels[y * WIDTH + x] = color

def draw_background(sky_color):
    """Draws the static background."""
    # Sky
    for y in range(HEIGHT):
        for x in range(WIDTH):
            set_pixel(x, y, sky_color)

    # Snowy ground
    for y in range(12, HEIGHT):
        for x in range(WIDTH):
            set_pixel(x, y, SNOW)

    # Forest
    for i in range(10):
        draw_tree(i * 6, 11)

    # Frozen lake
    for y in range(13, HEIGHT):
        for x in range(20, 44):
            set_pixel(x, y, LAKE)

def draw_tree(x, y):
    """Draws a simple pine tree."""
    set_pixel(x, y, TREE)
    set_pixel(x, y - 1, TREE)
    set_pixel(x, y - 2, TREE)
    set_pixel(x - 1, y - 1, TREE)
    set_pixel(x + 1, y - 1, TREE)

# --- Animation Classes ---
class Skater:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color

    def update(self):
        self.x = (self.x + self.speed)
        if self.x > 42:
            self.x = 22

    def draw(self):
        set_pixel(int(self.x), int(self.y), self.color)

class Snowflake:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self, wind):
        self.y += self.speed
        self.x += wind
        if self.y > HEIGHT:
            self.y = 0
            self.x = int(random.uniform(0, WIDTH))
        if self.x >= WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH - 1

    def draw(self):
        set_pixel(int(self.x), int(self.y), SNOW)

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

    def get_sky_color(self):
        y = abs(math.sin(self.angle))
        r = int(135 * y)
        g = int(206 * y)
        b = int(235 * y)
        return (r, g, b)

    def draw(self):
        x, y = self.get_position()
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            set_pixel(x, y, SUN)

# --- Animation setup ---
skaters = [
    Skater(22, 14, 0.2, SKATER_COLORS[0]),
    Skater(30, 15, -0.3, SKATER_COLORS[1]),
    Skater(25, 13, 0.4, SKATER_COLORS[2]),
    Skater(35, 14, -0.25, SKATER_COLORS[3]),
    Skater(28, 15, 0.35, SKATER_COLORS[4]),
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
    sky_color = sun.get_sky_color()
    draw_background(sky_color)
    for skater in skaters:
        skater.draw()
    for snowflake in snowflakes:
        snowflake.draw()
    sun.draw()

# Main loop
while True:
    update_animation()
    draw_scene()
    pixels.show()
    time.sleep(0.01)
