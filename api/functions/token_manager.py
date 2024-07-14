# import external packages
import uuid
from extensions import db
from models.external_token import Token
import secrets

def generate_token(expiration_time,id):
    token = secrets.token_hex(16)
    new_token = Token(token=token, supplier_id=id, expires_at=expiration_time)
    db.session.add(new_token)
    db.session.commit()
    return token