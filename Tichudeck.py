class Deck:
    def __init__(self, card, color, name, cardId):
        self.card = card
        self.color = color
        self.name = name
        self.id = cardId
        self.res = [0,0]
        self.selected = False
        self.y = 0
        self.socketed = [False, -1]
        self.mahjong = 0
        self.pretendedCard = 0.5
