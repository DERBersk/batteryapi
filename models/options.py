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