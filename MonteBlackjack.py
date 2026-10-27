import random
import numpy as np

class BlackJackJackSimulator:
    def __init__(self, numDecks, allowDAS, allowDouble):
        self.numDecks = numDecks
        self.shoe = Shoe(numDecks)
        self.allowDas = allowDAS
        self.allowDouble = allowDouble
        self.runningCount = 0
        self.trueCount = self.calculateTrueCount()

    def calculateRunningCount(self, cardHiLoValue):
        self.runningCount += cardHiLoValue
        self.trueCount = self.calculateTrueCount()

    def calculateTrueCount(self):
        return round(self.runningCount / self.numDecks)

class Shoe:
    def __init__(self, numDecks):
        self.stack = []
        self.numDecks = numDecks

    def buildDeck(self):
        for _ in range(self.numDecks):
            for suit in Card.suits:
                for rank in Card.ranks:
                    self.stack.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.stack)

    def deal(self):
        return self.stack.pop()

    def __len__(self):
        return len(self.stack)

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
        self.value = 0

    def calculateHandValue(self):
        totalHandValue = 0
        totalAces = 0

        for card in self.cards:
            totalHandValue += card.value
            if card.rank == 'A':
                totalAces += 1

        while totalHandValue > 21 and totalAces > 0:
            totalHandValue -= 10
            totalAces -= 1

        return totalHandValue

    def addCard(self, card):
        self.cards.append(card)
        self.value = self.calculateHandValue()

class Player:
    def __init__(self, bankroll, shoe):
        self.bankroll = bankroll
        self.hands = [Hand()]
        self.handIndex = 0
        self.betSize = 0
        self.shoe = shoe

    def placeBet(self, betAmount):
        if betAmount > self.bankroll:
            print("Insufficient funds")
        else:
            self.betSize += betAmount
            self.bankroll -= betAmount

    def stand(self):
        self.handIndex += 1
    
    def double(self):
        if len(self.hands[self.handIndex].cards) != 2:
            print("Cannot double down")
        else:
            self.hit()
            self.betSize *= 2

    def hit(self):
        cardDealt = self.shoe.deal()
        self.hands[self.handIndex].addCard(cardDealt)

    def split(self):
        newHand = Hand()
        newHand.addCard(self.hands[self.handIndex].cards.pop())

        newCardFirst = self.shoe.deal()
        newCardSecond = self.shoe.deal()

        self.hands[self.handIndex].addCard(newCardFirst)
        newHand.addCard(newCardSecond)

        self.hands.append(newHand)

    def surrender(self):
        self.handIndex += 1

    def isTwentyOne(self, hand):
        return self.hands[hand].value == 21 and len(self.hands[hand].cards) == 2

    def isBlackjack(self, hand):
        return self.hands[hand].value == 21 and len(self.hands[hand].cards) == 2

    def isBust(self, hand):
        return self.hands[hand].value > 21

    def checkHandStatus(self):
        handIndex = self.handIndex
        bustStatus = self.isBust(self.hands[handIndex])
        blackjackStatus = self.isBlackjack(self.hands[handIndex])
        twentyOneStatus = self.isTwentyOne(self.hands[handIndex])

        if (bustStatus):
            print("Bust")
            self.handIndex += 1
        elif (blackjackStatus):
            print("Blackjack!")
            self.handIndex += 1
        elif (twentyOneStatus):
            print("21")
            self.handIndex += 1

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

    blackjack = BlackJackJackSimulator(5, True, True)

    shoe = blackjack.shoe

    shoe.buildDeck()
    shoe.shuffle()

    playerOne = Player(bankroll=1000, shoe=shoe)

    for i in range(2):
        playerOne.hit()

    print("Initial Hand: " + playerOne.hands[0].cards[0].rank, playerOne.hands[0].cards[1].rank)
    print("At hand: " + str(playerOne.handIndex))
    
    playerOne.split()

    print("At hand after split: " + str(playerOne.handIndex))
    print("First Split: " + playerOne.hands[0].cards[0].rank, playerOne.hands[0].cards[1].rank)
    print("Second Split: " + playerOne.hands[1].cards[0].rank, playerOne.hands[1].cards[1].rank)

    playerOne.stand()
    print("At hand: " + str(playerOne.handIndex))
    print()

    playerOne.split()
    print("First Split: " + playerOne.hands[1].cards[0].rank, playerOne.hands[1].cards[1].rank)
    print("Second Split: " + playerOne.hands[2].cards[0].rank, playerOne.hands[2].cards[1].rank)

    playerOne.stand()

    playerOne.split()
    print("First Split: " + playerOne.hands[playerOne.handIndex].cards[0].rank, playerOne.hands[1].cards[1].rank)
    print("Second Split: " + playerOne.hands[2].cards[0].rank, playerOne.hands[2].cards[1].rank)

    # playerOne.split()

    # print(playerOne.hands[0].cards[0].rank, playerOne.hands[0].cards[1].rank)
    # print(playerOne.hands[1].cards[0].rank, playerOne.hands[1].cards[1].rank)
    # print(playerOne.hands[2].cards[0].rank, playerOne.hands[2].cards[1].rank)