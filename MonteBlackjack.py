import random
import numpy as np

class BlackJackJackSimulator:
    def __init__(self, numDecks, allowDAS, allowDouble):
        self.numDecks = numDecks
        self.allowDas = allowDAS
        self.allowDouble = allowDouble
        self.runningCount = 0
        self.trueCount = self.calculateTrueCount()

    def calculateRunningCount(self, cardHiLoValue):
        self.runningCount += cardHiLoValue
        self.trueCount = self.calculateTrueCount()

    def calculateTrueCount(self):
        return round(self.runningCount / self.numDecks)

class Deck:
    def __init__(self, numDecks):
        self.cards = []
        self.numDecks = numDecks

    def buildDeck(self):
        for _ in range(self.numDecks):
            for suit in Card.suits:
                for rank in Card.ranks:
                    self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

class Card:
    suits = ('Heart', 'Diamonds', 'Clubs', 'Spades')
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.getValue(rank)
        self.cardHiLoValue = self.getHiLoValue(rank)
    
    def getValue(self, rank):
        cardValues = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5, 
            '6': 6,
            '7': 7, 
            '8': 8,
            '9': 9,
            '10': 10,
            'K': 10,
            'Q': 10,
            'J': 10,
            'A': 11
        }

        return cardValues[rank]

    def getHiLoValue(self, rank):
        cardHiLoValues = {
            '2': 1,
            '3': 1,
            '4': 1,
            '5': 1, 
            '6': 1,
            '7': 0, 
            '8': 0,
            '9': 0,
            '10': -1,
            'K': -1,
            'Q': -1,
            'J': -1,
            'A': -1
        }

        return cardHiLoValues[rank]

class Hand:
    def __init__(self):
        self.cards = []
        self.value = self.calcalateHandValue()

    def calcalateHandValue(self):
        pass

    def addCard(self):
        pass

class Player:
    def __init__(self, bankroll):
        self.bankroll = bankroll

class Payout:
    def __init__(self):
        pass

    def calculatePayout(self, playerHand, dealerHand, betAmount):
        # Blackjack
        if len(playerHand) == 2 and playerHand.value == 21 and dealerHand.value != 21:
            return (betAmount * 3/2)
        # Tie
        elif playerHand.value == dealerHand.value:
            return 0
        # Win
        elif playerHand.value <= 21 and (dealerHand.value < playerHand.value or dealerHand > 21):
            return betAmount
        # Lost
        else:
            return -betAmount

def basicStrategy(playerHand, dealerUpcard, allowDAS, allowDouble):
    # Pair Splitting
    if len(playerHand) == 2 and (playerHand[0].value == playerHand[1].value):
        if playerHand[0].rank in ('A', '8'):
            print("split")
        elif playerHand[0].rank in ('K', 'Q', 'J', '10', '5'):
            print("dont split")
        elif playerHand[0].rank == '9':
            if dealerUpcard.rank in ('A', 'K', 'Q', 'J', '10', '7'):
                print("dont split")
            else:
                print("split")
        elif playerHand[0].rank == '7':
            if dealerUpcard.rank in ('A', 'K', 'Q', 'J', '10', '9', '8'):
                print("dont split")
            else:
                print("split")
        elif playerHand[0].rank == '6':
            if dealerUpcard.rank in ('A', 'K', 'Q', 'J', '10', '9', '8', '7'):
                print("dont split")
            elif dealerUpcard.rank == '2':
                print("double after split" if allowDAS else "dont split")
            else:
                print("split")
        elif playerHand[0].rank == '4':
            if dealerUpcard.rank in ('A', 'K', 'Q', 'J', '10', '9', '8', '7', '4', '3', '2'):
                print("dont split")
            elif dealerUpcard.rank in ('5', '6'):
                print("double after split" if allowDAS else "dont split")
        elif playerHand[0].rank in ('2', '3'):
            if dealerUpcard.rank in ('A', 'K', 'Q', 'J', '10', '9', '8'):
                print("dont split")
            elif dealerUpcard.rank in ('7', '6', '5', '4'):
                print("split")
            else:
                print("double after split" if allowDAS else "dont split")

    # Hard Total
    hardTotal = playerHand[0].value + playerHand[1].value

    if hardTotal == (17, 18, 19, 20):
        print("stand")
    elif hardTotal == (13, 14, 15, 16):
        if dealerUpcard.rank in ('2', '3', '4', '5', '6'):
            print("stand")
        else:
            print("hit")
    elif hardTotal == 12:
        if dealerUpcard.rank in ('4', '5', '6'):
            print("stand")
        else:
            print("hit")
    elif hardTotal == 11:
        print("double")
    elif hardTotal == 10:
        if dealerUpcard.rank in ('A', 'K', 'Q', 'J', '10'):
            print("hit")
        else:
            print("double")
    elif hardTotal == 9:
        if dealerUpcard.rank in ('3', '4', '5', 6):
            print("double")
        else:
            print("hit")
    elif (hardTotal <= 8):
        print("hit")

    # Soft Total
    softTotal = 0
    if softTotal == 20:
        print("stand")
    elif softTotal == 19:
        if dealerUpcard.rank == '6':
            print("double" if allowDouble else "stand")
        else:
            print("stand")
    elif softTotal == 18:
        if dealerUpcard.rank in ('2', '3', '4', '5', '6'):
            print("double" if allowDouble else "stand")
        elif dealerUpcard.rank in ('7', '8'):
            print("stand")
        else:
            print("hit")
    elif softTotal == 17:
        if dealerUpcard.rank in ('3', '4', '5', '6'):
            print("double" if allowDouble else "hit")
        else:
            print("hit")
    elif softTotal == (15, 16):
        if dealerUpcard.rank in ('4', '5', '6'):
            print("double" if allowDouble else "hit")
        else:
            print("hit")
    elif softTotal == (13, 14):
        if dealerUpcard.rank in ('5', '6'):
            print("double" if allowDouble else "hit")
        else:
            print("hit")

if __name__ == "__main__":

    deck = Deck(5)
    deck.buildDeck()
    deck.shuffle()
    playerCard = deck.draw()
    print(playerCard.suit, playerCard.rank)
    secondCard = deck.draw()
    print(secondCard.suit, secondCard.rank)
    print(len(deck.cards))

    # firstCard = Card('3')
    # secondCard = Card('3')
    # dealerUpcard = Card('3')
    # playerHand = [firstCard, secondCard]

    # basicStrategy(playerHand, dealerUpcard)

