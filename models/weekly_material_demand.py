from extensions import db

class WeeklyMaterialDemand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    week = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'material_id': self.material_id,
            'year': self.year,
            'week': self.week,
            'amount': self.amount
        }