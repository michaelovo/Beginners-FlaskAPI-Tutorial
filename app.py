from flask import Flask, request, jsonify
from utils.response import bad_request_response, format_item, format_items, format_response, make_response, not_found_response, success_response
from utils.validators import positive_integer, positive_value, validate_payload, validate_required_fields, validate_unique_field

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
        return success_response("No items found", format_response(items,'items'))
    return success_response("Items retrieved successfully", format_response(items,'items'))


#fetch single item by id
@app.route('/api/v1/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    single_item = next((item for item in items if item['id'] == item_id), None)
    if single_item:
        return success_response("Item retrieved successfully", format_response(single_item,'item'))
    return not_found_response(f"Item with id {item_id} not found")



#add new item
@app.route('/api/v1/item/add', methods=['POST'])
def add_item():
    global item_id_counter
    data = request.get_json()
    
    # Validate payload
    payload = validate_payload(data)
    if payload:
        return bad_request_response(payload)

    # Validate required fields
    error = validate_required_fields(data,'name') or validate_required_fields(data,'unit_price') or validate_required_fields(data,'quantity')
    if error:
        return bad_request_response(error)
    
    # Validate data types
    if not positive_value(data['unit_price']) or not positive_integer(data['quantity']):
        return bad_request_response('Invalid data type: quantity must be a positive integer, unit_price must be a positive number')

    # Check for duplicate item names (case-insensitive)
    if not validate_unique_field(items,'name', data['name']):
        return bad_request_response(f"Item with name '{data['name']}' already exists")
       
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

    return success_response("New item added successfully",format_response(new_item,'item'), 200)


# Update a item
@app.route("/api/v1/item/<int:item_id>/update", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    item = next((t for t in items if t["id"] == item_id), None)

    if not item:
        return not_found_response(f"Item with id {item_id} not found")

    item["name"] = data.get("name", item["name"])
    item["description"] = data.get("description", item["description"])
    item["quantity"] = data.get("quantity", item["quantity"])
    item["unit_price"] = data.get("unit_price", item["unit_price"])
    item["total_price"] = item["quantity"] * item["unit_price"]

    return success_response("Item updated successfully",format_response(item,'item'), 200)

#delete item
@app.route('/api/v1/item/<int:item_id>/delete', methods=['DELETE'])
def delete_item(item_id):
    global items

    # Find the item
    item_to_delete = next((item for item in items if item['id'] == item_id), None)
    
    if item_to_delete is None:
        return not_found_response(f"Item with id {item_id} not found")
    
    # Remove item from list
    items.remove(item_to_delete)
    return success_response("Item deleted successfully")