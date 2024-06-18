from extensions import db
from models.options import StrategyEnum

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    safety_stock = db.Column(db.Float)
    lot_size = db.Column(db.Float)
    stock_level = db.Column(db.Float)
    strategy = db.Column(db.Enum(StrategyEnum), nullable=False, default=StrategyEnum.NONE)
    unit = db.Column(db.String(50))
    external_id = db.Column(db.String(20), nullable=True)
        
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'safety_stock': self.safety_stock,
            'lot_size': self.lot_size,
            'stock_level': self.stock_level,
            'strategy': self.strategy.name if self.strategy else None,
            'unit': self.unit,
            'external_id': self.external_id,
        }