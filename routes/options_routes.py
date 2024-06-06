from flask import Blueprint,jsonify,request
from models.options import Options
from models.options import StrategyEnum
from extensions import db

options_bp = Blueprint('options', __name__, url_prefix='/api/options')

@options_bp.route('/', methods=['GET', 'POST'])
def options():
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
