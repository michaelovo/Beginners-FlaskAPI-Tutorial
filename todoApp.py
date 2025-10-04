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
    return success_response("User created successfully", format_user(user), 201)

# Fetch all users
@app.route('/api/v1/user/all', methods=['GET'])
def get_users():

    if not users:
        return jsonify(success_response("No users at the moment"))
    
    return jsonify(success_response("Users retrieved successfully",format_response(users.values(), 'users')))


# Fetch single user by id
@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return not_found_response(f"User with id {user_id} not found")
    return jsonify(success_response("User retrieved successfully", format_response(user,'user')))
