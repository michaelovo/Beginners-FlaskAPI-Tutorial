# Stock Manager API (Flask)

A simple Flask-based API for managing stock items.  
This project demonstrates how to build a RESTful API in Python using Flask with CRUD operations and test the endpoints with Postman.

---

## Features
- Create, Read, Update, and Delete (CRUD) stock items
- Custom JSON responses with status, message, and timestamp
- Virtual environment setup with `venv`
- Organized code with helper functions
- Postman collection included for easy testing

---

## Requirements
- Python 3.10+ installed
- `pip` package manager
- Postman (optional, for testing)

---

## Installation & Setup

Follow these steps to run the program locally:

1. **Clone the repository**
   ```bash
   https://github.com/michaelovo/Beginners-FlaskAPI-Tutorial.git
   cd stock_manager
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**
   - On Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install project dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Flask environment variables (only needed once)**
   - On Linux/Mac:
     ```bash
     export FLASK_APP=app.py
     export FLASK_ENV=development
     ```
   - On Windows (PowerShell):
     ```bash
     setx FLASK_APP "app.py"
     setx FLASK_ENV "development"
     ```

6. **Run the Flask development server**
   ```bash
   flask run
   ```

By default, the API will be available at:
```
http://127.0.0.1:5000/api/v1/
```

---

## API Endpoints

### Get All Items
```
GET /item/all
```

### Get Single Item
```
GET /item/<id>
```

### Add Item
```
POST /item/add
```
Request body (JSON):
```json
{
  "name": "Rice",
  "quantity": 10,
  "unit_price": 65000,
  "description": "50kg bag of rice"
}
```

### Update Item
```
PUT /item/<id>/update
```
Request body (JSON):
```json
{
  "name": "Updated Rice",
  "quantity": 15
}
```

### Delete Item
```
DELETE /item/<id>/delete
```

---


## Export Dependencies

If you install new Python packages, update the requirements file:
```bash
pip freeze > requirements.txt
```