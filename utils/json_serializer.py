import json
from objects.card import Card, Deck


class JsonEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, Card):
            return {
                    'name': object.name,
                    'image_url': object.image_url,
                    'card_type': object.card_type
                    }

        if isinstance(object, Deck):
            return {
                    'name': object.name,
                    'cards': object.cards
                    }

        return {'__{}__'.format(object.__class__.__name__): object.__dict__}
