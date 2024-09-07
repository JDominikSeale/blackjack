import random
import json

class game():
    def __init__(self, size=4):
        self.shoe = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] * size
        self.gameOrder = []

    def shuffle(self):
        random.shuffle(self.shoe)

    def initDeal(self):
        for i in range(2):
            for p in self.gameOrder:
                p.draw()

    def startGame(self):
        self.initDeal()
        again = self.gameLoop()
        if again:
            self.startGame()
        else:
            print("Thanks for playing!")
            quit()

    def winCon(self):
        for p in self.gameOrder:
            if p.dealer:
                dealer = p
            else:
                player = p
        if sum(dealer.hand) > sum(player.hand):
            print("Dealer Wins!")
        else:
            print("Player Wins!")
        print("Would you like to play again?")
        i = input("1. Yes\n2. No\n")
        if i == 2:
            return False
        self.startGame()

    def gameLoop(self):
        split = False
        self.rollOut = False
        for p in self.gameOrder:
            if p.dealer:
                if sum(p.hand) == 21:
                    print("Dealer Blackjack!")
                    return False
                print(p.hand[0])
            elif self.rollOut and p.dealer:
                while sum(p.hand) < 17:
                    p.draw()
                self.winCon()
            elif self.rollOut == False:
                p.evalHand()
                if p.hand[0] == p.hand[1]:
                    split = True
                choice = self.gameOptions(split)
                self.gameDecision(p, int(choice))
                p.evalHand()
                if sum(p.hand) > 21:
                    print("Bust!")
                    print("Would you like to play again?")
                    i = input("1. Yes\n2. No\n")
                    if i == 2:
                        return False
                    return True
                if self.rollOut:
                    self.gameLoop()
                    

    def gameOptions(self, split):
        print("1. Hit")
        print("2. Stand")
        print("3. Double Down")
        if split:
            print("4. Split")
            
        return input("What would you like to do?\n")
    
    def gameDecision(self, p, d):
        fin = False
        if d == 1:
            p.draw()
            return True
        elif d == 2:
            fin = p.stand()
            self.rollOut = True
        elif d == 3:
            p.money -= p.initialbet
            p.draw()
            fin = p.stand()

        return fin

class player(game):
    def __init__(self, shoe=None, dealer=False):
        super().__init__()
        self.dealer = dealer
        if shoe is not None:
            self.shoe = shoe
        if dealer:
            self.shuffle()
        self.money = 1000
        self.initialbet = 10
        self.hand = []

    def draw(self):
        self.hand.append(self.shoe.pop(0))

    
    def stand(self):
        return True
    
    def evalHand(self):
        print(self.hand, sum(self.hand))
        return self.hand, sum(self.hand)


if __name__ == "__main__":
    main = game()
    main.shuffle()
    dealer = player(main.shoe, True)
    pos1 = player(main.shoe)
    main.gameOrder = [dealer, pos1]
    main.startGame()