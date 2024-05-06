from extensions import db

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    risk_index = db.Column(db.Float, nullable=True)
    sustainability_index = db.Column(db.Float, nullable=True)
    quality = db.Column(db.Float, nullable=True)
    reliability = db.Column(db.Float, nullable=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'long': self.long,
            'risk_index': self.risk_index,
            'sustainability_index':self.sustainability_index,
            'quality':self.quality,
            'reliability':self.reliability,
        }
