from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import os, os.path

app = Flask(__name__)
CORS(app)  # This allows all origins. For production, you might want to configure this more strictly.
directory = "json"

@app.route('/api/submit', methods=['POST'])
def submit_entry():
    data = request.json
    
    if not data or 'name' not in data or 'usn' not in data or 'images' not in data:
        return jsonify({"error": "Invalid data format"}), 400
    
    new_entry = {
        "name": data['name'],
        "usn": data['usn'],
        "images": data['images']
    }
    
    # Save to file
    if not os.path.exists(directory): os.makedirs(directory)
    DATA_FILE = f"{directory}/{data['name']}.json"
    with open(DATA_FILE, 'w') as f:
        json.dump(new_entry, f, indent=2)
    
    return jsonify({"message": "Entry added successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)