# import functions and data
from extensions import db


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    supplier = db.relationship('Supplier')