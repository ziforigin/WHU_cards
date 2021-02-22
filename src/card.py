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
