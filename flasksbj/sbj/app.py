import os
from flask import Flask
from flask_migrate import Migrate
from datetime import timedelta
from decouple import config
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_mapping(
        FLASK_DEBUG=True,
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=config('DB_URI'),
        # SQLALCHEMY_DATABASE_URI=f'postgresql://postgres:admin123@127.0.0.1:5432/sbj',
        # SQLALCHEMY_DATABASE_URI=str(sqluri),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        NEO4J_URI=os.getenv('NEO4J_URI'),
        NEO4J_USERNAME=os.getenv('NEO4J_USERNAME'),
        NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD'),
        NEO4J_DATABASE=os.getenv('NEO4J_DATABASE'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET'),
        JWT_AUTH_HEADER_PREFIX="Bearer",
        JWT_VERIFY_CLAIMS="signature",
        JWT_EXPIRATION_DELTA=timedelta(360)
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate = Migrate(app, db)
    from sbj.src.api import card
    from sbj.src.api import player

    from sbj.src.api import deck
    from sbj.src.api import game
    from sbj.src.api import deckcards
    from sbj.src.api import hand
    # from src.api import card
    # from src.api import player

    # from src.api import deck
    # from src.api import game
    # from src.api import deckcards
    # from src.api import hand
    # ,hand,card, deck, game, deckcards
    app.register_blueprint(player.bp)
    app.register_blueprint(hand.bp)
    app.register_blueprint(card.bp)
    app.register_blueprint(deck.bp)
    app.register_blueprint(game.bp)
    app.register_blueprint(deckcards.bp)
    return app
