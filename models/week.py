from extensions import db

class Week(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    week = db.Column(db.Integer, nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'year': self.year,
            'week': self.week
        }