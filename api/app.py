import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import external sources
from flask import Flask
import json
from flask_cors import CORS
# import functions and data
from extensions import db, scheduler


def create_app():
    app = Flask(__name__.split(".")[0])
    CORS(app)
    
    with open('config.json', 'r') as file:
        config = json.load(file)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = config["DATABASE"]
    # Import routes
    from routes.supplier_routes import supplier_bp
    from routes.product_routes import product_bp
    from routes.project_routes import project_bp
    from routes.materials_routes import material_bp
    from routes.price_routes import price_bp
    from routes.user_routes import user_bp
    from routes.kpi_routes import kpi_bp
    from routes.external_production_routes import external_production_bp
    from routes.external_routes import external_bp
    from routes.options_routes import options_bp
    # Register blueprints
    app.register_blueprint(supplier_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(material_bp)
    app.register_blueprint(price_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(kpi_bp)
    app.register_blueprint(external_production_bp)
    app.register_blueprint(external_bp)
    app.register_blueprint(options_bp)
    
    return app

app = create_app()
db.init_app(app)
# scheduler.add_job(func=Run, trigger='cron', hour=23, minute=0)
@app.route('/')
def hello():
    return "Hello, World!"
with app.app_context():
    db.create_all()
# app.run(debug=True, host='0.0.0.0')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))