from flask import Flask, request, jsonify
from datetime import datetime,timezone
from utils.response import format_response, format_user, format_todo, format_users, format_todos, make_response, success_response, not_found_response, bad_request_response

app = Flask(__name__)

users = {}
todos = {}

next_user_id = 1
next_todo_id = 1

#create a user
@app.route('/api/v1/user/add', methods=['POST'])
def create_user():
    global next_user_id
    data = request.get_json()
    if not data or 'firstName' not in data or 'lastName' not in data or 'email' not in data or 'phone' not in data:
        return bad_request_response("firstName, lastName, email and phone fields are required")
    
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