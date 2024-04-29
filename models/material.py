from extensions import db

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    main_supplier = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    safety_stock = db.Column(db.Integer)
    lot_size = db.Column(db.Integer)