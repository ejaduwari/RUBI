#!/usr/bin/env python3
import subprocess
import json

# ---- CONFIG ----
# Hardcoded centers (if needed later)
# Example: {'U': 'Y', 'R': 'O', 'F': 'G', ...}
centers = {
    'U': 'Y',  # Up = Yellow
    'R': 'O',  # Right = Orange
    'F': 'G',  # Front = Green
    'D': 'W',  # Down = White
    'L': 'R',  # Left = Red
    'B': 'B'   # Back = Blue
}

# RGB → sticker color classification
def classify_color(r, g, b):
    """
    Classify an RGB value into a Rubik's cube sticker color:
    W - White
    Y - Yellow
    R - Red
    O - Orange
    G - Green
    B - Blue
    """

    # ----- Red vs Orange -----
    # Both have high R, low G/B; orange has more green relative to blue
    if r > 200 and g < 150 and b < 150:
        gb_delta = g - b
        if gb_delta > 10:  # orange only if significantly more green than blue
            return 'O'
        else:
            return 'R'

    # ----- White vs Yellow -----
    # Both have high R and G; B is lower in yellow
    if r >= 175 and g >= 175:
        gb_delta = g - b
        if b < 100 and gb_delta > 60:
            return 'Y'  # Yellow
        else:
            return 'W'  # White

    # ----- Green vs Blue -----
    # Low R, G and B may be close due to noise; classify based on gb_delta
    if r < 200:
        gb_delta = g - b
        if gb_delta > 0:
            return 'G'  # Green
        elif gb_delta < 0:
            return 'B'  # Blue
        else:
            # If G and B are very close, pick the larger
            if g >= b:
                return 'G'
            else:
                return 'B'

    # ----- Catch-all for errors -----
    return '?'  # Should only appear for unexpected RGB values

# Call the C++ executable to get RGB values for a given angle
def get_rgb_from_cpp(angle):
    try:
        result = subprocess.run(['sudo', './getrgb', angle], capture_output=True, text=True, check=True)
        # Last line should be JSON
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

# ---- MAIN ----
def main():
    print("==== RUBI RGB CLASSIFIER ====")
    angle = input("\nEnter angle name to scan (example: angle1): ").strip()

    print("\nRunning getrgb...\n")
    rgb_list = get_rgb_from_cpp(angle)
    if not rgb_list:
        print("Failed to get RGB data. Exiting.")
        return

    print(f"Received {len(rgb_list)} RGB values.\n")

    # Classify each tile
    classified_tiles = [classify_color(t['r'], t['g'], t['b']) for t in rgb_list]

    # Print classified colors
    print("Classified tiles (24):")
    print(classified_tiles)

    # Pre-Kociemba string (just concatenating colors in order)
    cube_string = ''.join(classified_tiles)
    print("\n=== PARTIAL CUBE STRING (24 tiles) ===")
    print(cube_string)
    print("\nNote: This is NOT the final 54-tile string. Additional angles will fill the rest.\n")

if __name__ == "__main__":
    main()

