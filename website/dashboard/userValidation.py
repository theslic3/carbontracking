from email_validator import validate_email, EmailNotValidError

def is_valid_name(name):
    if not name:
        return False
    if len(name) < 4 or len(name) > 20:
        return False
    if not name.isalpha():  # Check if name contains only alphabetic characters
        return False
    return True

def is_valid_password(password):
    if not password:
        return False
    if len(password) < 8 or len(password) > 20:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True

def is_valid_email(email):
    try:
        # Validate the email address using library
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
