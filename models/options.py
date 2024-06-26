from extensions import db
from enum import Enum

class StrategyEnum(Enum):
    Sustainability = "Sustainability"
    Risk = "Risk"
    LeadTime = "Lead Time"
    Price = "Price"
    NONE = " "

class Options(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strategy = db.Column(db.Enum(StrategyEnum), nullable=False, default=StrategyEnum.Price)
    overall_risk_weight_risk = db.Column(db.Float)
    overall_risk_weight_sustainability = db.Column(db.Float)
    risk_index_weight_country_risk = db.Column(db.Float)
    risk_index_weight_reliability = db.Column(db.Float)