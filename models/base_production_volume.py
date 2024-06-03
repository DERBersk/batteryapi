from extensions import db
import datetime
from sqlalchemy.ext.hybrid import hybrid_property

class BaseProductionVolume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    week = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'year': self.year,
            'week': self.week,
            'amount': self.amount
        }
        
    def is_later_or_equal(self):
        current_year, current_week = datetime.datetime.now().isocalendar()[:2]
        if self.year > current_year:
            return True
        elif self.year == current_year:
            return self.week >= current_week
        return False