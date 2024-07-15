# import external packages
from flask import Blueprint,jsonify,request
# import functions and data
from extensions import db
# import models
from models.options import Options
from models.options import StrategyEnum

options_bp = Blueprint('options', __name__, url_prefix='/api/options')

###################################################
# One Route to get and post data to and from the 
# overall Options table
###################################################
@options_bp.route('/strategies/', methods=['GET', 'POST'])
def options_strategies():
    options = Options.query.first()
    
    if request.method == 'POST':
        strategy_name = request.json.get('strategy')
        if strategy_name in StrategyEnum.__members__:
            options.strategy = StrategyEnum[strategy_name]
            db.session.commit()
            return jsonify({'message': 'Options updated successfully'})
        else:
            return jsonify({'error': 'Invalid strategy name'}), 400
    else:
        return jsonify({'strategy': options.strategy.value})
    
###################################################
# One Route to get and post data to and from the 
# overall Options table (excluding strategy)
###################################################
@options_bp.route('/weights/', methods=['GET', 'POST'])
def options_weights():
    options = Options.query.first()
    
    if request.method == 'POST':
        data = request.json
        
        # Update other fields
        if 'overall_risk_weight_risk' in data:
            options.overall_risk_weight_risk = data['overall_risk_weight_risk']
        if 'overall_risk_weight_sustainability' in data:
            options.overall_risk_weight_sustainability = data['overall_risk_weight_sustainability']
        if 'risk_index_weight_country_risk' in data:
            options.risk_index_weight_country_risk = data['risk_index_weight_country_risk']
        if 'risk_index_weight_reliability' in data:
            options.risk_index_weight_reliability = data['risk_index_weight_reliability']
        
        db.session.commit()
        return jsonify({'message': 'Options updated successfully'})
    
    else:
        return jsonify({
            'overall_risk_weight_risk': options.overall_risk_weight_risk,
            'overall_risk_weight_sustainability': options.overall_risk_weight_sustainability,
            'risk_index_weight_country_risk': options.risk_index_weight_country_risk,
            'risk_index_weight_reliability': options.risk_index_weight_reliability
        })
