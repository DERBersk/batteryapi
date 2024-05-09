from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    created_date = db.Column(db.Date)
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'created_date': self.created_date,
        }