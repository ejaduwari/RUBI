from flask import Flask, render_template, request, jsonify
import test  # reuse your test.py functions

app = Flask(__name__)

# ------------------------------
# Route: Home page
# ------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ------------------------------
# Route: Capture angle1 (U,L,F)
# ------------------------------
@app.route("/capture_angle1", methods=["POST"])
def capture_angle1():
    rgb_list = test.get_rgb_from_cpp("angle1")
    if not rgb_list:
        return jsonify({"success": False, "message": "Failed to get RGB from angle1"})
    test.save_angle1(rgb_list)
    return jsonify({"success": True, "faces": test.angle_data})

# ------------------------------
# Route: Capture angle2 (D,R,B)
# ------------------------------
@app.route("/capture_angle2", methods=["POST"])
def capture_angle2():
    rgb_list = test.get_rgb_from_cpp("angle2")
    if not rgb_list:
        return jsonify({"success": False, "message": "Failed to get RGB from angle2"})
    test.save_angle2(rgb_list)
    return jsonify({"success": True, "faces": test.angle_data})

# ------------------------------
# Route: Solve Cube (reads table edits)
# ------------------------------
@app.route("/solve", methods=["POST"])
def solve_cube():
    data = request.json
    if "faces" in data:
        # Update colors from web table edits
        for face, face_data in data["faces"].items():
            test.angle_data[face]["colors"] = face_data["colors"]
    kociemba_str = test.assemble_kociemba_string()
    moves = test.run_solver(kociemba_str)
    test.send_to_esp32(moves)
    return jsonify({"kociemba": kociemba_str, "moves": moves})

# ------------------------------
# Route: Scramble Cube
# ------------------------------
@app.route("/scramble", methods=["POST"])
def scramble_cube():
    test.scramble_cube()
    return jsonify({"success": True})

# ------------------------------
# Run Flask
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
