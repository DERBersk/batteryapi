from extensions import db

class ProductsPerProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'project_id':self.project_id,
            'amount':self.amount
        }