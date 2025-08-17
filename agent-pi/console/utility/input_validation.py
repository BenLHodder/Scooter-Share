import re

def validate_email(email):
    # regular expression for validating an email
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    
    # Check if the email matches the pattern
    if re.match(email_regex, email):
        return True
    else:
        return False

def validate_input(user_input: str) -> bool:
    """
    Validates user input to ensure it is not empty and does not contain any prohibited characters.
    
    Prohibited characters are:
        - double quotes (\")
        - single quotes (\')
        - backslashes (\\)
    
    If the input is invalid, a message is printed to the console and the function returns False.
    Otherwise, the function returns True.
    
    Prohibited characters are can be added if there is input validation put on when the user creates an account.
    Current characters are to stop an attempt of SQL injection.
    """
    if not user_input:
        print("Input cannot be empty.")
        return False
    
    prohibited_chars = ["\"", "'", "\\"]
    for char in prohibited_chars:
        if char in user_input:
            print(f"Input contains prohibited character: {char}")
            return False
        
    return True