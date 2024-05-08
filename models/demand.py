from extensions import db

class Demand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    time_slot = db.Column(db.Integer, db.ForeignKey('time.id'), nullable=False)
    order_count = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    
    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'time_slot': self.time_slot,
            'order_count': self.order_count,
            'amount': self.amount
        }
