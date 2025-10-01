from flask import Flask, jsonify, request

app = Flask(__name__)

#in memory data store
items = []
item_id_counter = 1

#fetch all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items), 200


#fetch single item by id
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    single_item = next((item for item in items if item['id'] == item_id), None)
    if single_item:
        return jsonify(single_item), 200
    return jsonify({'error': 'Item not found'}), 404


#add new item
@app.route('/items', methods=['POST'])
def add_item():
    global item_id_counter
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    new_item = {
        'id': item_id_counter,
        'name': data['name'],
        'description': data.get('description', '')
    }
    items.append(new_item)
    item_id_counter += 1
    return jsonify(new_item), 201

#update existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    for item in items:
        if item['id'] == item_id:
            item['name'] = data['name']
            item['description'] = data.get('description', item['description'])
            return jsonify(item), 200
    return jsonify({'error': 'Item not found'}), 404

# Update a task
# @app.route("/tasks/<int:task_id>", methods=["PUT"])
# def update_task(task_id):
#     data = request.get_json()
#     task = next((t for t in tasks if t["id"] == task_id), None)

#     if not task:
#         return jsonify({"error": "Task not found"}), 404

#     task["title"] = data.get("title", task["title"])
#     task["description"] = data.get("description", task["description"])
#     task["completed"] = data.get("completed", task["completed"])

#     return jsonify(task), 200

#delete item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'}), 200