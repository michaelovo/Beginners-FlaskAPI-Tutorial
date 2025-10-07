from flask import Flask, request, jsonify
from datetime import datetime,timezone
from utils.response import format_response, success_response, not_found_response, bad_request_response
from utils.validators import positive_integer, validate_email, validate_field_length, validate_payload, validate_phone, validate_required_fields, validate_unique_field

app = Flask(__name__)

users = {}
tasks = {}

next_user_id = 1
next_task_id = 1





# ============ USERS MANAGER ENDPOINTS ============

#create a user
@app.route('/api/v1/user/add', methods=['POST'])
def create_user():
    global next_user_id
    data = request.get_json()

    # Validate payload
    payload = validate_payload(data)
    if payload:
        return bad_request_response(payload)

    # Validate required fields
    error = validate_required_fields(data, 'firstName') or validate_required_fields(data,'lastName') or validate_required_fields(data,'email') or validate_required_fields(data,'phone') or     validate_field_length(data,'firstName') or validate_field_length(data,'lastName')
    if error:
        return bad_request_response(error)

    
    # Validate email format (basic validation)
    if not validate_email(data['email']):
        return bad_request_response("Invalid email format")
    
    # Validate phone number (basic validation)
    if not validate_phone(data['phone']):
                return bad_request_response("Phone number must be numeric and at least 11 digits long starting with a valid prefix (070, 080, 090, 081, 091)")
        
    # Check for duplicate emails
    if not validate_unique_field(users, 'email', data['email']):
        return bad_request_response(f"User with email '{data['email']}' already exists")
 
    # Check for duplicate phone numbers
    if not validate_unique_field(users, 'phone', data['phone']):
        return bad_request_response(f"User with phone number '{data['phone']}' already exists")
    
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

    # Ensure payload is json and not empty or null
    payload = validate_payload(data)
    if payload:
        return bad_request_response(payload)


    # Validate required fields
    error = validate_required_fields(data, 'firstName') or validate_required_fields(data,'lastName') or validate_required_fields(data,'email') or validate_required_fields(data,'phone') or validate_field_length(data,'firstName') or validate_field_length(data,'lastName')
    if error:
        return bad_request_response(error)

    # Check if user exists
    if not user:
        return not_found_response(f"User with id {user_id} not found")
    

    # Validate email format (basic validation)
    if not validate_email(data['email']):
        return bad_request_response("Invalid email format")
    
    # Validate phone number (basic validation)
    if not validate_phone(data['phone']):
                return bad_request_response("Phone number must be numeric and at least 11 digits long starting with a valid prefix (070, 080, 090, 081, 091)")
        
    # Check for duplicate emails
    if not validate_unique_field(users, 'email', data['email']):
        return bad_request_response(f"User with email '{data['email']}' already exists")
 
    # Check for duplicate phone numbers
    if not validate_unique_field(users, 'phone', data['phone']):
        return bad_request_response(f"User with phone number '{data['phone']}' already exists")
      
    user = {
        'id': user_id,
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'email': data['email'],
        'phone': data['phone']
    }

    users[user_id] = user # Save updated user
    return success_response("User updated successfully", format_response(user,'user'))


# Fetch tasks by user_id
@app.route('/api/v1/user/<int:user_id>/tasks', methods=['GET'])
def get_tasks_by_user(user_id):
    if user_id not in users:
        return not_found_response(f"User with id {user_id} not found")
    
    # Filter tasks by user_id
    user_tasks = [task for task in tasks.values() if task['user_id'] == user_id]
    
    # Check if user has tasks
    if not user_tasks:
        return success_response(f"No tasks assign to user with id {user_id} at the moment", [])
    
    return jsonify(success_response(f"Tasks for user with id {user_id} retrieved successfully", format_response(user_tasks, 'tasks')))

    
# Delete user by id
@app.route('/api/v1/user/<int:user_id>/delete', methods=['DELETE'])
def delete_user(user_id):
    user = users.pop(user_id, None) # Remove user by id

    # Set associated tasks' user_id to None
    for task in tasks.values():
        if task['user_id'] == user_id:
            task['user_id'] = None
    
     # Check if user exists
    if not user:
        return not_found_response(f"User with id {user_id} not found")
    
    return success_response("User deleted successfully")



# ============ TASK MANAGER ENDPOINTS ============

# Create a task
@app.route('/api/v1/task/add', methods=['POST'])
def create_task():
    global next_task_id # Access the global task ID counter
    data = request.get_json() # Get data from request body

    payload = validate_payload(data)
    if payload:
        return bad_request_response(payload)
  
    # Validate required fields
    error = validate_required_fields(data, 'title') or validate_required_fields(data,'description') or validate_required_fields(data,'duration') or  validate_field_length(data,'title')
    if error:
        return bad_request_response(error)
    
    # user_id field is in the payload then extract it and perform validation else set default to null
    if 'user_id' in data and isinstance(data['user_id'], int) and data['user_id'] <= 0:
        user_id = data['user_id'] # Extract user_id from request data

        #validate user_id is an integer
        if not isinstance(user_id, int):
            return bad_request_response("user_id must be an integer")
        
        # Check if user exists
        if user_id not in users:
            return not_found_response(f"User with id {user_id} not found")
    else:
        user_id = None # Set user_id to None if not provided or invalid

    # Check for duplicate title
    if not validate_unique_field(tasks, 'title', data['title']):
        return bad_request_response(f"Task with title '{data['title']}' already exists")
     
    # Validate duration is a positive integer
    if not positive_integer(data['duration']):
        return bad_request_response(f"Duration must be a positive integer representing minutes, and must not be less than 5 minutes")
     
    task_status = 'pending'
    task = {
        'id': len(tasks) + 1,
        'user_id': user_id,
        'title': data['title'],
        'description': data['description'],
        'status': task_status,
        'duration': data['duration'],
        'created_at': datetime.now(timezone.utc).isoformat(),
        'updated_at': None,
        'completed_at': None
    }
    tasks[next_task_id] = task
    next_task_id += 1
    return success_response("Task created successfully", format_response(task,'task'), 201)

# Fetch all tasks
@app.route('/api/v1/task/all', methods=['GET'])
def get_tasks():

    if not tasks:
        return jsonify(success_response("No tasks at the moment"))
    
    return jsonify(success_response("Tasks retrieved successfully",format_response(tasks.values(), 'tasks')))


# Fetch single task by id
@app.route('/api/v1/task/<int:task_id>/fetch', methods=['GET'])
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return not_found_response(f"Task with id {task_id} not found")
    return jsonify(success_response("Task retrieved successfully", format_response(task,'task')))


# Update task by id
@app.route('/api/v1/task/<int:task_id>/update', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() # Get data from request body
    task = tasks.get(task_id) # Fetch task by id

    # Check if task exists
    if not task:
        return not_found_response(f"Task with id {task_id} not found")
    
    # Validate data type, length and none emptiness for title
    if 'title' in data:
        if not isinstance(data['title'], str) or not data['title'].strip() or len(data['title']) < 3:
            return bad_request_response("Title must be a non-empty string of at least 3 characters")
        
        task['title'] = data['title'] # Update title
    
    # Validate data type and none emptiness
    if 'description' in data:
        if not isinstance(data['description'], str) or not data['description'].strip():
            return bad_request_response("Description must be a non-empty string")
        
        task['description'] = data['description'] # Update description
    
    # Validate data type and positive integer
    if 'duration' in data:
        if not isinstance(data['duration'], int) or data['duration'] <= 5:
            return bad_request_response("Duration must be a positive integer representing minutes, and must not be less than 5 minutes")
        
        task['duration'] = data['duration'] # Update duration
    
    
    task['updated_at'] = datetime.now(timezone.utc).isoformat() # Update the updated_at timestamp
    tasks[task_id] = task # Save updated task
    return success_response("Task updated successfully", format_response(task,'task'))


# Delete task by id
@app.route('/api/v1/task/<int:task_id>/delete', methods=['DELETE'])
def delete_task(task_id):
    task = tasks.pop(task_id, None) # Remove task by id
    if not task:
        return not_found_response(f"Task with id {task_id} not found")
    
    return success_response("Task deleted successfully")


# Assign a task to a user
@app.route('/api/v1/task/<int:task_id>/assign/<int:user_id>', methods=['PUT'])
def assign_task_to_user(task_id, user_id):
    task = tasks.get(task_id)
    if not task:
        return not_found_response(f"Task with id {task_id} not found")
    
    if user_id not in users:
        return not_found_response(f"User with id {user_id} not found")
    
    task['user_id'] = user_id
    task['updated_at'] = datetime.now(timezone.utc).isoformat() # Update the updated_at timestamp
    tasks[task_id] = task # Save updated task
    return success_response(f"Task with id {task_id} assigned to user with id {user_id} successfully", format_response(task,'task'))

# update task status to completed
@app.route('/api/v1/task/<int:task_id>/status/update', methods=['PUT'])
def mark_task_as_completed(task_id):
    data = request.get_json() # Get data from request body
    allowed_statuses = ['pending', 'in-progress', 'completed'] # Define allowed statuses
    task = tasks.get(task_id) # Fetch task by id

    # Check if task exists
    if not data or 'status' not in data:
        return bad_request_response("status field is required")
    
    # Validate task status value
    if data['status'] not in allowed_statuses:
            return bad_request_response("Invalid task status. Allowed values are: pending, in-progress, completed")
    
    # Check if task exists
    if not task:
        return not_found_response(f"Task with id {task_id} not found")

    # Check if task is already completed
    if task['status'] == 'completed':
        return bad_request_response(f"Task with id {task_id} is already marked as completed")
    
    # update task status based on input
    task['status'] = data['status']

    # If status is completed, set the completed_at timestamp
    if data['status'] == 'completed':
        task['completed_at'] = datetime.now(timezone.utc).isoformat() # Set the completed_at timestamp
    task['updated_at'] = datetime.now(timezone.utc).isoformat() # Update the updated_at timestamp
    tasks[task_id] = task # Save updated task

    return success_response(f"Task with id {task_id} marked as {data['status']} successfully", format_response(task,'task'))