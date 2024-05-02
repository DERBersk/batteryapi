from extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }