"""
Populate twitter database with fake data using the SQLAlchemy ORM.
"""
import json
from datetime import date
import random
import string
import hashlib
import secrets
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


from sbj.src.models.card import Card
from sbj.src.models.deck import Deck
from sbj.src.models.deckcard import DeckCard,deck_cards_table
from sbj.src.models.game import Game
from sbj.src.models.hand import Hand

from sbj.src.models.result import Result
from sbj.src.models.player import Player
from sbj.src.models.handcards import hand_cards_table
from sbj.src.dbObjects.gamedeck import game_deck_table
from sbj.src.models.game_results import game_results_table
from sbj.src.models.gameplayers import game_players_table
from sbj import create_app



USER_COUNT = 50
TWEET_COUNT = 100
LIKE_COUNT = 400

assert LIKE_COUNT <= (USER_COUNT * TWEET_COUNT)




def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&', # valid pw characters
            k=random.randint(8, 15) # length of pw
        )
    )

    salt = secrets.token_hex(16)

    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


def truncate_tables():
    """Delete all rows from database tables"""

    db.session.execute(game_players_table.delete())
    db.session.execute(game_deck_table.delete())
    db.session.execute(hand_cards_table.delete())
    db.session.execute(deck_cards_table.delete())
    db.session.execute(game_results_table.delete())

    Hand.query.delete()


    Result.query.delete()


    Deck.query.delete()
    Game.query.delete()
    Card.query.delete()
    Player.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()


    with open('./data.json') as cards_file:
            cards = json.load(cards_file)
            for card in cards['deck']:
                    cards_to_upload = []
                    if card['name'][0]=='D':
                        newCard = Card(card['name'], 'Diamonds', max(card['value']),min(card['value']),card['url'])
                    elif card['name'][0]=='C':
                        newCard=Card(card['name'], 'Clubs', max(card['value']),min(card['value']),card['url'])
                    elif card['name'][0]=='H':
                        newCard=Card(card['name'], 'Hearts', max(card['value']),min(card['value']),card['url'])
                    elif card['name'][0]=='S':
                        newCard=Card(card['name'], 'Spades', max(card['value']),min(card['value']),card['url'])
                    db.session.add(newCard)

            db.session.commit()
            # ADD PLAYERS
            player1 = Player(
                name="dealer"
            )
            player1.se
            player2 = Player(
                name="test_player"
            )
            db.session.add(player1)
            db.session.commit()
            db.session.add(player2)
            db.session.commit()
    deck_init = Deck()

    print(str(deck_init.created_at), deck_init.id)
    db.session.add(deck_init)
    db.session.commit()
    print (deck_init.serialize())


    # last_user = None  # save last user
    # for _ in range(USER_COUNT):
    #     last_user = User(
    #         username=fake.unique.first_name().lower() + str(random.randint(1,150)),
    #         password=random_passhash()
    #     )
    #     db.session.add(last_user)

    # insert users
    # db.session.commit()

    # last_tweet = None  # save last tweet
    # for _ in range(TWEET_COUNT):
    #     last_tweet = Tweet(
    #         content=fake.sentence(),
    #         user_id=random.randint(last_user.id - USER_COUNT + 1, last_user.id)
    #     )
    #     db.session.add(last_tweet)

    # insert tweets
    # db.session.commit()

    # user_tweet_pairs = set()
    # while len(user_tweet_pairs) < LIKE_COUNT:

    #     candidate = (
    #         random.randint(last_user.id - USER_COUNT + 1, last_user.id),
    #         random.randint(last_tweet.id - TWEET_COUNT + 1, last_tweet.id)
    #     )

    #     if candidate in user_tweet_pairs:
    #         continue  # pairs must be unique

    #     user_tweet_pairs.add(candidate)

    # new_likes = [{"user_id": pair[0], "tweet_id": pair[1]} for pair in list(user_tweet_pairs)]
    # insert_likes_query = likes_table.insert().values(new_likes)
    # db.session.execute(insert_likes_query)

    # # insert likes
    # db.session.commit()

# create test deck
test_deck = Deck()
# run script
main()