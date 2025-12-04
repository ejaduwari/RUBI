import subprocess
import json
import random
import kociemba

# ------------------------------
# GLOBAL STORAGE
# ------------------------------
# Holds scanned faces: RGB + classified colors
# Example: {"U": {"rgb": [...], "colors": [...]}, ...}
angle_data = {}

# Hardcoded centers for each face
centers = {
    'U': 'Y',  # Up = Yellow
    'R': 'O',  # Right = Orange
    'F': 'G',  # Front = Green
    'D': 'W',  # Down = White
    'L': 'R',  # Left = Red
    'B': 'B'   # Back = Blue
}

# ------------------------------
# FUNCTION: Classify RGB to Cube Color
# ------------------------------
def classify_color(r, g, b):
    """
    Classify an RGB value into a Rubik's cube sticker color:
    W - White, Y - Yellow, R - Red, O - Orange, G - Green, B - Blue
    """
    # Red vs Orange
    if r > 200 and g < 150 and b < 150:
        gb_delta = g - b
        return 'O' if gb_delta > 10 else 'R'

    # White vs Yellow
    if r >= 175 and g >= 175:
        gb_delta = g - b
        return 'Y' if b < 100 and gb_delta > 60 else 'W'

    # Green vs Blue
    if r < 200:
        gb_delta = g - b
        if gb_delta > 0:
            return 'G'
        elif gb_delta < 0:
            return 'B'
        else:
            return 'G' if g >= b else 'B'

    # Catch-all
    return '?'

# ------------------------------
# FUNCTION: Call C++ Executable
# ------------------------------
def get_rgb_from_cpp(angle):
    """
    Calls the C++ RGB program for a given angle.
    Returns a list of 8 or 24 RGB dicts depending on angle.
    """
    try:
        result = subprocess.run(
            ['sudo', './getrgb', angle],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.strip().splitlines()
        json_line = lines[-1]
        return json.loads(json_line)

    except subprocess.CalledProcessError as e:
        print("Error running getrgb:", e)
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
        return None
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        print("Raw output:", result.stdout)
        return None

# ------------------------------
# FUNCTION: Save Faces From Angle1
# ------------------------------
def save_angle1(rgb_list_24):
    """
    angle1 captures 3 faces: U, L, F
    Splits 24 RGB values into three faces of 8 tiles each
    """
    faces = ["U", "L", "F"]
    for i, face in enumerate(faces):
        tiles_8 = rgb_list_24[i*8 : (i+1)*8]
        colors = [classify_color(t['r'], t['g'], t['b']) for t in tiles_8]
        angle_data[face] = {"rgb": tiles_8, "colors": colors}
        print(f"Saved face {face} with colors:", colors)

# ------------------------------
# FUNCTION: Save Faces From Angle2
# ------------------------------
def save_angle2(rgb_list_24):
    """
    angle2 captures 3 faces: D, R, B
    Splits 24 RGB values into three faces of 8 tiles each
    """
    faces = ["D", "R", "B"]
    for i, face in enumerate(faces):
        tiles_8 = rgb_list_24[i*8 : (i+1)*8]
        colors = [classify_color(t['r'], t['g'], t['b']) for t in tiles_8]
        angle_data[face] = {"rgb": tiles_8, "colors": colors}
        print(f"Saved face {face} with colors:", colors)

# ------------------------------
# FUNCTION: Build Face String
# ------------------------------
def build_face_string(face_letter, tiles_8):
    """
    Inserts hardcoded center in the middle of 8-tile list to create 9-tile face string.
    """
    center = centers[face_letter]
    face_string = tiles_8[:4] + [center] + tiles_8[4:]
    return "".join(face_string)

# ------------------------------
# FUNCTION: Assemble Kociemba String
# ------------------------------
def assemble_kociemba_string():
    """
    Combines all 6 faces into the 54-character Kociemba string.
    Order: U R F D L B
    """
    kociemba_str = ""
    for face in ['U','R','F','D','L','B']:
        if face not in angle_data:
            print(f"Warning: Face {face} not scanned")
            continue
        tiles_8 = angle_data[face]["colors"]
        face_str = build_face_string(face, tiles_8)
        kociemba_str += face_str
    return kociemba_str

# ------------------------------
# FUNCTION: Solver Placeholder
# ------------------------------
def run_solver(color_string):
    """
    Solves the cube using the Kociemba algorithm.
    Accepts a color-letter string (W,R,Y,O,B,G) and maps it to face letters.
    Returns a list of moves.
    """
    # Define color → face mapping
    color_to_face = {
        "W": "D",  # White → Down
        "R": "L",  # Red → Left
        "Y": "U",  # Yellow → Up
        "O": "R",  # Orange → Right
        "B": "B",  # Blue → Back
        "G": "F"   # Green → Front
    }

    # Map the color string to face letters
    face_string = "".join(color_to_face.get(c, c) for c in color_string)

    try:
        # Solve cube using the mapped face string
        solution = kociemba.solve(face_string)
        moves = solution.split()  # Convert string to list

        # Print debug info
        print("Original color string: ", color_string)
        print("Mapped face string:    ", face_string)
        print("Solver moves:          ", moves)

        return moves
    except Exception as e:
        print("Error solving cube:", e)
        return []

# ------------------------------
# FUNCTION: Send Moves to ESP32
# ------------------------------
def send_to_esp32(moves_list, port="/dev/serial0", baudrate=115200):
    import serial
    import time

    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # allow ESP32 to initialize

        moves_str = " ".join(moves_list) + "\n"
        ser.write(moves_str.encode('utf-8'))
        print(f"Sent to ESP32: {moves_str.strip()}")

        ser.close()

    except serial.SerialException as e:
        print("Error opening/writing to serial port:", e)
# ------------------------------
# FUNCTION: Scramble Cube
# ------------------------------
def scramble_cube(num_moves=20):
    """
    Generates a random scramble sequence and sends to ESP32.
    """
    moves_options = ["R", "R'", "R2", "L", "L'", "L2",
                     "U", "U'", "U2", "D", "D'", "D2",
                     "F", "F'", "F2", "B", "B'", "B2"]
    scramble = [random.choice(moves_options) for _ in range(num_moves)]
    print("Scramble sequence:", scramble)
    send_to_esp32(scramble)

# ------------------------------
# MAIN BLOCK
# ------------------------------
if __name__ == "__main__":
    print("==== RUBI RGB CLASSIFIER ====")

    # Scan angle1 → U, L, F
    rgb_angle1 = get_rgb_from_cpp("angle1")
    if rgb_angle1:
        save_angle1(rgb_angle1)

    # Scan angle2 → D, R, B
    rgb_angle2 = get_rgb_from_cpp("angle2")
    if rgb_angle2:
        save_angle2(rgb_angle2)

    # Assemble full 54-character string
    k_str = assemble_kociemba_string()
    moves = run_solver(k_str)
    send_to_esp32(moves)

    # Optionally scramble
    scramble_input = input("\nDo you want to scramble the cube? (y/n): ").strip().lower()
    if scramble_input == 'y':
        scramble_cube()
