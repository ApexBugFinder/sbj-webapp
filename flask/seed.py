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
from sbj.src.models import *
from sbj.src import create_app



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
    Deck.query.delete()
    Game.query.delete()
    db.session.execute(game_deck_table.delete())
    Card.query.delete()
    db.session.execute(deck_cards_table.delete())

    Hand.query.delete()
    db.session.execute(hand_cards_table.delete())

    Result.query.delete()
    Player.query.delete()
    # db.session.execute(likes_table.delete())
    # Tweet.query.delete()
    # User.query.delete()
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
