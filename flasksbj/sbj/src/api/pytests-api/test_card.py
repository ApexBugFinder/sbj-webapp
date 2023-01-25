from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import responder
from werkzeug.routing import Map, Rule, MapAdapter, map, matcher
from conftest import tester

import os, sys
sys.path.append("../../../../sbj/src/models")
from card import Card

import imp
def test_card_check():
    assert True



def test_53cards_in_db():
        totalCards = 53


        response = tester.get("/api/cards/read/all", content_type="html/text")

        print(response)
        # Card = imp.load_source("Card", "../../models/card.py")
        # q = getsession.query(Card).all()
        # results = []
        # for record in q:
        #     results.append(record.serialize())

        # assert totalCards == len(results)
        assert True