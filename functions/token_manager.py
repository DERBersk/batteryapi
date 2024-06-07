import uuid

tokens = {}

def generate_token(email, expiration_time):
    token = str(uuid.uuid4())
    tokens[token] = {'email': email, 'expiration_time': expiration_time}
    return token