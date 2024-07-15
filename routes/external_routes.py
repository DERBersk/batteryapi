# import external packages
import json
from datetime import datetime,timedelta
from flask import Blueprint, request,render_template,current_app,jsonify
# import functions and data
from functions.email import send_email
from functions.token_manager import generate_token
from functions.fetch_updates import update_or_create_orders, update_or_create_materials
from extensions import db
# import models
from models.supplier import Supplier
from models.materials_per_supplier import MaterialsPerSupplier
from models.material import Material
from models.external_token import Token

external_bp = Blueprint('external', __name__, url_prefix='/api/external')

# Load configuration from a JSON file
with open('config.json', 'r') as file:
    config = json.load(file)
    
###################################################
# Route for calculation of token and sending
# an email with an "Update Data" Link to the 
# supplier
###################################################
@external_bp.route('/generate_link/<int:supplier_id>',methods=["POST"])
def generate_link(supplier_id):
    supplier = Supplier.query.filter(Supplier.id == supplier_id).first()
    if supplier:
        if supplier.email is not None:
            email = supplier.email #This email should be the email of the supplier
        else:
            return jsonify("Email field is empty"),404
        expiration_time = datetime.now() + timedelta(days=7)  # Change this to whatever expiration time you want
        token = generate_token(expiration_time, supplier.id)
        link = request.host_url + 'api/external/update_data/' + token

        # Render link.html content
        with current_app.app_context():
            html_content = render_template('link.html', link=link, company_name=config['COMPANY_NAME'])

        # Send email
        subject = 'Update Your Supplier Data'
        send_email(email, subject, html_content)

        return jsonify('Link sent to {}'.format(email)),200
    return jsonify("Failed"),404

###################################################
# Route for depicting an update-data page to the 
# supplier and the saving process of the given 
# data
###################################################
@external_bp.route('/update_data/<token>', methods=["GET", "POST"])
def update_data(token):
    valid_token = Token.query.filter_by(token=token).first()
    if valid_token:
        supplier_data = valid_token
        if datetime.now() < supplier_data.expires_at:
            supplier = Supplier.query.filter(Supplier.id == supplier_data.supplier_id).first()
            if not supplier:
                return jsonify('Invalid supplier.'),404

            if request.method == 'POST':
                # Retrieve form data
                name = request.form.get('name')
                email = request.form.get('email')

                with db.session.no_autoflush:
                    # Update supplier fields
                    supplier.name = name
                    supplier.email = email

                    # Update materials data
                    materials_per_supplier = MaterialsPerSupplier.query.filter_by(supplier_id=supplier.id).all()
                    for material_per_supplier in materials_per_supplier:
                        material_id = material_per_supplier.material_id
                        lead_time = request.form.get(f'lead_time_{material_id}')
                        co2_emissions = request.form.get(f'co2_emissions_{material_id}')
                        distance = request.form.get(f'distance_{material_id}')

                        if lead_time is not None:
                            material_per_supplier.lead_time = lead_time
                        if co2_emissions is not None:
                            material_per_supplier.co2_emissions = co2_emissions
                        if distance is not None:
                            material_per_supplier.distance = distance

                    # Commit changes to the database
                    db.session.commit()

                return jsonify('Data updated successfully!'),200

            # Query materials associated with the supplier
            materials = db.session.query(Material, MaterialsPerSupplier).\
                        join(MaterialsPerSupplier, Material.id == MaterialsPerSupplier.material_id).\
                        filter(MaterialsPerSupplier.supplier_id == supplier.id).\
                        all()

            # Prepare data for rendering the form
            materials_data = []
            for material, material_per_supplier in materials:
                materials_data.append({
                    'id': material.id,
                    'name': material.name,
                    'lead_time': material_per_supplier.lead_time,
                    'co2_emissions': material_per_supplier.co2_emissions,
                    'distance': material_per_supplier.distance
                })

            # Render the form with existing supplier data and materials
            return render_template('update_form.html', supplier=supplier, materials=materials_data)
        else:
            return jsonify('Link has expired.'),403
    else:
        return jsonify('Invalid link.'),400
    
###################################################
# Route for Fetch and update of orders from WMS
###################################################
@external_bp.route('/orders/',methods=["POST"])
def fetch_and_update_orders():
    return jsonify(update_or_create_orders())

###################################################
# Route for Fetch and update of materials from WMS
###################################################
@external_bp.route('/materials/',methods=["POST"])
def fetch_and_update_materials():
    return jsonify(update_or_create_materials())