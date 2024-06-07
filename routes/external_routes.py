from datetime import datetime,timedelta
from flask import Blueprint, request,render_template,current_app,flash
from functions.email import send_email
from functions.token_manager import generate_token,tokens
import json
from extensions import db
from models.supplier import Supplier
from models.materials_per_supplier import MaterialsPerSupplier
from models.material import Material

external_bp = Blueprint('external', __name__, url_prefix='/api/external')

# Load configuration from a JSON file
with open('config.json', 'r') as file:
    config = json.load(file)

@external_bp.route('/generate_link/<int:supplier_id>',methods=["POST"])
def generate_link(supplier_id):
    supplier = Supplier.query.filter(Supplier.id == supplier_id).first()
    if supplier:
        email = supplier.email #This email should be the email of the supplier
        expiration_time = datetime.now() + timedelta(days=7)  # Change this to whatever expiration time you want
        token = generate_token(email, expiration_time, supplier.id)
        link = request.host_url + 'api/external/update_data/' + token

        # Render link.html content
        with current_app.app_context():
            html_content = render_template('link.html', link=link, company_name=config['COMPANY_NAME'])

        # Send email
        subject = 'Update Your Supplier Data'
        send_email(email, subject, html_content)

        return 'Link sent to {}'.format(email)
    return "Failed"

@external_bp.route('/update_data/<token>', methods=["GET", "POST"])
def update_data(token):
    if token in tokens:
        supplier_data = tokens[token]
        if datetime.now() < supplier_data['expiration_time']:
            supplier = Supplier.query.filter(Supplier.id == supplier_data['id']).first()
            if not supplier:
                return 'Invalid supplier.'

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

                        if lead_time is not None:
                            material_per_supplier.lead_time = lead_time
                        if co2_emissions is not None:
                            material_per_supplier.co2_emissions = co2_emissions

                    # Commit changes to the database
                    db.session.commit()

                return 'Data updated successfully!'

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
                    'co2_emissions': material_per_supplier.co2_emissions
                })

            # Render the form with existing supplier data and materials
            return render_template('update_form.html', supplier=supplier, materials=materials_data)
        else:
            return 'Link has expired.'
    else:
        return 'Invalid link.'