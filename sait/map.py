from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# This will store our list of movements
command_queue = []

@app.route('/')
def index():
    # This will serve your map.html file if it's in a folder named 'templates'
    return render_template('map.html')

@app.route('/save-path', methods=['POST'])
def save_path():
    global command_queue
    command_queue = request.json
    print(f"Path Received: {len(command_queue)} steps")
    return jsonify({"status": "success", "message": "Path saved"})

@app.route('/get-command', methods=['GET'])
def get_command():
    global command_queue
    if len(command_queue) > 0:
        # Take the first command out of the list
        return jsonify(command_queue.pop(0))
    else:
        return jsonify({"action": "idle", "time": 0})

if __name__ == '__main__':
    # Run on port 5000 (Flask default)
    app.run(host='0.0.0.0', port=5000, debug=True)