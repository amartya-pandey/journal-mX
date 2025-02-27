from flask import Flask, request, jsonify
from database import Database
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

database_file = Database('db/journal.db')

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Web app working properly'})

@app.route('/entries', methods=['GET'])
def fetch_entries():
    entries = database_file.get_entries()
    return jsonify([
        {'id': entry[0], 'title': entry[1], 'content': entry[2], 'date': entry[3]}
        for entry in entries
    ])

@app.route('/create', methods=['POST'])
def create_entry():
    data = request.get_json()
    title, content = data.get('title'), data.get('content')

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    database_file.add_entry(title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({'message': 'Entry successfully created'}), 201

@app.route('/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    database_file.delete_entry(entry_id)
    return jsonify({'message': 'Entry successfully deleted'}), 200

@app.route('/update/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.json
    new_title, new_content = data.get('title'), data.get('content')

    if not new_title or not new_content:
        return jsonify({"error": "Title and content are required"}), 400

    database_file.update_entry(entry_id, new_title, new_content)
    return jsonify({"message": "Entry updated successfully!"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
