# 🧠 Building Smarter Flask APIs with In-Memory Data — A Practical Guide by Emmanuel Michael

⏱️ *Estimated Reading Time: 15 minutes*  

---

## 👋 Welcome

Hey there! I’m **Emmanuel Michael**, and in this guide, we’ll build *two progressive Flask APIs* that will help you think and code like a backend engineer.  
We’ll start simple with an **in-memory Stock Manager**, then evolve it into a more advanced **Task Manager** that handles users, tasks, validation, and more.

If you’ve ever wanted to understand *how to design clean, modular Flask APIs* — without getting lost in frameworks or databases — this guide is for you.

---

## 🧭 Table of Contents

1. [Why Flask and In-Memory APIs?](#why-flask-and-in-memory-apis)
2. [Project 1: Stock Manager API](#project-1-stock-manager-api)
3. [Project 2: Task Manager API](#project-2-task-manager-api)
4. [Shared Utilities: validators.py & response.py](#shared-utilities-validatorspy--responsepy)
5. [Testing Your APIs (curl & Postman)](#testing-your-apis-curl--postman)
6. [Folder Structure & Setup](#folder-structure--setup)
7. [Try It Yourself Challenges](#try-it-yourself-challenges)
8. [Next-Level Improvements](#next-level-improvements)
9. [Closing Reflection](#closing-reflection)
10. [About the Author](#about-the-author)

---

## 💡 Why Flask and In-Memory APIs?

Before we touch code, let’s understand *why* this project matters.

**Flask** is perfect for learning and prototyping because it’s:
- Lightweight 🪶
- Flexible 🔧
- Beginner-friendly 👶
- Production-capable 🚀

And **in-memory APIs**? They’re APIs that store data *temporarily in Python lists or dictionaries* instead of a database.  
It’s great for learning because you can focus on *API design, validation, and logic* — without worrying about SQL yet.

---

## 🧱 Project 1: Stock Manager API

Let’s start with something simple: managing stock items.  

Each stock item has:
- A name
- Quantity
- Unit price
- Description

From these, we’ll compute a `total_price` and allow CRUD operations.

### 🔹 Core Endpoints
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/api/v1/item/add` | Add a new item |
| `GET` | `/api/v1/item/all` | Get all items |
| `GET` | `/api/v1/item/<id>` | Get single item |
| `PUT` | `/api/v1/item/<id>/update` | Update an item |
| `DELETE` | `/api/v1/item/<id>/delete` | Delete an item |

---

### 🧩 Sample Endpoint — Add Item

```python
@app.route('/api/v1/item/add', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data:
        return bad_request_response("Invalid payload")

    # Validation example
    error = validate_required_fields(data, 'name')
    if error:
        return bad_request_response(error)

    new_item = {
        "id": len(items) + 1,
        "name": data["name"],
        "quantity": data.get("quantity", 0),
        "unit_price": data.get("unit_price", 0),
        "description": data.get("description", ""),
        "total_price": data.get("quantity", 0) * data.get("unit_price", 0)
    }

    items.append(new_item)
    return success_response("Item added successfully", new_item, 201)
```

💡 **Pro Tip:**  
Always validate input data before adding to your data store. It prevents inconsistent or missing values.

---

### 🧪 Example cURL Test

```bash
curl -X POST http://127.0.0.1:5000/api/v1/item/add -H "Content-Type: application/json" -d '{
    "name": "Rice",
    "quantity": 10,
    "unit_price": 65000,
    "description": "50kg bag of rice"
}'
```

### ✅ Example Response

```json
{
  "status": "success",
  "message": "Item added successfully",
  "data": {
    "id": 1,
    "name": "Rice",
    "quantity": 10,
    "unit_price": 65000,
    "total_price": 650000,
    "description": "50kg bag of rice"
  },
  "timestamp": "2025-10-05T09:00:00Z"
}
```

⚠️ **Common Mistake:**  
Don’t forget to use `request.get_json()` — using `request.form` will break your JSON body.

---

## 👥 Project 2: Task Manager API

Now let’s level up! 🎯  
We’ll build a **Task Manager** that supports both **users** and **tasks** — showing relationships between data.

Each user can have multiple tasks.  
Each task can have statuses like `pending`, `in-progress`, or `completed`.

---

### 🔹 Core Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/api/v1/user/add` | Create user |
| `GET` | `/api/v1/user/all` | Get all users |
| `POST` | `/api/v1/task/add` | Add task |
| `PUT` | `/api/v1/task/<id>/assign/<user_id>` | Assign a task |
| `PUT` | `/api/v1/task/<id>/status/update` | Update status |

---

### 👨‍💻 Sample — Create User Endpoint

```python
@app.route('/api/v1/user/add', methods=['POST'])
def create_user():
    data = request.get_json()

    payload_error = validate_payload(data)
    if payload_error:
        return bad_request_response(payload_error)

    # Validate fields
    error = (
        validate_required_fields(data, 'firstName') or
        validate_required_fields(data, 'lastName') or
        validate_required_fields(data, 'email') or
        validate_required_fields(data, 'phone')
    )
    if error:
        return bad_request_response(error)

    if not validate_email(data['email']):
        return bad_request_response("Invalid email format")

    if not validate_phone(data['phone']):
        return bad_request_response("Invalid phone number")

    new_user = {
        "id": len(users) + 1,
        "firstName": data["firstName"],
        "lastName": data["lastName"],
        "email": data["email"],
        "phone": data["phone"]
    }
    users[new_user["id"]] = new_user
    return success_response("User created successfully", new_user, 201)
```

💡 **Pro Tip:**  
Notice how every step validates data before proceeding. This pattern helps when you move to real databases later.

---

### 🧪 Example cURL Test — Create User

```bash
curl -X POST http://127.0.0.1:5000/api/v1/user/add -H "Content-Type: application/json" -d '{
  "firstName": "Emmanuel",
  "lastName": "Michael",
  "email": "emmanuel@example.com",
  "phone": "08123456789"
}'
```

### ✅ Example Response

```json
{
  "status": "success",
  "message": "User created successfully",
  "data": {
    "id": 1,
    "firstName": "Emmanuel",
    "lastName": "Michael",
    "email": "emmanuel@example.com",
    "phone": "08123456789"
  }
}
```

---

## 🧰 Shared Utilities: validators.py & response.py

Both APIs use the same helper modules — because **reusability is key**.

### ✳️ validators.py (Simplified)

```python
def validate_payload(payload):
    if payload is None:
        return "Payload is missing"
    if not isinstance(payload, dict):
        return "Payload must be a valid JSON object"
    if not payload:
        return "Payload cannot be empty"
    return None

def validate_required_fields(data, field):
    if field not in data or not str(data[field]).strip():
        return f"{field.capitalize()} is required"
    return None

def validate_email(email):
    return "@" in email and "." in email

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 11
```

💡 **Pro Tip:**  
By keeping validators separate, you avoid repetition and make your app easier to test.

---

### ⚙️ response.py

```python
from datetime import datetime
from flask import jsonify

def success_response(message, data=None, status_code=200):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }), status_code

def bad_request_response(error_message, status_code=400):
    return jsonify({
        "status": "error",
        "message": error_message,
        "timestamp": datetime.now().isoformat()
    }), status_code
```

⚠️ **Common Mistake:**  
Avoid repeating `jsonify` logic inside every route — centralize responses like this.

---

## 🧪 Testing Your APIs (curl & Postman)

You can use **Postman** or **curl** for testing.

💡 Example — Fetch all items:
```bash
curl http://127.0.0.1:5000/api/v1/item/all
```

💡 Example — Fetch all users:
```bash
curl http://127.0.0.1:5000/api/v1/user/all
```

💡 Example — Assign a task to a user:
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/task/1/assign/1
```

---

## 🧾 Folder Structure & Setup

```
project_root/
│── app.py                  # Stock Manager API
│── taskManagerApp.py       # Task Manager API
│── validators.py           # Input validation helpers
│── response.py             # Response format helpers
│── README.md               # This guide
│── .venv/                  # Virtual environment (optional)
```

### 🧰 Setup Commands

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Flask
pip install flask

# Run Stock Manager
flask --app app.py run

# Run Task Manager
flask --app taskManagerApp.py run
```

---

## 🧠 Try It Yourself Challenges

🧰 **Challenge 1:** Add an endpoint `/api/v1/item/search/<name>` to find an item by name.  
💡 *Hint:* Use list comprehensions and `.lower()` for case-insensitive search.

🧰 **Challenge 2:** Extend Task Manager to support deadlines and completion timestamps.

🧰 **Challenge 3:** Create a global counter that tracks how many requests the API has handled.

---

## 🚀 Next-Level Improvements

Once you’re comfortable with this setup, try upgrading your API:

| Goal | Description |
|------|--------------|
| 🧱 Add SQLite | Replace lists with persistent storage |
| 🔐 JWT Authentication | Secure user and task routes |
| 🧩 Flask Blueprints | Split routes into modules |
| 🧪 Testing | Use `pytest` for automated tests |
| 🧾 Logging | Track actions and errors |
| 🌍 Deployment | Deploy to Render or Railway |

---

## ✨ Closing Reflection

At this point, you’ve done more than just build two Flask apps —  
you’ve learned **how to think like a backend engineer**.

You now understand:
- How to structure APIs cleanly  
- How to validate and sanitize input  
- How to make reusable code modules  
- How to design endpoints with purpose  

> 💬 “Keep building, keep experimenting — that’s how you grow as a developer.”  
> — *Emmanuel Michael*

---

## 👨‍🏫 About the Author

**Emmanuel Michael** is a Backend Engineer passionate about building scalable APIs and helping others grow into confident developers.  
He loves teaching through practical projects and turning ideas into real, working systems.

---