import json

def generate_diagram(rows, cols):
    """Generates the JSON for a Wokwi NeoPixel matrix."""
    parts = []
    connections = []

    start_top = -230.2
    start_left = -158.1
    top_offset = 28.8
    left_offset = 28.8

    # Add the microcontroller
    parts.append({
        "type": "wokwi-arduino-nano",
        "id": "nano",
        "top": -350.4,
        "left": -67.7,
        "attrs": {}
    })

    # Generate parts (LEDs)
    for col in range(cols):
        left = start_left + col * left_offset
        for row in range(rows):
            led_num = col * rows + row + 1

            # Serpentine layout
            if col % 2 == 0:
                # Even columns, top to bottom
                top = start_top + row * top_offset
                rotate = 270
            else:
                # Odd columns, bottom to top
                top = start_top + (rows - 1 - row) * top_offset
                rotate = 90

            parts.append({
                "type": "wokwi-neopixel",
                "id": f"rgb{led_num}",
                "top": top,
                "left": left,
                "rotate": rotate,
                "attrs": {}
            })

    # Generate connections
    # Connection from nano to the first pixel
    connections.append([ "rgb1:DIN", "nano:6", "green", [ "v-152.8", "h163.2" ] ])

    # Connections between pixels
    for i in range(1, rows * cols):
        connections.append([f"rgb{i}:DOUT", f"rgb{i+1}:DIN", "green", ["v0"]])

    diagram = {
        "version": 1,
        "author": "Jules",
        "editor": "wokwi",
        "parts": parts,
        "connections": connections,
        "dependencies": {},
        ".wokwi": {
            "firmware": "../winter/code.py",
            "files": [
                "winter/code.py"
            ]
        }
    }

    return json.dumps(diagram, indent=2)

if __name__ == "__main__":
    generated_json = generate_diagram(16, 64)
    # The plan is to run this and redirect the output, but for now, just print.
    print(generated_json)
