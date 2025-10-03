from datetime import datetime,timezone

def format_item(item):
    return {
        'id': item['id'],
        'name': item['name'],
        'quantity': item['quantity'],
        'unit_price': item['unit_price'],
        'total_price': item['total_price'],
        'description': item['description'],
    }

def format_items(items):
    return [format_item(item) for item in items]

def make_response(status, message, data=None, code=200):
    return {
        'status': status,
        'message': message,
        'data': data,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }, code