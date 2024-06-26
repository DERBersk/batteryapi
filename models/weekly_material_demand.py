import datetime
from extensions import db
from models.week import Week
from models.material import Material

class WeeklyMaterialDemand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    week_id = db.Column(db.String(10), db.ForeignKey('week.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    def serialize(self):
        week = Week.query.filter(Week.id == self.week_id).first()
        material = Material.query.filter(Material.id == self.material_id).first()
        
        return {
            'id': self.id,
            'material_id': self.material_id,
            'week': week.week,
            'year': week.year,
            'amount': self.amount,
            'unit': material.unit
        }
    
    def is_later_or_equal(self):
        week = Week.query.filter(Week.id == self.week_id).first()
        current_year, current_week = datetime.datetime.now().isocalendar()[:2]
        if week.year > current_year:
            return True
        elif week.year == current_year:
            return week.week >= current_week
        return False
    
    def is_in_lead_time(self, lead_time_end_date):
        week = Week.query.filter(Week.id == self.week_id).first()
        week_start_date = datetime.date(week.year, 1, 1) + datetime.timedelta(weeks=week.week) + datetime.timedelta(weeks=-2)
        return week_start_date <= lead_time_end_date