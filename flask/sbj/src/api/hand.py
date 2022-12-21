import sqlalchemy
from flask import Blueprint, jsonify, abort, request
from ..models import Hand

bp = Blueprint('hands', __name__, url_prefix='/hands')

@bp.route('', methods=['GET'])
def index():
        records = Hand.query.all()
        result = []
        for record in records:
                result.append(record.serialize())
        if len(records)== 0:
            return jsonify(False,{'message':'No Hands yet, Sorry'})
        return jsonify(result)



