from flask import Flask, request, jsonify
from datetime import datetime,timezone
from utils.response import format_response, format_user, format_todo, format_users, format_todos, make_response, success_response, not_found_response, bad_request_response

app = Flask(__name__)

users = {}
todos = {}

next_user_id = 1
next_todo_id = 1

# USER SETTINGS
#create a user
@app.route('/api/v1/user/add', methods=['POST'])
def create_user():
    global next_user_id
    data = request.get_json()
    if not data or 'firstName' not in data or 'lastName' not in data or 'email' not in data or 'phone' not in data:
        return bad_request_response("firstName, lastName, email and phone fields are required")
    
    # Validate firstName and lastName are not empty
    if not data['firstName'].strip() or not data['lastName'].strip():
        return bad_request_response("firstName and lastName cannot be empty")

    #Validate firstName and lastName to be strings
    if not isinstance(data['firstName'], str) or not isinstance(data['lastName'], str):
        return bad_request_response("firstName and lastName must be strings")
    
    #Validate firstName and LastNmae to be minimum of two(2) characters
    if not data['firstName'].isalpha() or not data['lastName'].isalpha() or len(data['firstName']) < 2 or len(data['lastName']) < 2:
        return bad_request_response("firstName and lastName must be alphabetic and at least 2 characters long")
    
    # Validate email format (basic validation)
    if '@' not in data['email'] or '.' not in data['email']:
        return bad_request_response("Invalid email format")
    
    # Validate email to not be empty
    if not data['email'].strip():
        return bad_request_response("Email cannot be empty")
    
    # Validate phone number (basic validation)
    if not data['phone'].isdigit() or len(data['phone']) < 11:
        return bad_request_response("Phone number must be numeric and at least 7 digits long")
    
    # Validate phone to not be empty
    if not data['phone'].strip():
        return bad_request_response("Phone number cannot be empty")
    
    # Check for duplicate emails
    if any(user['email'].lower() == data['email'].lower() for user in users.values()):
        return bad_request_response(f"User with email '{data['email']}' already exists")
    
    # Check for duplicate phone numbers
    if any(user['phone'] == data['phone'] for user in users.values()):
        return bad_request_response(f"User with phone number '{data['phone']}' already exists")
    
    # Phone number should start with a valid prefix
    valid_prefixes = ['070', '080', '090', '081', '091']
    if not any(data['phone'].startswith(prefix) for prefix in valid_prefixes):
        return bad_request_response("Phone number must start with a valid prefix (070, 080, 090, 081, 091)")
    
    user = {
        'id': len(users) + 1,
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'email': data['email'],
        'phone': data['phone']
    }
    users[next_user_id] = user
    next_user_id += 1
    return success_response("User created successfully", format_response(user, 'user'), 201)

# Fetch all users
@app.route('/api/v1/user/all', methods=['GET'])
def get_users():

    if not users:
        return jsonify(success_response("No users at the moment"))
    
    return jsonify(success_response("Users retrieved successfully",format_response(users.values(), 'users')))


# Fetch single user by id
@app.route('/api/v1/user/<int:user_id>/fetch', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return not_found_response(f"User with id {user_id} not found")
    return jsonify(success_response("User retrieved successfully", format_response(user,'user')))

# Update user by id and avoid duplicate email and phone number
@app.route('/api/v1/user/<int:user_id>/update', methods=['PUT'])
def update_user(user_id):
    data = request.get_json() # Get data from request body
    user = users.get(user_id) # Fetch user by id

    # Check if user exists
    if not user:
        return not_found_response(f"User with id {user_id} not found")
    
    # Update fields if provided
    if 'firstName' in data:
        # Validate data type, none emptiness and length
        if not isinstance(data['firstName'], str) or not data['firstName'].strip() or not data['firstName'].isalpha() or len(data['firstName']) < 2:
            return bad_request_response("firstName must be a non-empty alphabetic string of at least 2 characters")
        
        user['firstName'] = data['firstName'] # Update firstName
    
    if 'lastName' in data:
        # Validate data type, none emptiness and length
        if not isinstance(data['lastName'], str) or not data['lastName'].strip() or not data['lastName'].isalpha() or len(data['lastName']) < 2:
            return bad_request_response("lastName must be a non-empty alphabetic string of at least 2 characters")
        
        user['lastName'] = data['lastName'] # Update lastName
    
    if 'email' in data:
        # Validate data type
        if not isinstance(data['email'], str):
            return bad_request_response("Email must be a valid string")
        
        # Validate email format and none emptiness
        if '@' not in data['email'] or '.' not in data['email'] or not data['email'].strip():
            return bad_request_response("Invalid email format")
        
        # Check for duplicate emails
        if any(u['email'].lower() == data['email'].lower() and u['id'] != user_id for u in users.values()):
            return bad_request_response(f"User with email '{data['email']}' already exists")
        
        user['email'] = data['email'] # Update email
    
    if 'phone' in data:

        # Validate data type
        if not isinstance(data['phone'], str):
            return bad_request_response("Phone number must be a string of digits")
        
        # Validate phone number length, none emptiness, and numeric
        if not data['phone'].isdigit() or len(data['phone']) < 11 or not data['phone'].strip():
            return bad_request_response("Phone number must be numeric and at least 11 digits long")
        
        # Validate phone number prefix
        valid_prefixes = ['070', '080', '090', '081', '091']
        if not any(data['phone'].startswith(prefix) for prefix in valid_prefixes):
            return bad_request_response("Phone number must start with a valid prefix (070, 080, 090, 081, 091)")
        
        # Check for duplicate phone numbers
        if any(u['phone'] == data['phone'] and u['id'] != user_id for u in users.values()):
            return bad_request_response(f"User with phone number '{data['phone']}' already exists")
        
        user['phone'] = data['phone'] # Update phone number
    
    users[user_id] = user # Save updated user
    return success_response("User updated successfully", format_response(user,'user'))

# Delete user by id
@app.route('/api/v1/user/<int:user_id>/delete', methods=['DELETE'])
def delete_user(user_id):
    user = users.pop(user_id, None) # Remove user by id
    if not user:
        return not_found_response(f"User with id {user_id} not found")
    
    return success_response("User deleted successfully")