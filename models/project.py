import datetime 

from extensions import db

from models.week import Week
from models.products_per_project import ProductsPerProject

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner = db.Column(db.String(100), nullable=False)
    start_week = db.Column(db.String(10), db.ForeignKey('week.id'), nullable=False)
    end_week =  db.Column(db.String(10), db.ForeignKey('week.id'), nullable=False)
    
    def serialize(self):
        startweek = Week.query.filter(Week.id == self.start_week).first()
        endweek = Week.query.filter(Week.id == self.end_week).first()
        
        product_count = ProductsPerProject.query.filter(ProductsPerProject.project_id == self.id).count()
        
        return {
            'id': self.id,
            'partner': self.partner,
            'start_week': startweek.week,
            'start_year': startweek.year,
            'end_week': endweek.week,
            'end_year': endweek.year,
            'product_count': product_count
        }
        
    def check_project_week(self):
        start_week = Week.query.filter(Week.id == self.start_week).first()
        end_week = Week.query.filter(Week.id == self.end_week).first()
        check_year, check_week = datetime.datetime.now().isocalendar()[:2]
        if check_year < start_week.year or (check_year == start_week.year and check_week < start_week.week):
            return True
        elif check_year > end_week.year or (check_year == end_week.year and check_week > end_week.week):
            return False
        else:
            return True
        
    def check_project_week_past_year(self):
        start_week = Week.query.filter(Week.id == self.start_week).first()
        end_week = Week.query.filter(Week.id == self.end_week).first()
        one_year_ago = datetime.datetime.now()-datetime.timedelta(days=365)
        check_year, check_week = one_year_ago.isocalendar()[:2]
        if check_year < start_week.year or (check_year == start_week.year and check_week < start_week.week):
            return True
        elif check_year > end_week.year or (check_year == end_week.year and check_week > end_week.week):
            return False
        else:
            return True
