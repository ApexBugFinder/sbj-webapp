from . import Card
class DeckCard(Card):
      def __init__(self, card:Card, deck_id:str):

          self.id = card.id
          self.face = card.face
          self.suite = card.suite
          self.value = None
          self.h_value = card.h_value
          self.l_value = card.l_value
          self.url = card.url
          self.possible_values = (self.h_value, self.l_value)
          self.deck_id = deck_id

      def serialize(self):
           return {
                        'id': self.id,
                        'deck_id': self.deck_id,
                        'face': self.face,
                        'suite': self.suite,
                        'h_value': self.h_value,
                        'l_value': self.l_value,
                        'value': self.value,
                        'url': self.url
           }

      def serialize_deck(self, array: list):
              apple = ''
              for deckc in array:
                    apple += '{\n'+deckc.serialize() + '\n},\n'
              return {
                  apple
              }
