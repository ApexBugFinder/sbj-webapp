from flask import Blueprint, jsonify, abort, request
from ..models import *

bp = Blueprint('cards', __name__, url_prefix='/cards')


@bp.route('', methods=['GET'])
def index():
          cards = Card.query.all()
          result = []
          for card in cards:
                    result.append(card.serialize())
          return jsonify(result)


@bp.route('/', methods=['POST'])
def create():
          if 'face' not in request.json or 'suite'not in request.json or 'url' not in request.json:
                  return abort(400)

          c = Card(
            face=request.json['face'],
            h_value=request.json['h_value'],
            l_value=request.json['l_value'],
            suite=request.json['suite'],
            url=request.json['url']
          )
          db.session.add(c)
          db.session.commit()
          return jsonify(c.serialize())

@bp.route('/<int:id>', methods=['GET'])
def show_by_id(id:int):
        c = Card.query.get_or_404(id)

        return jsonify(c.serialize())

@bp.route('/<int:id>', methods=['PUT'])
def updateCard(id:int):
        c = Card.query.get_or_404(id)
        if 'face' in request.json:
            c.face = request.json['face']
        if 'suite' in request.json:
            c.suite = request.json['suite']
        if 'h_value' in request.json:
            c.h_value = request.json['h_value']
        if 'l_value' in request.json:
            c.l_value = request.json['l_value']
        if 'url' in request.json:
            c.url = request.json['url']
        try:
                db.session.add(c)
                db.session.commit()
                return jsonify(c.serialize())
        except:
                return jsonify(False)

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
      c = Card.query.get_or_404(id)
      try:
            db.session.delete(c)
            db.session.commit()
            return jsonify(True)
      except:
            return jsonify(False)


