from extensions import db

class MaterialsPerSupplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    transportation_cost = db.Column(db.Float, nullable=False)
    delivery_time = db.Column(db.Integer, nullable=False)
    min_amount = db.Column(db.Integer, nullable=False)