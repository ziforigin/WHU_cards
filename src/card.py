class Card:
    name: str = None
    image_url: str = None
    card_type: str = None

    def __init__(self, name, image_url, card_type):
        self.name: str = name
        self.image_url: str = image_url
        self.card_type: str = card_type

    def to_dict(self):
        return dict(
            name=self.name,
            image_url=self.image_url,
            card_type=self.card_type
        )

    @classmethod
    def decode_from_json(cls, json_data: dict):
        return cls(**json_data)

    @classmethod
    def decode_from_dict(cls, dict_data: dict):
        return cls(**dict_data)


class Deck:
    __deck__ = True
    name: str = None
    cards: list = list()

    def __init__(self, name, cards):
        self.name = Deck.edit_deck_name(name)
        self.cards = cards

    def remove_card(self, card_name):
        for card in self.cards:
            if card.name == card_name:
                self.cards.remove(card)

    def is_card_in_deck(self, card):
        for every_card in self.cards:
            if every_card.name == card.name:
                return True

    def add_card(self, card: Card):
        if not self.is_card_in_deck(card):
            self.cards.append(card)

    def to_dict(self):
        list_of_card = list()
        for card in self.cards:
            list_of_card.append(card.to_dict())
        return dict(
            name=self.name,
            cards=list_of_card
        )

    @classmethod
    def decode_from_json(cls, name: str, json_data: dict):
        cards = list(map(Card.decode_from_json, json_data["cards"]))
        return cls(name, cards)

    @classmethod
    def decode_from_dict(cls, name: str, dict_data: dict):
        cards = list(map(Card.decode_from_dict, dict_data["cards"]))
        return cls(name, cards)

    @classmethod
    def edit_deck_name(cls, deck_name):
        if len(deck_name) > 25:
            result_deck_name = deck_name[0:24]
        else:
            result_deck_name = deck_name
        return result_deck_name
