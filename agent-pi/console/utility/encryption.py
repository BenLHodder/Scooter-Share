from werkzeug.security import check_password_hash

def compare_password(plain_password:str, hashed: bytes) -> bool:
    return check_password_hash(hashed, plain_password) # Hash has to be the first argument