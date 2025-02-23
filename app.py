from flask import Flask, request, jsonify
from database import Database
from flask_cors import CORS
from datetime import datetime


app=Flask(__name__)
CORS(app)

database_file = Database(r'db/journal.db')

entries=database_file.get_entries()
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'web-app working properly'})


@app.route('/entries', methods=['GET'])
def fetch_entries():
    f_entries = [
        {'id': entry[0], 'title': entry[1], 'content': entry[2],'date': entry[3]}
        for entry in entries
    ]
    return jsonify(f_entries)


@app.route('/create', methods=['POST'])
def create_entry():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    database_file.add_entry(title, content, date)
    return jsonify({'message': 'entry succesfully created'})


@app.route('/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    database_file.delete_entry(entry_id)
    return jsonify({'message': 'entry successfully deleted'})

@app.route("/update/<int:entry_id>", methods=['GET',"PUT"])
def update_entry(entry_id):
    if not request.is_json:
        return jsonify({'error': 'request must be json'}), 400
    data = request.json
    new_title = data.get('title')
    new_content = data.get('content')
    if new_title and new_content:
    
        database_file.update_entry(entry_id, new_title, new_content)
        return jsonify({"message": "Entry updated!"})
    return jsonify({"error": "Title or Content not given"}), 404




if __name__=='__main__':
   app.run(host="0.0.0.0", port=5000)