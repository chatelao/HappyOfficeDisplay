import board
import neopixel
import time

# Display dimensions
WIDTH = 64
HEIGHT = 16

# --- Colors ---
BACKGROUND = (0, 0, 0)
SNOW = (255, 255, 255)
TREE = (0, 100, 0)
LAKE = (0, 0, 139)
SKATER = (255, 0, 0)
SUN = (255, 255, 0)

# Create a NeoPixel object
pixels = neopixel.NeoPixel(board.D18, WIDTH * HEIGHT, auto_write=False)

# --- Drawing functions ---
def set_pixel(x, y, color):
    """Sets a pixel in the 2D grid."""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        pixels[y * WIDTH + x] = color

def draw_background():
    """Draws the static background."""
    # Sky
    for y in range(HEIGHT):
        for x in range(WIDTH):
            set_pixel(x, y, (135, 206, 235))  # Sky blue

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

# --- Animation state ---
skater_pos = [22, 14]
snowflakes = []

def update_animation():
    """Updates the positions of animated elements."""
    global skater_pos
    skater_pos[0] = (skater_pos[0] + 1) % 42
    # Add snow logic here
    # Add sun logic here
    # Add wind logic here

def draw_scene():
    """Draws all elements of the scene."""
    draw_background()
    # Draw skaters
    set_pixel(skater_pos[0], skater_pos[1], SKATER)
    # Draw snowflakes
    # Draw sun
    # Draw wind

# Main loop
while True:
    update_animation()
    draw_scene()
    pixels.show()
    time.sleep(0.1)
