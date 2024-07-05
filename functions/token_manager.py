# import external packages
import uuid

tokens = {}

def generate_token(email, expiration_time,id):
    token = str(uuid.uuid4())
    tokens[token] = {'email': email, 'expiration_time': expiration_time, 'id': id}
    return token