from flask import Flask
from extensions import db

def create_app():
    app = Flask(__name__.split(".")[0])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    # Import routes
    from routes.supplier_routes import supplier_bp
    from routes.product_routes import product_bp
    from routes.project_routes import project_bp
    from routes.materials_routes import material_bp
    from routes.products_per_project_routes import products_per_project_bp
    from routes.materials_per_product_routes import materials_per_product_bp
    from routes.materials_per_supplier_routes import materials_per_supplier_bp

    # Register blueprints
    app.register_blueprint(supplier_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(material_bp)
    app.register_blueprint(products_per_project_bp)
    app.register_blueprint(materials_per_product_bp)
    app.register_blueprint(materials_per_supplier_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0')