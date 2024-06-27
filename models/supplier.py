from extensions import db

from models.material import Material
from models.materials_per_supplier import MaterialsPerSupplier
from models.order import Order

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    risk_index = db.Column(db.Float, nullable=True)
    sustainability_index = db.Column(db.Float, nullable=True)
    quality = db.Column(db.Float, nullable=True)
    reliability = db.Column(db.Float, nullable=True)
    availability = db.Column(db.Boolean, nullable=True)
    country = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    external_id = db.Column(db.String(20), nullable=True)
    
    def serialize(self):
        mat_count = Material.query.join(MaterialsPerSupplier)\
                                  .join(Supplier)\
                                  .filter(MaterialsPerSupplier.supplier_id==self.id)\
                                  .filter(Material.id==MaterialsPerSupplier.material_id)\
                                  .add_columns(Material.id,Material.name,Material.safety_stock,Material.lot_size,Material.stock_level,MaterialsPerSupplier.lead_time, Material.unit)\
                                  .count()
        
        ord_count = Order.query.filter(Order.delivery_date.is_(None)).filter(Order.supplier_id == self.id).count()
        
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'long': self.long,
            'risk_index': self.risk_index,
            'sustainability_index':self.sustainability_index,
            'quality':self.quality,
            'reliability':self.reliability, # Reliability = Compliance
            'availability':self.availability,
            'country':self.country,
            'email': self.email,
            'external_id': self.external_id,
            'mat_count': mat_count,
            'order_count': ord_count
        }
