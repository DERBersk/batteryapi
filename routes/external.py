from datetime import datetime,timedelta
from flask import Blueprint, request,render_template,current_app
from link_generate_concept.email import send_email
from link_generate_concept.token_manager import generate_token,tokens
from models.supplier import Supplier

external_bp = Blueprint('external', __name__, url_prefix='/api/external')

@external_bp.route('/generate_link/<int:supplier_id>',methods=["POST"])
def generate_link(supplier_id):
    print("HERE")
    supplier = Supplier.query.filter(Supplier.id == supplier_id).first()
    if supplier:
        email = 'dominikeitner@gmail.com' #This email should be the email of the supplier
        expiration_time = datetime.now() + timedelta(days=1)  # Change this to whatever expiration time you want
        token = generate_token(email, expiration_time)
        link = request.host_url + 'api/external/update_data/' + token

        # Render link.html content
        with current_app.app_context():
            html_content = render_template('link.html', link=link)

        # Send email
        subject = 'Update Your Supplier Data'
        send_email(email, subject, html_content)

        return 'Link sent to {}'.format(email)
    return "Failed"

@external_bp.route('/update_data/<token>',methods=["GET","POST"])
def update_data(token):
    if token in tokens:
        supplier_data = tokens[token]
        if datetime.now() < supplier_data['expiration_time']:
            if request.method == 'POST':
                # Update supplier data here
                # For example, you can access form data using request.form
                return 'Data updated successfully!'
            else:
                return render_template('update_form.html')
        else:
            return 'Link has expired.'
    else:
        return 'Invalid link.'