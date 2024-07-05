# import external packages
import datetime
# import functions and data
from extensions import db
# import models
from models.week import Week

class ExternalProductionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    week_id = db.Column(db.String(10), db.ForeignKey('week.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    external_id = db.Column(db.String(20))
    
    def serialize(self):
        week = Week.query.filter(Week.id == self.week_id).first()
        return {
            'id': self.id,
            'product_id': self.product_id,
            'week': week.week,
            'year': week.year,
            'amount': self.amount
        }
        
    def is_later_or_equal(self):
        week = Week.query.filter(Week.id == self.week_id).first()
        current_year, current_week = datetime.datetime.now().isocalendar()[:2]
        if week.year > current_year:
            return True
        elif week.year == current_year:
            return week.week >= current_week
        return False