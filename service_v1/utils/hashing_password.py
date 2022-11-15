from hashlib import sha384

def hashing (password : str) -> str :

    password_encode = password.encode("utf-8")

    return sha384(password_encode).hexdigest()