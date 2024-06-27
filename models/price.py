from extensions import db
from models.material import Material

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    cost = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    def serialize(self):
        material = Material.query.filter(Material.id == self.material_id).first()
        
        return {
            'id': self.id,
            'material_id': self.material_id,
            'supplier_id': self.supplier_id,
            'cost': self.cost,
            'unit': material.unit.name if material.unit else None,
            'start_date': self.start_date,
            'end_date': self.end_date
        }