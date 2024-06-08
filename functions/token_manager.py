# import external packages
import uuid
from collections import defaultdict

tokens = {}

def generate_token(email, expiration_time,id):
    token = str(uuid.uuid4())
    tokens[token] = {'email': email, 'expiration_time': expiration_time, 'id': id}
    return token