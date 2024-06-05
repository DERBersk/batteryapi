from extensions import db
from models.week import Week

class WeeklyMaterialDemand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    week_id = db.Column(db.String(10), db.ForeignKey('week.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    def serialize(self):
        week = Week.query.filter(Week.id == self.week_id).first()
        
        return {
            'id': self.id,
            'material_id': self.material_id,
            'week': week.week,
            'year': week.year,
            'amount': self.amount
        }