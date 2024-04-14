import pytest
from email_validator import EmailNotValidError
from website.dashboard.userValidation import *

'''
THESE UNIT TESTS TEST THE 'userValidation' FUNCTION TO ENSURE CORRECT FORMAT UPON WEBSITE REGISTRATION
'''

# Test cases for is_valid_name function
def test_is_valid_name_valid():
    assert is_valid_name("JohnDoe") == True

def test_is_valid_name_too_short():
    assert is_valid_name("Jo") == False

def test_is_valid_name_too_long():
    assert is_valid_name("JohnDoeJohnDoeJohnDoe") == False

def test_is_valid_name_contains_non_alpha():
    assert is_valid_name("JohnDoe123") == False

def test_is_valid_name_empty():
    assert is_valid_name("") == False


# Test cases for is_valid_password function
def test_is_valid_password_valid():
    assert is_valid_password("Passw0rd") == True

def test_is_valid_password_too_short():
    assert is_valid_password("Passw0r") == False

def test_is_valid_password_too_long():
    assert is_valid_password("Passw0rdPassw0rdPassw0rd") == False

def test_is_valid_password_no_uppercase():
    assert is_valid_password("password0") == False

def test_is_valid_password_no_lowercase():
    assert is_valid_password("PASSWORD0") == False

def test_is_valid_password_no_digit():
    assert is_valid_password("Password") == False

def test_is_valid_password_empty():
    assert is_valid_password("") == False


# Test cases for is_valid_email function
def test_is_valid_email_valid():
    assert is_valid_email("knijjar01@qub.ac.uk") == True

def test_is_valid_email_invalid():
    assert is_valid_email("123@z") == False

def test_is_valid_email_invalid():
    assert is_valid_email("correctformat@example.com") == False


'''scaling tests
@pytest.mark.parametrize("email, expected_result", [
    ("hello@gmail.com", True),
    ("test@example.com", False)
])
def test_is_valid_email_with_mocking(email, expected_result, mocker):
    mocker.patch("email_validator.validate_email")
    email_validator_mock = mocker.patch("email_validator.validate_email")
    email_validator_mock.side_effect = [None, EmailNotValidError]

    assert is_valid_email(email) == expected_result
'''
