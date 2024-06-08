from extensions import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    amount = db.Column(db.Float)
    planned_delivery_date = db.Column(db.Date, nullable = True)
    delivery_date = db.Column(db.Date, nullable = True)
        
    def serialize(self):
        return {
            'id': self.id,
            'material_id': self.material_id,
            'supplier_id': self.supplier_id,
            'amount': self.amount,
            'planned_delivery_date': self.planned_delivery_date,
            'delivery_date': self.delivery_date
        }
    
    def is_punctual(self):
        if self.delivery_date and self.planned_delivery_date:
            return self.delivery_date <= self.planned_delivery_date
        return False