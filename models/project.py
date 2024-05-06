from extensions import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    production_schedule = db.Column(db.String(10))
    machine_labor_availability = db.Column(db.Float)
    
    def serialize(self):
        return {
            'id': self.id,
            'partner': self.partner,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'production_schedule': self.production_schedule,
            'machine_labor_availability': self.machine_labor_availability
        }