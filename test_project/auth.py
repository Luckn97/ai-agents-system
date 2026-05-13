import hashlib

API_KEY = "super-secret"

def create_user(password, roles=[]):

    return hashlib.md5(password.encode()).hexdigest()
