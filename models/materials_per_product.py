from extensions import db

class MaterialsPerProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'material_id': self.material_id,
            'product_id': self.product_id,
            'amount': self.amount
        }