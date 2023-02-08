import bcrypt


def hash_password(password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return password_hash.decode()


def check_password(password, password_hash):
    if bcrypt.checkpw(password.encode(), password_hash):
        return True
    else:
        return False