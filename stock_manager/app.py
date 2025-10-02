from flask import Flask, request, jsonify
from utils.response import format_item, format_items, make_response

app = Flask(__name__)


#in memory data store
items = [
        {"id": 1, "name": "Rice", "quantity": 10, "unit_price": 65000, "total_price": 650000, "description": "50kg bag of rice"},
        {"id": 2, "name": "Salt", "quantity": 5, "unit_price": 400, "total_price": 2000, "description": "2kg dangote salt"}
]
item_id_counter = 1

#fetch all items
@app.route('/api/v1/item/all', methods=['GET'])
def get_items():
    if not items:
        return jsonify(make_response("success", "No items found", [], 200)[0]), 200
    return jsonify(make_response(
        "success",
        "Items retrieved successfully",
        format_items(items),
        200
    )[0]), 200


#fetch single item by id
@app.route('/api/v1/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    single_item = next((item for item in items if item['id'] == item_id), None)
    if single_item:
        return jsonify(make_response(
            "success",
            "Item retrieved successfully",
            format_item(single_item),
            200
        )[0]), 200
    return jsonify(make_response("error", f"Item {item_id} not found", None, 404)[0]), 404



#add new item
@app.route('/api/v1/item/add', methods=['POST'])
def add_item():
    global item_id_counter
    data = request.get_json()

    # Validate required fields
    if not data or 'name' not in data or 'unit_price' not in data or 'quantity' not in data:
        return jsonify({
            "status": "error",
            "message": "Missing required fields: name, quantity, unit_price"
        }), 400
    
    # Validate data types
    if not isinstance(data['name'], str) or not isinstance(data['unit_price'], (int, float)) or not isinstance(data['quantity'], int):
        return jsonify({
            "status": "error",
            "message": "Invalid data types for fields: name must be a string, quantity must be an integer, unit_price must be a number"
        }), 400

    #validate name is not empty
    if not data['name'].strip():
        return jsonify({
            "status": "error",
            "message": "Item name cannot be empty"
        }), 400
    
    # Validate quantity and unit_price are non-negative
    if data['quantity'] <= 0 or data['unit_price'] <= 0:
        return jsonify({
            "status": "error",
            "message": "Quantity and unit_price must be non-negative/greater than zero"
        }), 400

    
    # Check for duplicate item names (case-insensitive)
    if any(item['name'].lower() == data['name'].lower() for item in items):
        return jsonify(make_response("error", f"Item with name '{data['name']}' already exists", None, 400)[0]), 400
       
    new_item = {
        "id": len(items) + 1,
        'name': data['name'],
        'quantity': data.get('quantity', 1),
        'unit_price': data['unit_price'],
        'description': data.get('description', ''),
        'total_price': data['quantity'] * data['unit_price']
    }
    items.append(new_item)
    item_id_counter += 1

    return jsonify(make_response(
        "success",
        "New item added successfully",
        format_item(new_item),
        200
    )[0]), 200


# Update a item
@app.route("/api/v1/item/<int:item_id>/update", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    item = next((t for t in items if t["id"] == item_id), None)

    if not item:
        return jsonify(make_response("error", f"Item with ID: {item_id} not found", None, 404)[0]), 404

    item["name"] = data.get("name", item["name"])
    item["description"] = data.get("description", item["description"])
    item["quantity"] = data.get("quantity", item["quantity"])
    item["unit_price"] = data.get("unit_price", item["unit_price"])
    item["total_price"] = item["quantity"] * item["unit_price"]

    return jsonify(make_response(
        "success",
        "Item updated successfully",
        format_item(item),
        200
    )[0]), 200

#delete item
@app.route('/api/v1/item/<int:item_id>/delete', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify(make_response(
        "success",
        "Item deleted successfully",
        None,
        200
    )[0]), 200