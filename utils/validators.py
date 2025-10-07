import re


# Validate that payload exists
def validate_payload(payload):
       if payload is None:
           return "Payload is missing"
       if not isinstance(payload, dict):
           return "Payload must be a valid JSON object"
       if not payload:  # Empty dictionary
           return "Payload cannot be empty"
       return None

# Validate that a field is present and non-empty in the payload
def validate_required_fields(data, field):
    if field not in data or not str(data[field]).strip():
        return f"{field.capitalize()} is required and cannot be empty"
    return None

def allow_alphanumeric_length(data, field, min=3):
    value = str(data.get(field, '')).strip()
    if not value.isalnum() or len(value) < min:
        return f"{field.capitalize()} must be alphanumeric and at least {min} characters long"
    return None

# Validate input field value be only alphabetic and length to be minimum of 3 characters
def validate_field_length(data,field,min=3):
     if field not in data or not (data[field].isalpha())  or len(str(data[field]).strip()) < min:
          return f"{field.capitalize()} cannot be less than {min} alphabetic characters" 
     return None

# Validate email format (basic validation)
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# Validate phone number (basic validation)
def valid_phone_isDigit_and_length(phone, min = 11):
     return (phone.isdigit() and len(phone) >= min)
     

# Phone number should start with a valid prefix
def valid_phone_format(phone):
    valid_prefixes = ['070', '080', '090', '081', '091']
    return any(phone.startswith(prefix) for prefix in valid_prefixes)

# validate phone
def validate_phone(phone):
     return valid_phone_isDigit_and_length(phone) and valid_phone_format(phone)

# Check for duplicate record to prevent redundancy   
def validate_unique_field(tables, field, value):
    """
    Check if a field value is unique across all records.
    Returns True if unique, False if duplicate exists.
    """

    # handles both list and dictionary
    records = tables.values() if isinstance(tables, dict) else tables
    return not any(
        record.get(field, '').lower() == value.lower() 
        for record in records
    )

# Validate integer
def positive_integer(value, min =1 ):
     return isinstance(value,int) and value >= min

# Validate float
def positive_float(value, min = 1.0):
     return isinstance(value, float) and value >= min

# Validate positive value
def positive_value(value):
     return positive_integer(value) or positive_float(value)