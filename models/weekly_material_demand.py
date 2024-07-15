# import external packages
import datetime
import re
# import functions and data
from extensions import db
# import models
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
            'unit': material.unit.name if material.unit else None
        }
    
    def is_later_or_equal(self):
        week = Week.query.filter(Week.id == self.week_id).first()
        current_year, current_week = datetime.datetime.now().isocalendar()[:2]
        return (week.year > current_year) or (week.year == current_year and week.week >= current_week)

    def is_in_lead_time(self, lead_time_end_date):
        week, year = self.extract_week_and_year(self.week_id)
        week_start_date = datetime.date(year, 1, 1) + datetime.timedelta(weeks=week) + datetime.timedelta(weeks=-2)
        return week_start_date <= lead_time_end_date
    def extract_week_and_year(self,date_str):
        # Define the regular expression pattern to match the format "wk<week>_<year>"
        pattern = r'wk(\d{2})_(\d{4})'
        match = re.match(pattern, date_str)

        if match:
            week = int(match.group(1))
            year = int(match.group(2))
            return week, year
        else:
            raise ValueError("The input string does not match the required format 'wk<week>_<year>'")