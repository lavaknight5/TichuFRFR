from Tichudeck import Deck
import random
import pygame


#cardSurface = pygame.Surface((cardWidth, cardHeight), pygame.SRCALPHA)
# card = [cardImage, (x, y)]

class Game:
    def __init__(self, id):
        self.hands = []
        self.id = id
        self.canPlay = False
        self.ready = False
        self.pTurn = -1
        self.deck = self.getDeck()
        self.phase = ""

    def isCombination(self, cards):
        length = len(cards)
        cardNum = []
        for card in cards:
            cardNum.append(card.card)
            if (card.card == -2 or card.card == 15) and length > 1:
                return "Unplayable"
            cardNum = sorted(cardNum)
        if length == 1:
            return "HighCard"
        elif length == 2:
            if (cardNum[0] == cardNum[1] or cardNum[0] == 0.5) and cardNum[1] != 1:
                return "Pair"
            else:
                return "Unplayable"
        elif length == 3:
            if cardNum[0] == cardNum[1] == cardNum[2]:
                return "ThreeOfAKind"
            elif cardNum[1] == cardNum[2] and cardNum[0] == 0.5:
                return "ThreeOfAKind"
            else:
                return "Unplayable"
        elif length == 4:
            if cardNum[0] == cardNum[1] == cardNum[2] == cardNum[3]:
                return "Bomb"
            x = -1
            for i in range(4):
                if cardNum[i] == 0.5:
                    x = i
            if x == -1 and self.isCombination([cardNum[0], cardNum[1]]) == "Pair" and self.isCombination([cardNum[2], cardNum[3]]) == "Pair" and cardNum[1] + 1 == cardNum[2]:
                    return "Steps"
            elif x == 0:
                if self.isCombination([cardNum[0], cardNum[1]]) == "Pair" and self.isCombination([cardNum[2], cardNum[3]]) == "Pair" and cardNum[1] + 1 == cardNum[2]:
                    return "Steps"
                elif self.isCombination([cardNum[1], cardNum[2]]) == "Pair" and cardNum[1] + 1 == cardNum[3]:
                    return "Steps"
                else:
                    return "Unplayable"

        elif length >= 5:
            if (self.isCombination([cardNum[0], cardNum[1]]) == "Pair" and self.isCombination([cardNum[2], cardNum[3], cardNum[4]]) == "ThreeOfAKind") or (self.isCombination([cardNum[3], cardNum[4]]) == "Pair" and self.isCombination([cardNum[0], cardNum[1], cardNum[2]]) == "ThreeOfAKind") or (self.isCombination([cardNum[0], cardNum[4]]) == "Pair" and self.isCombination([cardNum[1], cardNum[2], cardNum[3]]) == "ThreeOfAKind"):
                return "FullHouse"
            elif length % 2 == 1:
                if cardNum[0] != 0.5:
                    for i in range(length - 1):
                        if cardNum[i] + 1 != cardNum[i + 1]:
                            return "Unplayable"
                        return "Straight"
                else:
                    x = 0
                    for i in range(1, length - 1):
                        if cardNum[i] + 1 != cardNum[i + 1]:
                           x += 1
                           if cardNum[i] + 2 != cardNum[i + 2]:
                               return "Unplayable"
                    if x > 1:
                        return "Unplayable"
                    return "Straight"
            elif length % 2 == 0:
                if cardNum[0] != 0.5 or (cardNum[0] == 0.5 and self.isCombination([cardNum[1], cardNum[2]]) != "Pair"):
                    for i in range(0, length, 2):
                        if self.isCombination([cardNum[i], cardNum[i + 1]]) != "Pair":
                            return "Unplayable"
                    for i in range(1, length, 2):
                        if cardNum[i] + 1 != cardNum[i + 1]:
                            return "Unplayable"
                    return "Steps"
                else:
                    templist1 = []
                    templist2 = []
                    x = 0
                    for i in range(1, length):
                        if i % 2 == 0:
                            templist1.append(cardNum[i])
                        else:
                            templist2.append(cardNum[i])
                    for card in templist1:
                        for i in range(len(templist2)):
                            if templist2[i] == card:
                                x += 1
                    if x != len(templist1):
                        return "Unplayable"
                    elif self.isCombination(templist2) != "Straight":
                        return "Unplayable"
                    else:
                        return "Steps"
            else:
                return "Unplayable"

    def shuffle(self, cards):
        hand1 = []
        hand2 = []
        hand3 = []
        hand4 = []
        random.shuffle(cards)
        for i in range(56):
            if i < 14:
                hand1.append(cards[i])
            elif i < 28:
                hand2.append(cards[i])
            elif i < 42:
                hand3.append(cards[i])
            else:
                hand4.append(cards[i])
        return hand1, hand2, hand3, hand4

    def getDeck(self):
        cards = []
        for i in range(1, 5):
            for j in range(1, 14):
                if i == 1:
                    cardId = j
                    color = "Red"
                    card = Deck(j + 1, color, "card", cardId)
                    cards.append(card)

                elif i == 2:
                    cardId = j + 13
                    color = "Green"
                    card = Deck(j + 1, color, "card", cardId)
                    cards.append(card)

                elif i == 3:
                    cardId = j + 26
                    color = "Blue"
                    card = Deck(j + 1, color, "card", cardId)
                    cards.append(card)

                else:
                    cardId = j + 39
                    color = "Black"
                    card = Deck(j + 1, color, "card", cardId)
                    cards.append(card)

        Dragon = Deck(15, "None", "Dragon", 56)
        Phoenix = Deck(0.5, "None", "Phoenix", 55)
        Dogs = Deck(-2, "None", "Dogs", 54)
        MahJong = Deck(1, "None", "MahJong", 53)

        cards.append(MahJong)
        cards.append(Dogs)
        cards.append(Phoenix)
        cards.append(Dragon)
        return cards

    def sendCard(self, card, player1, player2):
        self.hands[player1].pop(card)
        self.hands[player2].append(card)

    def play(self, p1, p2, p3, p4):
        if self.phase == "Giving":
            #p = [card1, card2, card3]
            for i in range(1,4):
                self.sendCard(p1[i-1], 1, i+1)
                self.sendCard(p4[3-i], 4, 4-i)
            self.sendCard(p2[0], 1, 1)
            self.sendCard(p2[2], 1, 3)
            self.sendCard(p2[1], 1, 4)