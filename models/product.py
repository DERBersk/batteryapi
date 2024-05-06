from extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    specification = db.Column(db.String(100))
    
    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'specification': self.specification
        }