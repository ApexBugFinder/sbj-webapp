import datetime
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()


# CORE TABLES
from .card import Card
from .player import Player
from .deck import Deck
from .game import *
from .hand import *
from .result import Result
# JOIN TABLES
from .players_hand import players_hand_table
from .deckcard import deck_cards_table, DeckCard
from .gamedeck import  game_deck_table
from .gameplayers import game_players_table
from .handcards import hand_cards_table




# from .result import Result



