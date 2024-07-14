# import external packages
import datetime
# import functions and data
from extensions import db

class MaterialsPerSupplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    lead_time = db.Column(db.Integer)
    co2_emissions = db.Column(db.Float, nullable = True)
    distance = db.Column(db.Float, nullable = True)
    
    def serialize(self):
        return {
            'id': self.id,
            'material_id': self.material_id,
            'supplier_id': self.supplier_id,
            'lead_time': self.lead_time,
            'co2_emissions': self.co2_emissions,
            'distance': self.distance
        }