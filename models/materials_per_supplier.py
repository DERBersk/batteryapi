from extensions import db

class MaterialsPerSupplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    min_amount = db.Column(db.Integer)
    max_amount = db.Column(db.Integer)
    lead_time = db.Column(db.Time)
    availability = db.Column(db.Float)
    volume_commitment = db.Column(db.Float)
    
    def serialize(self):
        return {
            'id': self.id,
            'material_id': self.material_id,
            'supplier_id': self.supplier_id,
            'min_amount': self.min_amount,
            'max_amount': self.max_amount,
            'lead_time': self.lead_time,
            'availability': self.availability,
            'volume_commitment': self.volume_commitment
        }
