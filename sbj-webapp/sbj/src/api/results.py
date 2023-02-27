from flask import Blueprint, jsonify, abort, request
from flask_cors import CORS
bp = Blueprint('results', __name__, url_prefix='/api/results')
CORS(bp)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo=True)

Sesson = sessionmaker(bind=engine)
session = Sesson()


# POST WINNING
@bp.route('/win', methods=['POST'])
def win():
      try:

            jsonify(True)
      except:

            jsonify(False)
# POST LOSING
@bp.route('/lose', methods=['POST'])
def lose():
      try:

            jsonify(True)
      except:

            jsonify(False)
# POST DRAW
@bp.route('/draw', methods=['POST'])
def draw():
        try:

                  jsonify(True)
        except:

                  jsonify(False)


# GET RESULTS
@bp.route('/<int:id>',methods=['GET'])
def get_result():
      try:

            jsonify(True)
      except:

            jsonify(False)
