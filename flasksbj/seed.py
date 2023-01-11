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
import sqlalchemy
from sqlalchemy import select, join
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from flask import jsonify


engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo =True)

Sesson = sessionmaker(bind = engine)
session = Sesson()




from sbj.src.models.card import Card
from sbj.src.models.deck import Deck
from sbj.src.models.deckcard import DeckCard,deck_cards_table
from sbj.src.models.game import Game
from sbj.src.models.hand import Hand, dbHand

from sbj.src.models.result import Result
from sbj.src.models.player import Player
from sbj.src.models.handcards import hand_cards_table
from sbj.src.models.gamedeck import game_deck_table
from sbj.src.models.game_results import game_results_table
from sbj.src.models.gameplayers import game_players_table
from sbj.src.models.players_hand import players_hand_table
from sbj.app import create_app



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

    session.execute(game_players_table.delete())
    session.execute(game_deck_table.delete())
    session.execute(hand_cards_table.delete())
    session.execute(deck_cards_table.delete())
    # session.execute(game_results_table.delete())

    handstmt = text("TRUNCATE TABLE hands CASCADE")
    session.execute(handstmt)


    # resultstmt = text("TRUNCATE TABLE results")
    # session.execute(resultstmt)


    deckstmt = text ("TRUNCATE TABLE decks CASCADE")
    session.execute(deckstmt)

    gamestmt = text("TRUNCATE TABLE games CASCADE")
    session.execute(gamestmt)

    cardstmt = text("TRUNCATE TABLE cards CASCADE")
    session.execute(cardstmt)

    playstmt = text("TRUNCATE TABLE players CASCADE")
    session.execute(playstmt)

    session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    session.begin()
    truncate_tables()
    fake = Faker()



    with open('./data.json') as cards_file:
            cards = json.load(cards_file)

            for card in cards['deck']:

                    if card['name'][0]=='D':
                        newCard = Card(card['name'], 'Diamonds', max(card['value']),min(card['value']),card['url'])
                    elif card['name'][0]=='C':
                        newCard=Card(card['name'], 'Clubs', max(card['value']),min(card['value']),card['url'])
                    elif card['name'][0]=='H':
                        newCard=Card(card['name'], 'Hearts', max(card['value']),min(card['value']),card['url'])
                    elif card['name'][0]=='S':
                        newCard=Card(card['name'], 'Spades', max(card['value']),min(card['value']),card['url'])

                    session.add(newCard)

            session.commit()
            # ADD PLAYERS
            player1 = Player(
                name="dealer",

            )
            player1.change_limit(17)
            player2 = Player(
                name="test_player"
            )
            session.add(player1)
            session.commit()
            session.add(player2)
            session.commit()

    print(player1.id, player1.name);

    print(player2.id, player1.name)
    players = {
        "dealer": player1,
        "player": player2
    }


    game_init = Game(players=players)



    session.add(game_init)



    deck_init = Deck()

    print(str(deck_init.created_at), deck_init.id)
    session.add(deck_init)
    session.commit()



    # GAMEDECK
    print ("Deck: ", deck_init.serialize())
    print ("Game: ", game_init.serialize())
    deckid = deck_init.id
    gameid = game_init.id
    if deckid != None and gameid != None:
        print("************DECKID:", deckid)
        print("************GAMEID:", gameid)
        gamedeckstmt= sqlalchemy.insert(game_deck_table).values(game_id=gameid, deck_id=deckid)

    session.execute(gamedeckstmt)


    # GAME PLAYERS

    gameplayersstmt = sqlalchemy.insert(game_players_table).values(game_id=gameid, player_id=game_init.player_id)
    session.execute(gameplayersstmt)
    gamedealerstmt = sqlalchemy.insert(game_players_table).values(game_id=gameid, player_id = game_init.dealer_id)
    session.execute(gamedealerstmt)

    # TEST DECK CARDS
    cards = session.query(Card).all()
    deckcardsToupload = []
    for card in cards:
            a = {
                    "deck_id": deckid,
                    "card_id": card.id
            }
            deckcardsstmt = sqlalchemy.insert(deck_cards_table).values(
                deck_id=deckid, card_id=card.id)
            session.execute(deckcardsstmt)

    # INITIATE HANDS
    player1.change_limit(17)
    player1.initHand()
    session.add(player1.hand)

    player2.initHand()
    session.add(player2.hand)
    session.commit()

    playerhandsstmt_dealer = sqlalchemy.insert(players_hand_table).values(
        player_id=player1.id, hand_id=player1.hand.id
    )
    session.execute(playerhandsstmt_dealer)
    playerhandsstmt_player = sqlalchemy.insert(players_hand_table).values(
        player_id=player2.id, hand_id=player2.hand.id
    )
    session.execute(playerhandsstmt_player)

    session.commit()

    print(player1.hand.serialize())



    # ADD TO HAND
    # pull gamedeck
    # pull deckcards
    # sort and pull 2 random cards
    # add to hand method
    print("\n\n*************** DECK ID:", deckid)
    gamedeckstmt2 = sqlalchemy.select(game_deck_table).where(game_deck_table.c.game_id==gameid)
    deckies =session.execute(gamedeckstmt2)
    deckies_rt = None
    for dcs in deckies:

            deckies_rt = {
                "deck.id": dcs['deck_id'],
                "game.id": dcs['game_id'],

            }
            deckid = dcs['deck_id']


    print("\n\n", deckies_rt)
    j = deck_cards_table.join(Card)
    deckcardsstmt22 = select([deck_cards_table, Card]).select_from(
        j).filter(deck_cards_table.c.deck_id == deckid)
    # deckcardsstmt22 = sqlalchemy.select(deck_cards_table).where(deck_cards_table.c.deck_id==deckid)
    deckies_part2 = session.execute(deckcardsstmt22)
    deckies_rt2 = []
    print(deckies_part2)
    for deckie in deckies_part2:
            c = deckie['Card']
            c.serialize()
            print(c.serialize())

            a = {
                "deck.id": int(deckie['deck_id']),
                "card":c.serialize(),
                'used': deckie['used']
            }
            p = DeckCard(card=c, deck_id=deckie['deck_id'], used=deckie['used'])
            print(p.serialize())
            deckies_rt2.append(p)

    print("\n\n*******deckies Part 2: ", deckies_rt2)
    # SET GAME DECK
    game_init.setDeck(deckies_rt2)
    game_init.sortDeck()
    print(game_init.serialize())
    game_init.play_game()

    print(game_init.serialize())

    dealt_cards_dealer = game_init.deal_from_deck(2)
    update_cards_dealer = []
    for cd in dealt_cards_dealer:
            print(cd.serialize())
            a = {
                "deck_id": cd.deck_id,
                "card_id": cd.id,
                "used": cd.used

            }
            print(a)

            updateStmt = sqlalchemy.update(deck_cards_table).where(
                deck_cards_table.c.deck_id==cd.deck_id, deck_cards_table.c.card_id==cd.id).values(
                deck_id=cd.deck_id, card_id=cd.id, used=cd.used
            )

            session.execute(updateStmt)

            insertStmt = sqlalchemy.insert(hand_cards_table).values(
                hand_id=game_init.dealer.hand.id, card_id=cd.id
            )
            session.execute(insertStmt)
    player1.add_to_hand(dealt_cards_dealer)
    # update hand
    player1.hand
    updatehandStmt = session.update()

    session.commit()





    # HAND to dealer
    player1.add_to_hand(dealt_cards_dealer)


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
# test_deck = Deck()
# run script
main()
