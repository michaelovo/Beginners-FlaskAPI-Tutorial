from datetime import datetime,timezone

# Helper function for single item formatting
def format_item(item):
    return {
        'id': item['id'],
        'name': item['name'],
        'quantity': item['quantity'],
        'unit_price': item['unit_price'],
        'total_price': item['total_price'],
        'description': item['description'],
    }

# Helper function for multiple items formatting
def format_items(items):
    return [format_item(item) for item in items]

# Helper functions for standardized responses
def make_response(status, message, data=None, code=200):
    return {
        'status': status,
        'message': message,
        'data': data,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }, code


# Helper functions to format user
def format_user(user):
    return {
        'id': user['id'],
        'firstName': user['firstName'],
        'lastName': user['lastName'],
        'email': user['email'],
        'phone': user['phone']
    }

# Helper functions to format task
def format_task(task):
    return {
        'id': task['id'],
        'user_id': task['user_id'],
        'title': task['title'],
        'description': task['description'],
        'status': task['status'],
        'duration': task['duration'],
        'created_at': task['created_at'],
        'updated_at': task['updated_at'],
        'completed_at': task['completed_at']    
    }

# Helper functions to format list of users
def format_users(users):
    return [format_user(user) for user in users]

# Helper functions to format list of tasks
def format_tasks(tasks):
    return [format_task(task) for task in tasks]

# Success helper functions
def success_response(message, data=None, status_code=200):
    return make_response("success", message, data, status_code)


#not found helper function responses
def not_found_response(message="Resource not found"):
    return make_response("error", message, None, 404)

# bad request helper function responses
def bad_request_response(message="Bad request"):
    return make_response("error", message, None, 400)

# internal server error helper function responses
def internal_error_response(message="Internal server error"):
    return make_response("error", message, None, 500)

# Format data based on type
def format_response(data, data_type):
    if data_type == 'user':
        return format_user(data)
    elif data_type == 'task':
        return format_task(data)
    elif data_type == 'users':
        return format_users(data)
    elif data_type == 'tasks':
        return format_tasks(data)
    else:
        return data