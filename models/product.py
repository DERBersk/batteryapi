from extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    specification = db.Column(db.String(100))
    external_id = db.Column(db.String(20), nullable=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'specification': self.specification,
            'external_id': self.external_id,
        }