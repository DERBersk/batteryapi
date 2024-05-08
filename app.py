from flask import Flask
from extensions import db

#TODO: Historical Demand Routes
#TODO: Analytics Routes - First Mock then create

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.xheevcowfsiqoblrojtv:TGEBzsP7RGjpVM5E@aws-0-eu-west-2.pooler.supabase.com:5432/postgres'
    # Import routes
    from routes.supplier_routes import supplier_bp
    from routes.product_routes import product_bp
    from routes.project_routes import project_bp
    from routes.materials_routes import material_bp
    from routes.create_test_data_routes import test_data_bp
    from routes.price_routes import price_bp

    # Register blueprints
    app.register_blueprint(supplier_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(material_bp)
    app.register_blueprint(test_data_bp)
    app.register_blueprint(price_bp)
    
    return app

app = create_app()
db.init_app(app)
with app.app_context():
    db.create_all()
# app.run(debug=True, host='0.0.0.0')
if __name__ == "__main__":
    app.run(debug=True)