import sqlalchemy
from flask import Blueprint, jsonify, abort, request
from ..models import Game, GameStatus

bp = Blueprint('games', __name__, url_prefix='/games')


@bp.route('', methods=['GET'])
def index():
        games = Game.query.all()
        result = []
        for game in games:
                result.append(game.serialize())
        if len(games)== 0:
            return jsonify(False,{'message':'No games yet, Sorry'})
        return jsonify(result)



@bp.route('create_game', methods=['POST'])
def create():
        if 'players' not in request.json:
              return abort(400,'players not in request json')
        new_game = Game()
